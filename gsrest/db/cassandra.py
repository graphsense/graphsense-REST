from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory, SimpleStatement,\
    dict_factory, ValueSequence
from cassandra.concurrent import execute_concurrent
from math import floor

from gsrest.util.exceptions import BadConfigError

BUCKET_SIZE = 25000  # TODO: get BUCKET_SIZE from cassandra

BLOCKS_PAGE_SIZE = 100
ADDRESS_PAGE_SIZE = 100
TXS_PAGE_SIZE = 100
ENTITY_PAGE_SIZE = 100
ENTITY_ADDRESSES_PAGE_SIZE = 100

ADDRESS_PREFIX_LENGTH = 5
LABEL_PREFIX_LENGTH = 3
TX_PREFIX_LENGTH = 5


def to_hex(paging_state):
    return paging_state.hex() if paging_state is not None else None


def from_hex(page):
    return bytes.fromhex(page) if page else None


class Cassandra():

    def __init__(self, config):
        if 'currencies' not in config:
            raise BadConfigError('Missing config property: currencies')
        if 'nodes' not in config:
            raise BadConfigError('Missing config property: nodes')
        if 'tagpacks' not in config:
            raise BadConfigError('Missing config property: tagpacks')
        self.config = config
        self.cluster = Cluster(config['nodes'])
        self.session = self.cluster.connect()
        self.check_keyspace(config['tagpacks'])
        for currency in config['currencies']:
            self.check_keyspace(config['currencies'][currency]['raw'])
            self.check_keyspace(config['currencies'][currency]['transformed'])

    def check_keyspace(self, keyspace):
        query = ("SELECT * FROM system_schema.keyspaces "
                 "where keyspace_name = %s")
        result = self.session.execute(query, [keyspace])
        if result is None or result.one() is None:
            raise BadConfigError("Keyspace {} does not exist".format(keyspace))

    def get_prefix_lengths(self):
        return {'address': ADDRESS_PREFIX_LENGTH,
                'tx': TX_PREFIX_LENGTH,
                'label': LABEL_PREFIX_LENGTH}

    def get_supported_currencies(self):
        return self.config['currencies'].keys()

    def get_keyspace_mapping(self, currency, keyspace_type):
        if currency is None and keyspace_type == 'tagpacks':
            return self.config['tagpacks']
        if currency is None:
            raise ValueError('Missing currency')
        if keyspace_type not in ('raw', 'transformed'):
            raise ValueError('Unknown keyspace type {}'.format(keyspace_type))
        if currency not in self.config['currencies']:
            raise BadConfigError('Unknown currency in config: {}'
                                 .format(currency))
        return self.config['currencies'][currency][keyspace_type]

    def get_session(self, currency, keyspace_type):
        # enforce standard row factory (can be overridden on service-level)
        self.session.row_factory = named_tuple_factory

        keyspace = self.get_keyspace_mapping(currency, keyspace_type)
        self.session.set_keyspace(keyspace)

        return self.session

    def close(self):
        self.cluster.shutdown()

    def concurrent(self, session, statements_and_params):
        result = execute_concurrent(session, statements_and_params,
                                    raise_on_first_error=False)
        return [row.one() for (success, row) in result if success]

    def get_currency_statistics(self, currency):
        session = self.get_session(currency, 'transformed')
        query = "SELECT * FROM summary_statistics LIMIT 1"
        return session.execute(query).one()

    def get_block(self, currency, height):
        session = self.get_session(currency, 'raw')
        query = "SELECT * FROM block WHERE height = %s"
        return session.execute(query, [height]).one()

    def list_blocks(self, currency, page=None):
        session = self.get_session(currency, 'raw')
        paging_state = from_hex(page)

        query = "SELECT * FROM block"
        statement = SimpleStatement(query, fetch_size=BLOCKS_PAGE_SIZE)
        results = session.execute(statement, paging_state=paging_state)

        return results, to_hex(paging_state)

    def list_block_txs(self, currency, height):
        session = self.get_session(currency, 'raw')

        query = "SELECT * FROM block_transactions WHERE height = %s"
        result = session.execute(query, [height])
        if result:
            return result.one()

    def get_rates(self, currency, height=None):
        session = self.get_session(currency, 'transformed')
        session.row_factory = dict_factory
        query = "SELECT * FROM exchange_rates WHERE height = %s"
        result = session.execute(query, [height])
        if result is None:
            return None
        return result.current_rows[0]

    def list_rates(self, currency, heights):
        session = self.get_session(currency, 'transformed')
        session.row_factory = dict_factory

        concurrent_query = "SELECT * FROM exchange_rates WHERE height = %s"
        statements_and_params = []
        for h in heights:
            statements_and_params.append((concurrent_query, [h]))
        return self.concurrent(session, statements_and_params)

    def list_address_txs(self, currency, address, page=None, pagesize=None):
        paging_state = from_hex(page)
        address_id, address_id_group = \
            self.get_address_id_id_group(currency, address)
        session = self.get_session(currency, 'transformed')
        query = "SELECT * FROM address_transactions WHERE address_id = %s " \
                "AND address_id_group = %s"
        fetch_size = ADDRESS_PAGE_SIZE
        if pagesize:
            fetch_size = pagesize
        statement = SimpleStatement(query, fetch_size=fetch_size)
        results = session.execute(statement, [address_id, address_id_group],
                                  paging_state=paging_state)
        if results is None:
            return [], None
        return results.current_rows, to_hex(results.paging_state)

    def get_address_by_id_group(self, currency, address_id_group, address_id):
        session = self.get_session(currency, 'transformed')
        query = "SELECT address FROM address_by_id_group WHERE " \
                "address_id_group = %s and address_id = %s"
        result = session.execute(query, [address_id_group, address_id])
        return result.one().address if result else None

    def get_address_id(self, currency, address):
        session = self.get_session(currency, 'transformed')
        query = "SELECT * FROM address WHERE address_prefix = %s " \
                "AND address = %s"
        result = session.execute(query,
                                 [address[:ADDRESS_PREFIX_LENGTH], address])
        if result:
            return result.one().address_id

    def get_address_id_id_group(self, currency, address):
        address_id = self.get_address_id(currency, address)
        id_group = self.get_id_group(address_id)
        return address_id, id_group

    def get_id_group(self, id_):
        # if BUCKET_SIZE depends on the currency, we need session = ... here
        return floor(id_ / BUCKET_SIZE)

    def get_address(self, currency, address):
        session = self.get_session(currency, 'transformed')

        query = \
            "SELECT * FROM address WHERE address_prefix = %s AND address = %s"
        result = session.execute(
            query, [address[:ADDRESS_PREFIX_LENGTH], address])
        if result:
            return result.one()

    def list_address_tags(self, currency, address):
        session = self.get_session(currency, 'transformed')

        query = "SELECT * FROM address_tags WHERE address = %s"
        results = session.execute(query, [address])
        if results is None:
            return []
        return results.current_rows

    def get_address_entity_id(self, currency, address):
        session = self.get_session(currency, 'transformed')
        address_id, address_id_group = \
            self.get_address_id_id_group(currency, address)

        query = "SELECT cluster FROM address_cluster WHERE " \
                "address_id_group = %s AND address_id = %s "
        result = session.execute(query, [address_id_group, address_id])
        if result:
            return result.one().cluster

    def list_address_relations(self, currency, address, is_outgoing,
                               page=None, pagesize=None):
        paging_state = from_hex(page)
        session = self.get_session(currency, 'transformed')

        address_id, address_id_group = \
            self.get_address_id_id_group(currency, address)
        if not address_id:
            raise RuntimeError("Address {} not found in currency {}"
                               .format(address, currency))
        src, dst, table = ('src', 'dst', 'outgoing') \
            if is_outgoing else ('dst', 'src', 'incoming')

        query = "SELECT * FROM address_"+table+"_relations WHERE " \
                + src + "_address_id_group = %s AND "+src+"_address_id = %s"
        fetch_size = ADDRESS_PAGE_SIZE
        if pagesize:
            fetch_size = pagesize
        statement = SimpleStatement(query, fetch_size=fetch_size)
        session.row_factory = dict_factory
        results = session.execute(statement, [address_id_group, address_id],
                                  paging_state=paging_state)
        if results is None:
            return [], None

        for row in results.current_rows:
            address_id_group = \
                self.get_id_group(row[dst+'_address_id'])
            address = \
                self.get_address_by_id_group(
                     currency,
                     address_id_group,
                     row[dst+'_address_id'])
            row['id'] = address
        return results.current_rows, to_hex(results.paging_state)

    def list_address_links(self, currency, address, neighbor):
        session = self.get_session(currency, 'transformed')

        address_id, address_id_group = \
            self.get_address_id_id_group(currency, address)
        neighbor_id, neighbor_id_group = \
            self.get_address_id_id_group(currency, neighbor)
        if address_id is None or neighbor_id is None:
            raise RuntimeError("Links between {} and {} not found"
                               .format(address, neighbor))

        query = "SELECT tx_list FROM address_outgoing_relations WHERE " \
                "src_address_id_group = %s AND src_address_id = %s AND " \
                "dst_address_id = %s"
        results = session.execute(query, [address_id_group, address_id,
                                          neighbor_id])
        if not results.current_rows:
            return []

        txs = [tx_hash for tx_hash in
               results.current_rows[0].tx_list]
        query = "SELECT * FROM address_transactions WHERE " \
                "address_id_group = %s AND address_id = %s AND " \
                "tx_hash IN %s"
        results1 = session.execute(query, [address_id_group, address_id,
                                           ValueSequence(txs)])
        results2 = session.execute(query, [neighbor_id_group, neighbor_id,
                                           ValueSequence(txs)])

        if not results1.current_rows or not results2.current_rows:
            return []

        links = dict()
        for row in results1.current_rows:
            hsh = row.tx_hash.hex()
            links[hsh] = dict()
            links[hsh]['tx_hash'] = hsh
            links[hsh]['height'] = row.height
            links[hsh]['timestamp'] = row.timestamp
            links[hsh]['input_value'] = row.value
        for row in results2.current_rows:
            hsh = row.tx_hash.hex()
            links[hsh]['output_value'] = row.value
        return links.values()

    def list_matching_addresses(self, currency, expression):
        session = self.get_session(currency, 'transformed')
        query = "SELECT address FROM address WHERE address_prefix = %s"
        result = None
        paging_state = None
        statement = SimpleStatement(query, fetch_size=ADDRESS_PAGE_SIZE)
        rows = []
        while result is None or paging_state is not None:
            result = session.execute(
                        statement,
                        [expression[:ADDRESS_PREFIX_LENGTH]],
                        paging_state=paging_state)
            rows += [row.address for row in result
                     if row.address.startswith(expression)]
        return rows

    def list_entity_tags(self, currency, entity):
        session = self.get_session(currency, 'transformed')
        entity_group = self.get_id_group(entity)
        query = ("SELECT * FROM cluster_tags "
                 "WHERE cluster_group = %s and cluster"
                 " = %s")
        results = session.execute(query, [entity_group, entity])

        if results is None:
            return []
        return results.current_rows

    def get_entity(self, currency, entity):
        session = self.get_session(currency, 'transformed')
        entity_id_group = self.get_id_group(entity)
        query = ("SELECT * FROM cluster "
                 "WHERE cluster_group = %s AND cluster = %s ")
        result = session.execute(query, [entity_id_group, entity])
        if result:
            return result.one()

    def list_entity_addresses(self, currency, entity, page=None,
                              pagesize=None):
        paging_state = from_hex(page)
        session = self.get_session(currency, 'transformed')
        entity_id_group = self.get_id_group(entity)
        query = ("SELECT * FROM cluster_addresses "
                 "WHERE cluster_group = %s AND cluster = %s")
        fetch_size = ENTITY_ADDRESSES_PAGE_SIZE
        if pagesize:
            fetch_size = pagesize
        statement = SimpleStatement(query, fetch_size=fetch_size)
        session.row_factory = dict_factory
        results = session.execute(statement, [entity_id_group, entity],
                                  paging_state=paging_state)
        if results is None:
            return []

        for row in results.current_rows:
            address_id_group = self.get_id_group(row['address_id'])
            address = self.get_address_by_id_group(currency, address_id_group,
                                                   row['address_id'])
            row['address'] = address
        return results.current_rows, to_hex(results.paging_state)

    def list_entity_neighbors(self, currency, entity, is_outgoing,
                              targets=None, page=None, pagesize=None):
        paging_state = from_hex(page)
        if is_outgoing:
            table, this, that = ('outgoing', 'src', 'dst')
        else:
            table, this, that = ('incoming', 'dst', 'src')

        session = self.get_session(currency, 'transformed')
        entity_id_group = self.get_id_group(entity)

        has_targets = isinstance(targets, list)
        parameters = [entity_id_group, entity]
        basequery = "SELECT * FROM cluster_{}_relations WHERE " \
                    "{}_cluster_group = %s AND " \
                    "{}_cluster = %s".format(table, this, this)
        if has_targets:
            if len(targets) == 0:
                return None
            query = basequery.replace('*', '{}_cluster'.format(that))
            query += " AND {}_cluster in ({})" \
                .format(that, ','.join(map(str, targets)))
        else:
            query = basequery
        fetch_size = ENTITY_PAGE_SIZE
        if pagesize:
            fetch_size = pagesize
        statement = SimpleStatement(query, fetch_size=fetch_size)
        results = session.execute(statement, parameters,
                                  paging_state=paging_state)
        paging_state = results.paging_state
        if has_targets:
            statements_and_params = []
            query = basequery + " AND {}_cluster = %s".format(that)
            for row in results.current_rows:
                params = parameters.copy()
                params.append(getattr(row, "{}_cluster".format(that)))
                statements_and_params.append((query, params))
            results = self.concurrent(session, statements_and_params)
        return results, to_hex(paging_state)

    def list_tags(self, label, currency=None):
        if(currency is None):
            tags = []
            for currency in self.config['currencies']:
                tags += self.list_tags(label, currency)
            return tags

        label_norm_prefix = label[:LABEL_PREFIX_LENGTH]

        session = self.get_session(currency=currency,
                                   keyspace_type='transformed')
        query = "SELECT * FROM tag_by_label WHERE label_norm_prefix = %s and "\
                "label_norm = %s"
        rows = session.execute(query, [label_norm_prefix, label])
        if rows is None:
            return []
        return rows

    def list_labels(self, currency, expression_norm):
        expression_norm_prefix = expression_norm[:LABEL_PREFIX_LENGTH]

        session = self.get_session(currency=currency,
                                   keyspace_type='transformed')
        query = "SELECT label, label_norm, currency FROM tag_by_label WHERE " \
                "label_norm_prefix = %s GROUP BY label_norm_prefix, label_norm"
        result = session.execute(query, [expression_norm_prefix])
        if result is None:
            return []
        return result

    def list_concepts(self, taxonomy):
        session = self.get_session(currency=None, keyspace_type='tagpacks')

        query = "SELECT * FROM concept_by_taxonomy_id WHERE taxonomy = %s"
        rows = session.execute(query, [taxonomy])
        if rows is None:
            return []
        return rows

    def list_taxonomies(self, ):
        session = self.get_session(currency=None, keyspace_type='tagpacks')

        query = "SELECT * FROM taxonomy_by_key LIMIT 100"
        rows = session.execute(query)
        if rows is None:
            return []
        return rows

    def get_tx(self, currency, tx_hash):
        session = self.get_session(currency, 'raw')

        query = \
            "SELECT * FROM transaction WHERE tx_prefix = %s AND tx_hash = %s"
        result = session.execute(query, [tx_hash[:TX_PREFIX_LENGTH],
                                         bytearray.fromhex(tx_hash)])
        if result:
            return result.one()

    def list_txs(self, currency, page=None):
        session = self.get_session(currency, 'raw')

        paging_state = from_hex(page)
        query = "SELECT * FROM transaction"
        statement = SimpleStatement(query, fetch_size=TXS_PAGE_SIZE)
        results = session.execute(statement, paging_state=paging_state)

        if results is None:
            return [], None
        return results.current_rows, to_hex(results.paging_state)

    def list_matching_txs(self, currency, expression, leading_zeros):
        session = self.get_session(currency, 'raw')
        query = 'SELECT tx_hash from transaction where tx_prefix = %s'
        results = session.execute(query, [expression[:TX_PREFIX_LENGTH]])
        if results is None:
            return []
        return results
