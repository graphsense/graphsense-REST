from collections import namedtuple
from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory, SimpleStatement,\
    dict_factory, ValueSequence
from cassandra.concurrent import execute_concurrent, \
    execute_concurrent_with_args
from math import floor

from gsrest.util.exceptions import BadConfigError

PAGE_SIZE = 1000
SEARCH_PAGE_SIZE = 100

ADDRESS_PREFIX_LENGTH = 5
LABEL_PREFIX_LENGTH = 3
TX_PREFIX_LENGTH = 5

ETH_BLOCK_BUCKET_SIZE = 100000
ETH_ADDRESS_PREFIX_LENGTH = 4
ETH_TX_PREFIX_LENGTH = 4


def to_hex(paging_state):
    return paging_state.hex() if paging_state is not None else None


def from_hex(page):
    return bytes.fromhex(page) if page else None


class Cassandra():

    def eth(func):
        def check(*args, **kwargs):
            self = args[0]
            currency = args[1]
            if(currency == 'eth'):
                do = func.__name__ + "_eth"
                if hasattr(self, do) and callable(getattr(self, do)):
                    f = getattr(self, do)
                    args = args[1:]
                    return f(*args, **kwargs)
            return func(*args, **kwargs)
        return check

    def new(func):
        def check(*args, **kwargs):
            self = args[0]
            currency = args[1]
            if(currency == 'eth'):
                do = func.__name__ + "_new"
                if hasattr(self, do) and callable(getattr(self, do)):
                    f = getattr(self, do)
                    args = args[1:]
                    return f(*args, **kwargs)
            return func(*args, **kwargs)
        return check

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
        self.parameters = {}
        for currency in config['currencies']:
            self.check_keyspace(config['currencies'][currency]['raw'])
            self.check_keyspace(config['currencies'][currency]['transformed'])
            self.load_parameters(currency)

    def check_keyspace(self, keyspace):
        query = ("SELECT * FROM system_schema.keyspaces "
                 "where keyspace_name = %s")
        result = self.session.execute(query, [keyspace])
        if result is None or result.one() is None:
            raise BadConfigError("Keyspace {} does not exist".format(keyspace))

    def load_parameters(self, keyspace):
        session = self.get_session(keyspace, 'transformed')
        query = "SELECT * FROM configuration"
        session.row_factory = dict_factory
        result = session.execute(query)
        if result is None or result.one() is None:
            raise BadConfigError(
                "No configuration table found for keyspace {}"
                .format(keyspace))
        self.parameters[keyspace] = result.one()

    def get_prefix_lengths(self, currency):
        return {'address': ADDRESS_PREFIX_LENGTH
                if currency != 'eth' else ETH_ADDRESS_PREFIX_LENGTH,
                'tx': TX_PREFIX_LENGTH
                if currency != 'eth' else ETH_TX_PREFIX_LENGTH,
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
        self.session.default_fetch_size = PAGE_SIZE

        keyspace = self.get_keyspace_mapping(currency, keyspace_type)
        self.session.set_keyspace(keyspace)

        return self.session

    def close(self):
        self.cluster.shutdown()

    def concurrent(self, session, statements_and_params):
        result = execute_concurrent(session, statements_and_params,
                                    raise_on_first_error=False)
        return [row.one() for (success, row) in result if success]

    def concurrent_with_args(self, session, statement, params):
        result = execute_concurrent_with_args(
            session, statement, params, raise_on_first_error=False,
            results_generator=True)
        return [row.one() for (success, row) in result
                if success and row.one()]

    @eth
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
        results = session.execute(query, paging_state=paging_state)

        return results, to_hex(results.paging_state)

    @eth
    def list_block_txs(self, currency, height):
        session = self.get_session(currency, 'raw')

        query = "SELECT * FROM block_transactions WHERE height = %s"
        result = session.execute(query, [height])
        if result is None or result.one() is None:
            return None
        return result.one().txs

    @new
    def get_rates(self, currency, height):
        session = self.get_session(currency, 'transformed')
        session.row_factory = dict_factory
        query = "SELECT * FROM exchange_rates WHERE height = %s"
        result = session.execute(query, [height])
        if result is None:
            return None
        return result.one()

    @new
    def list_rates(self, currency, heights):
        session = self.get_session(currency, 'transformed')
        session.row_factory = dict_factory

        concurrent_query = "SELECT * FROM exchange_rates WHERE height = %s"
        statements_and_params = []
        for h in heights:
            statements_and_params.append((concurrent_query, [h]))
        return self.concurrent(session, statements_and_params)

    @eth
    def list_address_txs(self, currency, address, page=None,
                         pagesize=None):
        paging_state = from_hex(page)
        address_id, address_id_group = \
            self.get_address_id_id_group(currency, address)
        session = self.get_session(currency, 'transformed')
        query = "SELECT * FROM address_transactions WHERE address_id = %s " \
                "AND address_id_group = %s"
        fetch_size = min(pagesize or PAGE_SIZE, PAGE_SIZE)
        statement = SimpleStatement(query, fetch_size=fetch_size)
        results = session.execute(statement, [address_id, address_id_group],
                                  paging_state=paging_state)
        if results is None:
            raise RuntimeError(
                f'address {address} not found in currency {currency}')
        return results.current_rows, to_hex(results.paging_state)

    @new
    def get_addresses_by_ids(self, currency, address_ids):
        params = [(self.get_id_group(currency, address_id),
                   address_id) for address_id in address_ids]
        session = self.get_session(currency, 'transformed')
        query = "SELECT address FROM address_by_id_group WHERE " \
                "address_id_group = %s and address_id = %s"
        return [row.address for row in
                self.concurrent_with_args(session, query, params)]

    @new
    def get_address_id(self, currency, address):
        session = self.get_session(currency, 'transformed')
        prefix = self.scrub_prefix(currency, address)
        query = "SELECT * FROM address WHERE address_prefix = %s " \
                "AND address = %s"
        result = session.execute(query,
                                 [prefix[:ADDRESS_PREFIX_LENGTH], address])
        if result:
            return result.one().address_id

    def get_address_id_id_group(self, currency, address):
        address_id = self.get_address_id(currency, address)
        if not address_id:
            raise RuntimeError("Address {} not found in currency {}"
                               .format(address, currency))
        id_group = self.get_id_group(currency, address_id)
        return address_id, id_group

    def get_id_group(self, keyspace, id_):
        return floor(int(id_) / self.parameters[keyspace]['bucket_size'])

    @new
    def get_address(self, currency, address):
        session = self.get_session(currency, 'transformed')
        prefix = self.scrub_prefix(currency, address)
        query = \
            "SELECT * FROM address WHERE address_prefix = %s AND address = %s"
        session.row_factory = dict_factory
        result = session.execute(
            query, [prefix[:ADDRESS_PREFIX_LENGTH], address])
        if result:
            return result.one()

    @new
    def list_tags_by_address(self, currency, address):
        session = self.get_session(currency, 'transformed')

        query = "SELECT * FROM address_tags WHERE address = %s"
        results = session.execute(query, [address])
        if results is None:
            return []
        return results.current_rows

    @eth
    def get_address_entity_id(self, currency, address):
        session = self.get_session(currency, 'transformed')
        address_id, address_id_group = \
            self.get_address_id_id_group(currency, address)

        query = "SELECT cluster FROM address_cluster WHERE " \
                "address_id_group = %s AND address_id = %s "
        result = session.execute(query, [address_id_group, address_id])
        if result:
            return result.one().cluster

    @eth
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

    @new
    def list_matching_addresses(self, currency, expression):
        session = self.get_session(currency, 'transformed')
        prefix = self.scrub_prefix(currency, expression)
        query = "SELECT address FROM address WHERE address_prefix = %s"
        result = None
        paging_state = None
        statement = SimpleStatement(query, fetch_size=SEARCH_PAGE_SIZE)
        rows = []
        while result is None or paging_state is not None:
            result = session.execute(
                        statement,
                        [prefix[:ADDRESS_PREFIX_LENGTH]],
                        paging_state=paging_state)
            rows += [row.address for row in result
                     if row.address.startswith(expression)]
        return rows

    @eth
    def list_entity_tags_by_entity(self, currency, entity):
        session = self.get_session(currency, 'transformed')
        entity = int(entity)
        group = self.get_id_group(currency, entity)
        query = ("SELECT * FROM cluster_tags "
                 "WHERE cluster_group = %s and cluster = %s")
        results = session.execute(query, [group, entity])

        if results is None:
            return []
        return results.current_rows

    @eth
    def list_address_tags_by_entity(self, currency, entity):
        session = self.get_session(currency, 'transformed')
        entity = int(entity)
        group = self.get_id_group(currency, entity)
        query = ("SELECT * FROM cluster_address_tags "
                 "WHERE cluster_group = %s and cluster = %s")
        session.row_factory = dict_factory
        results = session.execute(query, [group, entity])

        if results is None:
            return []
        ids = [row['address_id'] for row in results.current_rows]
        addresses = self.get_addresses_by_ids(currency, ids)
        for (row, address) in zip(results.current_rows, addresses):
            row['address'] = address
        return results.current_rows

    @eth
    def get_entity(self, currency, entity):
        session = self.get_session(currency, 'transformed')
        entity_id_group = self.get_id_group(currency, entity)
        entity = int(entity)
        session.row_factory = dict_factory
        query = ("SELECT * FROM cluster "
                 "WHERE cluster_group = %s AND cluster = %s ")
        result = session.execute(query, [entity_id_group, entity])
        if result:
            return result.one()

    @eth
    def list_entities(self, currency, ids, page=None, pagesize=None):
        session = self.get_session(currency, 'transformed')
        fetch_size = min(pagesize or PAGE_SIZE, PAGE_SIZE)
        paging_state = from_hex(page)
        session.row_factory = dict_factory
        query = \
            "SELECT * FROM cluster"
        has_ids = isinstance(ids, list)
        if has_ids:
            query += " WHERE cluster_group = %s AND cluster = %s"
            params = [[self.get_id_group(currency, id),
                       id] for id in ids]
            return self.concurrent_with_args(session, query, params), None

        statement = SimpleStatement(query, fetch_size=fetch_size)
        result = session.execute(statement, paging_state=paging_state)
        return result.current_rows, to_hex(result.paging_state)

    @eth
    def list_entity_addresses(self, currency, entity, page=None,
                              pagesize=None):
        paging_state = from_hex(page)
        session = self.get_session(currency, 'transformed')
        entity_id_group = self.get_id_group(currency, entity)
        entity = int(entity)
        query = ("SELECT * FROM cluster_addresses "
                 "WHERE cluster_group = %s AND cluster = %s")
        fetch_size = min(pagesize or PAGE_SIZE, PAGE_SIZE)
        statement = SimpleStatement(query, fetch_size=fetch_size)
        session.row_factory = dict_factory
        results = session.execute(statement, [entity_id_group, entity],
                                  paging_state=paging_state)
        if results is None:
            return []

        ids = [row['address_id'] for row in results.current_rows]
        addresses = self.get_addresses_by_ids(currency, ids)
        for (row, address) in zip(results.current_rows, addresses):
            row['address'] = address
        return results.current_rows, to_hex(results.paging_state)

    @new
    def list_neighbors(self, currency, id, is_outgoing, node_type,
                       targets=None, page=None, pagesize=None):
        if node_type == 'address':
            id = self.get_address_id(currency, id)
        else:
            id = int(id)

        return self.list_neighbors_(currency, id, is_outgoing, node_type,
                                    targets=targets, page=page,
                                    pagesize=pagesize)

    def list_neighbors_(self, currency, id, is_outgoing, node_type,
                        targets=None, page=None, pagesize=None):
        if node_type == 'entity':
            node_type = 'cluster'
        if is_outgoing:
            direction, this, that = ('outgoing', 'src', 'dst')
        else:
            direction, this, that = ('incoming', 'dst', 'src')

        id_suffix = '_id' if node_type == 'address' else ''

        session = self.get_session(currency, 'transformed')
        id_group = self.get_id_group(currency, id)
        parameters = [id_group, id]
        has_targets = isinstance(targets, list)
        sec_condition = ''
        if currency == 'eth':
            secondary_id_group = \
                self.get_secondary_id_group_eth(
                    f'address_{direction}_relations',
                    id_group)
            sec_in = self.sec_in(secondary_id_group)
            sec_condition = \
                f' AND {this}_address_id_secondary_group in {sec_in}'
            if has_targets:
                prefix = self.get_prefix_lengths('eth')
                params = []
                for target in targets:
                    address = self.entity_to_address_id(target)
                    params.append((address[:prefix['address']].upper(),
                                   bytes.fromhex(address)))
                targets = self.concurrent_with_args(
                    session,
                    "SELECT address_id FROM address_ids_by_address_prefix "
                    "WHERE address_prefix = %s AND address = %s", params)
                targets = [target.address_id for target in targets]

        basequery = (f"SELECT * FROM {node_type}_{direction}_relations WHERE "
                     f"{this}_{node_type}{id_suffix}_group = %s AND "
                     f"{this}_{node_type}{id_suffix} = %s {sec_condition}")
        if has_targets:
            if len(targets) == 0:
                return None

            query = basequery.replace('*', f'{that}_{node_type}{id_suffix}')
            targets = ','.join(map(str, targets))
            query += f' AND {that}_{node_type}{id_suffix} in ({targets})'
        else:
            query = basequery
        session.row_factory = dict_factory
        fetch_size = min(pagesize or PAGE_SIZE, PAGE_SIZE)
        statement = SimpleStatement(query, fetch_size=fetch_size)
        paging_state = from_hex(page)
        results = session.execute(statement, parameters,
                                  paging_state=paging_state)
        paging_state = results.paging_state
        results = results.current_rows
        if has_targets:
            statements_and_params = []
            query = basequery + f" AND {that}_{node_type}{id_suffix} = %s"
            for row in results:
                params = parameters.copy()
                params.append(row[f'{that}_{node_type}{id_suffix}'])
                statements_and_params.append((query, params))
            results = self.concurrent(session, statements_and_params)
        if node_type == 'address':
            ids = [row[that+'_address_id'] for row in results]
            addresses = self.get_addresses_by_ids(currency, ids)
            for (row, address) in zip(results, addresses):
                row[f'{that}_address'] = address
        if node_type == 'cluster':
            for row in results:
                row['estimated_value'] = row['value']
        return results, to_hex(paging_state)

    def list_address_tags(self, currency, label):
        label_norm_prefix = label[:LABEL_PREFIX_LENGTH]

        session = self.get_session(currency=currency,
                                   keyspace_type='transformed')
        query = ("SELECT * FROM address_tag_by_label WHERE "
                 "label_norm_prefix = %s and label_norm = %s")
        rows = session.execute(query, [label_norm_prefix, label])
        if rows is None:
            return []
        return rows

    def list_labels(self, currency, expression_norm):
        expression_norm_prefix = expression_norm[:LABEL_PREFIX_LENGTH]

        session = self.get_session(currency=currency,
                                   keyspace_type='transformed')
        query = ("SELECT label, label_norm, currency FROM address_tag_by_label"
                 " WHERE label_norm_prefix = %s GROUP BY label_norm_prefix, "
                 "label_norm")
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

    @eth
    def get_tx(self, currency, tx_hash):
        result = self.list_txs_by_hashes(currency, [tx_hash])
        if result:
            return result[0]

    def get_transactions_by_ids(self, currency, ids):
        session = self.get_session(currency, 'transformed')

        params = [[self.get_id_group(currency, id),
                   id] for id in ids]
        query = ("SELECT transaction_id, transaction FROM "
                 "transaction_ids_by_transaction_id_group "
                 "WHERE transaction_id_group = %s AND transaction_id = %s")
        return [(row.transaction_id, row.transaction)
                for row in self.concurrent_with_args(session, query, params)]

    def list_txs(self, currency, page=None):
        session = self.get_session(currency, 'raw')

        paging_state = from_hex(page)
        query = "SELECT * FROM transaction"
        results = session.execute(query, paging_state=paging_state)

        if results is None:
            return [], None
        return results.current_rows, to_hex(results.paging_state)

    @new
    def list_matching_txs(self, currency, expression):
        session = self.get_session(currency, 'raw')
        query = 'SELECT tx_hash from transaction where tx_prefix = %s'
        results = session.execute(query, [expression[:TX_PREFIX_LENGTH]])
        if results is None:
            return []
        return results.current_rows

    @eth
    def scrub_prefix(self, currency, expression):
        bech32_prefix = self.parameters[currency]['bech_32_prefix']
        return expression[len(bech32_prefix):] \
            if expression.startswith(bech32_prefix) \
            else expression

    @eth
    def list_txs_by_hashes(self, currency, hashes):
        prefix = self.get_prefix_lengths(currency)
        params = [[hash[:prefix['tx']],
                   bytearray.fromhex(hash)]
                  for hash in hashes]
        session = self.get_session(currency, 'raw')
        statement = ('SELECT * from transaction where '
                     'tx_prefix=%s and tx_hash=%s')
        return self.concurrent_with_args(session, statement, params)

    @new
    def list_addresses(self, currency, ids=None, page=None, pagesize=None):
        session = self.get_session(currency, 'transformed')
        fetch_size = min(pagesize or PAGE_SIZE, PAGE_SIZE)
        paging_state = from_hex(page)
        session.row_factory = dict_factory
        query = \
            "SELECT * FROM address"
        has_ids = isinstance(ids, list)
        if has_ids:
            prefix_length = self.get_prefix_lengths(currency)['address']
            query += " WHERE address_prefix = %s AND address = %s"
            params = [[self.scrub_prefix(currency, id)[:prefix_length],
                       id] for id in ids]
            return self.concurrent_with_args(session, query, params), None

        statement = SimpleStatement(query, fetch_size=fetch_size)
        result = session.execute(statement, paging_state=paging_state)
        return result.current_rows, to_hex(result.paging_state)

#####################
# ETHEREUM VARIANTS #
#####################

    def get_block_group_eth(self, id_):
        return floor(id_ / 100000)

    def get_currency_statistics_eth(self, currency):
        session = self.get_session(currency, 'transformed')
        query = "SELECT * FROM summary_statistics LIMIT 1"
        result = session.execute(query).one()
        Result = namedtuple('Result', result._fields+('no_clusters',))
        result = result._asdict()
        result['no_clusters'] = 0
        result = Result(**result)
        return result

    def scrub_prefix_eth(self, currency, expression):
        return expression

    def get_block_eth(self, height):
        session = self.get_session('eth', 'raw')
        block_group = self.get_block_group_eth(height)
        query = "SELECT * FROM block WHERE block_group = %s and number = %s"
        return session.execute(query, [block_group, height]).one()

    def list_blocks_eth(self, page=None):
        session = self.get_session('eth', 'raw')
        paging_state = from_hex(page)

        query = "SELECT * FROM block"
        results = session.execute(query, paging_state=paging_state)

        return results, to_hex(results.paging_state)

    def address_to_entity_id(self, address):
        return address + '_'

    def entity_to_address_id(self, entity):
        return entity[:-1]

    def get_entity_eth(self, currency, entity):
        # mockup entity by address
        address = self.entity_to_address_id(entity)
        address = self.get_address_new(currency, address)
        entity = address
        entity['cluster'] = self.address_to_entity_id(entity['address'])
        entity['no_addresses'] = 1
        return entity

    def list_entities_eth(self, currency, ids, page=None, pagesize=None):
        if isinstance(ids, list):
            ids = [self.entity_to_address_id(id) for id in ids]
        result, paging_state = \
            self.list_addresses(currency, ids, page, pagesize)

        for address in result:
            address['cluster'] = self.address_to_entity_id(address['address'])
            address['no_addresses'] = 1
        return result, paging_state

    def list_entity_tags_by_entity_eth(self, currency, entity):
        return []

    def list_address_tags_by_entity_eth(self, currency, entity):
        return []

    def get_address_entity_id_eth(self, currency, address):
        return self.address_to_entity_id(address)

    def list_block_txs_eth(self, currency, height):
        session = self.get_session(currency, 'transformed')
        height_group = self.get_block_group_eth(height)
        query = ("SELECT txs FROM block_transactions WHERE "
                 "height_group = %s and height = %s")
        result = session.execute(query, [height_group, height])
        if result is None:
            raise RuntimeError(
                    f'block {height} not found in currency {currency}')
        return self.list_txs_by_ids_eth(result.one().txs)

    def get_secondary_id_group_eth(self, table, id_group):
        column_prefix = ''
        if table == 'address_incoming_relations':
            column_prefix = 'dst_'
        elif table == 'address_outgoing_relations':
            column_prefix = 'src_'

        session = self.get_session('eth', 'transformed')
        query = (f"SELECT max_secondary_id FROM {table}_"
                 f"secondary_ids WHERE {column_prefix}address_id_group = %s")
        result = session.execute(query, [id_group])
        return 0 if result.one() is None else \
            result.one().max_secondary_id

    def list_address_txs_eth(self, currency, address,
                             page=None, pagesize=None):
        paging_state = from_hex(page)
        session = self.get_session(currency, 'transformed')
        address_id, id_group = self.get_address_id_id_group(currency, address)
        secondary_id_group = \
            self.get_secondary_id_group_eth('address_transactions', id_group)
        sec_in = self.sec_in(secondary_id_group)
        query = ("SELECT transaction_id FROM address_transactions WHERE "
                 "address_id_group = %s and "
                 f"address_id_secondary_group in {sec_in}"
                 " and address_id = %s")
        fetch_size = min(pagesize or PAGE_SIZE, PAGE_SIZE)
        statement = SimpleStatement(query, fetch_size=fetch_size)
        result = session.execute(statement,
                                 [id_group,
                                  address_id],
                                 paging_state=paging_state)
        if result is None:
            raise RuntimeError(
                    f'address {address} not found in currency {currency}')
        txs = [row.transaction_id for row in result.current_rows]
        paging_state = result.paging_state
        result = self.list_txs_by_ids_eth(txs)
        return result, to_hex(paging_state)

    def list_txs_by_ids_eth(self, ids):
        currency = 'eth'
        session = self.get_session(currency, 'transformed')
        params = [[self.get_id_group(currency, id), id] for id in ids]
        statement = (
            'SELECT transaction from transaction_ids_by_transaction_id_group'
            ' where transaction_id_group = %s and transaction_id = %s')
        result = self.concurrent_with_args(session, statement, params)
        return self.list_txs_by_hashes(currency,
                                       [row.transaction for row in result])

    def list_txs_by_hashes_eth(self, currency, hashes):
        prefix = self.get_prefix_lengths(currency)
        params = [[hash.hex()[:prefix['tx']], hash]
                  for hash in hashes]
        session = self.get_session(currency, 'raw')
        statement = (
            'SELECT hash, block_number, block_timestamp, value from '
            'transaction where hash_prefix=%s and hash=%s')
        return self.concurrent_with_args(session, statement, params)

    def list_address_links_eth(self, currency, address, neighbor):
        session = self.get_session(currency, 'transformed')
        address_id, id_group = self.get_address_id_id_group(currency, address)
        neighbor_id, n_id_group = \
            self.get_address_id_id_group(currency, neighbor)
        secondary_id_group = \
            self.get_secondary_id_group_eth('address_outgoing_relations',
                                            id_group)
        sec_in = self.sec_in(secondary_id_group)
        query = ("SELECT transaction_ids FROM address_outgoing_relations "
                 "WHERE src_address_id_group = %s and "
                 f"src_address_id_secondary_group in {sec_in}"
                 " and src_address_id = %s and dst_address_id = %s")
        statement = SimpleStatement(query)
        result = session.execute(statement, [id_group, address_id,
                                             neighbor_id])
        if result is None or result.one() is None:
            return [], None
        txs = result.one().transaction_ids
        return self.list_txs_by_ids_eth(txs)

    def get_tx_eth(self, currency, tx_hash):
        session = self.get_session(currency, 'raw')
        query = (
            'SELECT hash, block_number, block_timestamp, value from '
            'transaction where hash_prefix=%s and hash=%s')
        prefix_length = self.get_prefix_lengths(currency)
        prefix = tx_hash[:prefix_length['tx']]
        result = session.execute(query, [prefix, bytearray.fromhex(tx_hash)])
        if result is None:
            return None
        return result.one()

    def list_entity_addresses_eth(self, currency, entity, page=None,
                                  pagesize=None):
        address = self.entity_to_address_id(entity)
        address = self.get_address_new(currency, address)
        if address is None:
            return None
        return [address], None

##################################
# VARIANTS USING NEW DATA SCHEME #
##################################

    def backport_currencies(self, currency, values):
        currencies = list(map(lambda x: x.lower(),
                              self.parameters[currency]['fiat_currencies']))
        Values = namedtuple('Values', values._fields + (* currencies,))
        values = values._asdict()
        for (fiat, curr) in zip(values['fiat_values'], currencies):
            values[curr.lower()] = fiat
        return Values(**values)

    def get_address_id_new(self, currency, address):
        session = self.get_session(currency, 'transformed')
        prefix = self.scrub_prefix(currency, address)
        query = (
            "SELECT address_id FROM address_ids_by_address_prefix "
            "WHERE address_prefix = %s AND address = %s")
        prefix_length = self.get_prefix_lengths(currency)['address']
        result = session.execute(
            query, [prefix[:prefix_length].upper(), bytes.fromhex(address)])
        return result.one().address_id if result else None

    def get_address_new(self, currency, address):
        session = self.get_session(currency, 'transformed')
        address_id, address_id_group = \
            self.get_address_id_id_group(currency, address)

        session.row_factory = dict_factory
        query = (
            "SELECT * FROM address WHERE "
            "address_id_group = %s AND address_id = %s")
        result = session.execute(
            query, [address_id_group, address_id])
        if not result:
            return None

        result = result.one()
        result['address'] = address
        return self.finish_addresses(currency, [result])[0]

    def list_tags_by_address_new(self, currency, address):
        session = self.get_session(currency, 'transformed')
        address_id, _ = \
            self.get_address_id_id_group(currency, address)

        query = "SELECT * FROM address_tags WHERE address_id = %s"
        results = session.execute(query, [address_id])
        if results is None:
            return []
        tags = []
        for tag in results.current_rows:
            Tag = namedtuple('Tag', tag._fields + ('address',))
            tag = tag._asdict()
            tag['address'] = address
            tags.append(Tag(**tag))
        return tags

    def get_rates_new(self, currency, height):
        session = self.get_session(currency, 'transformed')
        session.row_factory = dict_factory
        query = "SELECT * FROM exchange_rates WHERE height = %s"
        result = session.execute(query, [height])
        if result is None:
            return None
        row = result.one()
        self.backport_values(currency, row)
        return row

    def backport_values(self, currency, row):
        for (fiat, curr) in zip(
                row['fiat_values'],
                self.parameters[currency]['fiat_currencies']):
            row[curr.lower()] = fiat

    def list_rates_new(self, currency, heights):
        session = self.get_session(currency, 'transformed')
        session.row_factory = dict_factory
        result = self.concurrent_with_args(
            session,
            "SELECT * FROM exchange_rates WHERE height = %s",
            [[h] for h in heights])
        for row in result:
            self.backport_values(currency, row)
        return result

    def list_matching_txs_new(self, currency, expression):
        session = self.get_session(currency, 'transformed')
        query = ('SELECT transaction from transaction_ids_by_transaction_pre'
                 'fix where transaction_prefix = %s')
        prefix_length = self.get_prefix_lengths(currency)
        prefix = expression[:prefix_length['tx']].upper()
        results = session.execute(query, [prefix])
        if results is None:
            return []
        Tx = namedtuple('Tx', ('tx_hash',))
        return [Tx(tx_hash=row.transaction) for row in results.current_rows]

    def list_matching_addresses_new(self, currency, expression):
        session = self.get_session(currency, 'transformed')
        prefix = self.scrub_prefix(currency, expression)
        query = ("SELECT address FROM address_ids_by_address_prefix "
                 "WHERE address_prefix = %s")
        result = None
        paging_state = None
        statement = SimpleStatement(query, fetch_size=SEARCH_PAGE_SIZE)
        prefix_length = self.get_prefix_lengths(currency)['address']
        rows = []
        while result is None or paging_state is not None:
            result = session.execute(
                        statement,
                        [prefix[:prefix_length].upper()],
                        paging_state=paging_state)
            rows += [row.address.hex() for row in result
                     if row.address.hex().startswith(expression)]
        return rows

    def get_addresses_by_ids_new(self, currency, address_ids):
        params = [(self.get_id_group(currency, address_id),
                   address_id) for address_id in address_ids]
        session = self.get_session(currency, 'transformed')
        query = "SELECT address FROM address_ids_by_address_id_group WHERE " \
                "address_id_group = %s and address_id = %s"
        return [row.address.hex() for row in
                self.concurrent_with_args(session, query, params)]

    def list_neighbors_new(self, currency, id, is_outgoing, node_type,
                           targets=None, page=None, pagesize=None):
        orig_node_type = node_type
        if node_type == 'address':
            id = self.get_address_id(currency, id)
        elif node_type == 'entity' and currency == 'eth':
            id = self.entity_to_address_id(id)
            id = self.get_address_id(currency, id)
            node_type = 'address'

        neighbors, page = self.list_neighbors_(currency,
                                               id,
                                               is_outgoing,
                                               node_type,
                                               targets,
                                               page,
                                               pagesize)
        dr = 'dst' if is_outgoing else 'src'
        props = dr + '_properties'
        for neighbor in neighbors:
            neighbor[props] = neighbor[props]._replace(
                total_received=self.backport_currencies(
                    currency,
                    neighbor[props].total_received),
                total_spent=self.backport_currencies(
                    currency,
                    neighbor[props].total_spent))

            neighbor['estimated_value'] = \
                self.backport_currencies(currency, neighbor['value'])
            neighbor[dr + '_labels'] = []

            if orig_node_type == 'entity' and currency == 'eth':
                neighbor[dr + '_cluster'] = \
                    self.address_to_entity_id(neighbor[dr + '_address'])
        return neighbors, page

    def list_tags_new(self, currency, label):
        label_norm_prefix = label[:LABEL_PREFIX_LENGTH]

        session = self.get_session(currency=currency,
                                   keyspace_type='transformed')
        query = ("SELECT * FROM address_tag_by_label WHERE label_norm_prefix"
                 "= %s and label_norm = %s")
        rows = session.execute(query, [label_norm_prefix, label])
        if rows is None:
            return []
        return rows

    def sec_in(self, id):
        return "(" + ','.join(map(str, range(0, id+1))) + ")"

    def list_addresses_new(self, currency, ids=None, page=None, pagesize=None):
        session = self.get_session(currency, 'transformed')
        query = "SELECT address_id, address FROM address_ids_by_address_prefix"
        has_ids = isinstance(ids, list)
        if has_ids:
            prefix_length = self.get_prefix_lengths(currency)['address']
            query += " WHERE address_prefix = %s AND address = %s"
            params = [[self.scrub_prefix(currency, id)[:prefix_length].upper(),
                       bytearray.fromhex(id)] for id in ids]
            ids = self.concurrent_with_args(session, query, params)
            paging_state = None
        else:
            fetch_size = min(pagesize or PAGE_SIZE, PAGE_SIZE)
            statement = SimpleStatement(query, fetch_size=fetch_size)
            result = session.execute(statement, paging_state=from_hex(page))
            ids = result.current_rows
            paging_state = result.paging_state

        query = (
            "SELECT * FROM address WHERE "
            "address_id_group = %s AND address_id = %s")

        ids = [((self.get_id_group(currency, row.address_id),
                 row.address_id),
                row.address)
               for row in ids]
        ids.sort()
        params = [param[0] for param in ids]
        session.row_factory = dict_factory
        result = self.concurrent_with_args(session, query, params)
        for (row, param) in zip(result, ids):
            row['address'] = param[1].hex()
        return self.finish_addresses(currency, result), to_hex(paging_state)

    def finish_addresses(self, currency, rows):
        ids = []
        for row in rows:
            ids.append(row['first_tx'].transaction_id)
            ids.append(row['last_tx'].transaction_id)
            row['total_received'] = \
                self.backport_currencies(currency, row['total_received'])
            row['total_spent'] = \
                self.backport_currencies(currency, row['total_spent'])

        txs = self.get_transactions_by_ids(currency, ids)
        TxSummary = namedtuple('TxSummary', ['height', 'timestamp',
                                             'tx_hash', 'transaction_id'])

        for i, (transaction_id, transaction) in enumerate(txs):
            row = rows[i//2]
            if row['first_tx'].transaction_id == transaction_id:
                row['first_tx'] = TxSummary(
                            height=row['first_tx'].height,
                            timestamp=row['first_tx'].block_timestamp,
                            transaction_id=transaction_id,
                            tx_hash=transaction)
            if row['last_tx'].transaction_id == transaction_id:
                row['last_tx'] = TxSummary(
                            height=row['last_tx'].height,
                            timestamp=row['last_tx'].block_timestamp,
                            transaction_id=transaction_id,
                            tx_hash=transaction)
        return rows
