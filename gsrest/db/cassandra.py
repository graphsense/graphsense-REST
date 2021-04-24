from collections import namedtuple
from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory, SimpleStatement,\
    dict_factory, ValueSequence
from cassandra.concurrent import execute_concurrent
from math import floor

from gsrest.util.exceptions import BadConfigError

BLOCKS_PAGE_SIZE = 100
ADDRESS_PAGE_SIZE = 100
TXS_PAGE_SIZE = 100
ENTITY_PAGE_SIZE = 100
ENTITY_ADDRESSES_PAGE_SIZE = 100

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

        keyspace = self.get_keyspace_mapping(currency, keyspace_type)
        self.session.set_keyspace(keyspace)

        return self.session

    def close(self):
        self.cluster.shutdown()

    def concurrent(self, session, statements_and_params):
        result = execute_concurrent(session, statements_and_params,
                                    raise_on_first_error=False)
        return [row.one() for (success, row) in result if success]

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
        statement = SimpleStatement(query, fetch_size=BLOCKS_PAGE_SIZE)
        results = session.execute(statement, paging_state=paging_state)

        return results, to_hex(results.paging_state)

    def list_block_txs(self, currency, height):
        session = self.get_session(currency, 'raw')

        query = "SELECT * FROM block_transactions WHERE height = %s"
        result = session.execute(query, [height])
        if result:
            return result.one()

    @new
    def get_rates(self, currency, height):
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

    @new
    def get_address_by_id_group(self, currency, address_id_group, address_id):
        session = self.get_session(currency, 'transformed')
        query = "SELECT address FROM address_by_id_group WHERE " \
                "address_id_group = %s and address_id = %s"
        result = session.execute(query, [address_id_group, address_id])
        return result.one().address if result else None

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
        return floor(id_ / self.parameters[keyspace]['bucket_size'])

    @new
    def get_address(self, currency, address):
        session = self.get_session(currency, 'transformed')
        prefix = self.scrub_prefix(currency, address)
        query = \
            "SELECT * FROM address WHERE address_prefix = %s AND address = %s"
        result = session.execute(
            query, [prefix[:ADDRESS_PREFIX_LENGTH], address])
        if result:
            return result.one()

    @new
    def list_address_tags(self, currency, address):
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

    @new
    def list_address_relations(self, *args, **kwargs):
        return self.list_address_relations_(*args, **kwargs)

    def list_address_relations_(self, currency, address, is_outgoing,
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
                self.get_id_group(currency, row[dst+'_address_id'])
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

    @new
    def list_matching_addresses(self, currency, expression):
        session = self.get_session(currency, 'transformed')
        prefix = self.scrub_prefix(currency, expression)
        query = "SELECT address FROM address WHERE address_prefix = %s"
        result = None
        paging_state = None
        statement = SimpleStatement(query, fetch_size=ADDRESS_PAGE_SIZE)
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
    def list_entity_tags(self, currency, entity):
        session = self.get_session(currency, 'transformed')
        entity_group = self.get_id_group(currency, entity)
        query = ("SELECT * FROM cluster_tags "
                 "WHERE cluster_group = %s and cluster"
                 " = %s")
        results = session.execute(query, [entity_group, entity])

        if results is None:
            return []
        return results.current_rows

    @eth
    def get_entity(self, currency, entity):
        session = self.get_session(currency, 'transformed')
        entity_id_group = self.get_id_group(currency, entity)
        query = ("SELECT * FROM cluster "
                 "WHERE cluster_group = %s AND cluster = %s ")
        result = session.execute(query, [entity_id_group, entity])
        if result:
            return result.one()

    def list_entity_addresses(self, currency, entity, page=None,
                              pagesize=None):
        paging_state = from_hex(page)
        session = self.get_session(currency, 'transformed')
        entity_id_group = self.get_id_group(currency, entity)
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
            address_id_group = self.get_id_group(currency, row['address_id'])
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
        entity_id_group = self.get_id_group(currency, entity)

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

    def get_transaction_by_id(self, currency, id):
        session = self.get_session(currency, 'transformed')

        id_group = self.get_id_group(currency, id)

        query = (
            "SELECT transaction FROM transaction_ids_by_transaction_id_group "
            "WHERE transaction_id_group = %s AND transaction_id = %s")
        result = session.execute(query, [id_group, id])
        if result:
            return result.one().transaction

    def list_txs(self, currency, page=None):
        session = self.get_session(currency, 'raw')

        paging_state = from_hex(page)
        query = "SELECT * FROM transaction"
        statement = SimpleStatement(query, fetch_size=TXS_PAGE_SIZE)
        results = session.execute(statement, paging_state=paging_state)

        if results is None:
            return [], None
        return results.current_rows, to_hex(results.paging_state)

    @new
    def list_matching_txs(self, currency, expression, leading_zeros):
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
        statement = SimpleStatement(query, fetch_size=BLOCKS_PAGE_SIZE)
        results = session.execute(statement, paging_state=paging_state)

        return results, to_hex(results.paging_state)

    def address_to_entity_id(self, address):
        return address + '_'

    def entity_to_address_id(self, entity):
        return entity[:-1]

    def get_entity_eth(self, currency, entity):
        # mockup entity by address
        address = self.get_address_new(currency,
                                       self.entity_to_address_id(entity))
        Entity = namedtuple('Entity',
                            address._fields + ('cluster', 'no_addresses',))
        entity = address._asdict()
        entity['cluster'] = self.address_to_entity_id(entity['address'])
        entity['no_addresses'] = 1
        return Entity(**entity)

    def list_entity_tags_eth(self, currency, entity):
        return self.list_address_tags_new(currency,
                                          self.entity_to_address_id(entity))

    def get_address_entity_id_eth(self, currency, address):
        return self.address_to_entity_id(address)

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

        query = (
            "SELECT * FROM address WHERE "
            "address_id_group = %s AND address_id = %s")
        result = session.execute(
            query, [address_id_group, address_id])
        if not result:
            return None

        result = result.one()

        result = result._replace(
            total_received=self.backport_currencies(
                currency, result.total_received),
            total_spent=self.backport_currencies(
                currency, result.total_spent))

        first_tx_hash = \
            self.get_transaction_by_id(
                currency,
                result.first_tx.transaction_id)
        last_tx_hash = \
            self.get_transaction_by_id(
                currency,
                result.last_tx.transaction_id)

        TxSummary = namedtuple('TxSummary', ['height', 'timestamp', 'tx_hash'])
        Result = namedtuple('Result', result._fields+('address',))

        first_tx = TxSummary(
                    height=result.first_tx.height,
                    timestamp=result.first_tx.block_timestamp,
                    tx_hash=first_tx_hash)
        last_tx = TxSummary(
                    height=result.last_tx.height,
                    timestamp=result.last_tx.block_timestamp,
                    tx_hash=last_tx_hash)

        result = result._asdict()
        result['address'] = address
        result = Result(**result)
        return result._replace(first_tx=first_tx, last_tx=last_tx)

    def list_address_tags_new(self, currency, address):
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
        row = result.current_rows[0]
        for (fiat, curr) in zip(
                row['fiat_values'],
                self.parameters[currency]['fiat_currencies']):
            row[curr.lower()] = fiat
        return row

    def list_matching_txs_new(self, currency, expression, leading_zeros):
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
        statement = SimpleStatement(query, fetch_size=ADDRESS_PAGE_SIZE)
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

    def get_address_by_id_group_new(self, currency,
                                    address_id_group, address_id):
        session = self.get_session(currency, 'transformed')
        query = "SELECT address FROM address_ids_by_address_id_group WHERE " \
                "address_id_group = %s and address_id = %s"
        result = session.execute(query, [address_id_group, address_id])
        return result.one().address.hex() if result else None

    def list_address_relations_new(self, currency, address, is_outgoing,
                                   page=None, pagesize=None):
        neighbors, page = self.list_address_relations_(
                            currency, address, is_outgoing, page, pagesize)
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
        return neighbors, page
