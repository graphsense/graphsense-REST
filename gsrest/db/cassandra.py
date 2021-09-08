import re
from collections import namedtuple
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement,\
    dict_factory, ValueSequence
from cassandra.concurrent import execute_concurrent, \
    execute_concurrent_with_args
from math import floor
# from codetiming import Timer

from gsrest.util.exceptions import BadConfigError

SMALL_PAGE_SIZE = 1000
BIG_PAGE_SIZE = 10000
SEARCH_PAGE_SIZE = 100


def to_hex(paging_state):
    return paging_state.hex() if paging_state is not None else None


def from_hex(page):
    return bytes.fromhex(page) if page else None


def eth_address_to_hex(address):
    if type(address) != bytes:
        return address
    return '0x' + address.hex()


def eth_address_from_hex(address):
    # eth addresses are case insensitive
    return bytes.fromhex(address[2:].lower())


def identity(x):
    return x


def replaceFrom(keyspace, query):
    r = re.compile(r'\s+FROM\s+', re.IGNORECASE)
    return r.sub(f' FROM {keyspace}.', query)


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
        self.session.row_factory = dict_factory
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
        self.parameters[keyspace] = {}
        for kind in ['raw', 'transformed']:
            query = "SELECT * FROM configuration"
            result = self.execute(keyspace, kind, query, use_dict_factory=True)
            if result is None or result.one() is None:
                raise BadConfigError(
                    "No configuration table found for keyspace {}"
                    .format(keyspace))
            for key, value in result.one().items():
                self.parameters[keyspace][key] = value

    def get_prefix_lengths(self, currency):
        p = self.parameters[currency]
        return \
            {'address': p['address_prefix_length'],
             'tx': p['tx_prefix_length'],
             'label': p['label_prefix_length']}

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

    def close(self):
        self.cluster.shutdown()

    def execute(self, currency, keyspace_type, query, params=None,
                use_dict_factory=False, paging_state=None, fetch_size=None):
        keyspace = self.get_keyspace_mapping(currency, keyspace_type)
        query = replaceFrom(keyspace, query)
        query = SimpleStatement(query, fetch_size=fetch_size)
        result = self.session.execute(query, params, paging_state=paging_state)
        return result

    def concurrent_with_args(self, currency, keyspace_type, query, params,
                             filter_empty=True, use_dict_factory=False, one=True):
        keyspace = self.get_keyspace_mapping(currency, keyspace_type)
        query = replaceFrom(keyspace, query)
        result = execute_concurrent_with_args(
            self.session, query, params, raise_on_first_error=False,
            results_generator=True)
        if filter_empty:
            return [row.one() if one else row for (success, row) in result
                    if success and (not one or row.one())]
        else:
            return [row.one() if one else row if success and (not one or row.one()) else None
                    for (success, row) in result]

    @eth
    # @Timer(text="Timer: stats {:.2f}")
    def get_currency_statistics(self, currency):
        query = "SELECT * FROM summary_statistics LIMIT 1"
        return self.execute(currency, 'transformed', query).one()

    @eth
    # @Timer(text="Timer: get_block {:.2f}")
    def get_block(self, currency, height):
        query = ("SELECT * FROM block WHERE block_id_group = %s "
                 "AND block_id = %s")
        return self.execute(currency, 'raw',
                    query, [self.get_block_id_group(currency, height), height]
                ).one()

    # @Timer(text="Timer: list_blocks {:.2f}")
    def list_blocks(self, currency, page=None):
        paging_state = from_hex(page)

        query = "SELECT * FROM block"
        results = self.execute(currency, 'raw', query, paging_state=paging_state)

        return results, to_hex(results.paging_state)

    @eth
    # @Timer(text="Timer: list_block_txs {:.2f}")
    def list_block_txs(self, currency, height):
        height_group = self.get_block_id_group(currency, height)
        query = ("SELECT txs FROM block_transactions WHERE "
                 "block_id_group = %s and block_id = %s")
        result = self.execute(currency, 'raw', query, [height_group, height])
        if result is None or result.one() is None:
            return None
        txs = [tx.tx_id for tx in result.one()['txs']]
        return self.list_txs_by_ids(currency, txs)

    # @Timer(text="Timer: get_rates {:.2f}")
    def get_rates(self, currency, height):
        query = "SELECT * FROM exchange_rates WHERE block_id = %s"
        result = self.execute(currency, 'transformed', query, [height], use_dict_factory=True)
        if result is None:
            return None
        result = result.one()
        return self.markup_rates(currency, result)

    # @Timer(text="Timer: list_rates {:.2f}")
    def list_rates(self, currency, heights):
        result = self.concurrent_with_args(
            currency,
            'transformed',
            "SELECT * FROM exchange_rates WHERE block_id = %s",
            [[h] for h in heights], use_dict_factory=True)
        for row in result:
            self.markup_rates(currency, row)
        return result

    @eth
    # @Timer(text="Timer: list_address_txs {:.2f}")
    def list_address_txs(self, currency, address, page=None,
                         pagesize=None):
        paging_state = from_hex(page)
        address_id, address_id_group = \
            self.get_address_id_id_group(currency, address)
        query = "SELECT * FROM address_transactions " \
                "WHERE address_id = %s AND address_id_group = %s"
        fetch_size = min(pagesize or BIG_PAGE_SIZE, BIG_PAGE_SIZE)
        results = self.execute(currency, 'transformed', query, [address_id, address_id_group], use_dict_factory=True,
                                  paging_state=paging_state, fetch_size=fetch_size)
        if results is None:
            raise RuntimeError(
                f'address {address} not found in currency {currency}')

        txs = self.list_txs_by_ids(
                currency,
                [row['tx_id'] for row in results.current_rows])
        for (row, tx) in zip(results.current_rows, txs):
            row['tx_hash'] = tx['tx_hash']
            row['height'] = tx['block_id']
            row['timestamp'] = tx['timestamp']

        return results.current_rows, to_hex(results.paging_state)

    # @Timer(text="Timer: get_addresses_by_ids {:.2f}")
    def get_addresses_by_ids(self, currency, address_ids, address_only=False):
        params = [(self.get_id_group(currency, address_id),
                   address_id) for address_id in address_ids]
        fields = 'address' if address_only else '*'
        query = (f"SELECT {fields} FROM address WHERE "
                 "address_id_group = %s and address_id = %s")
        result = self.concurrent_with_args(currency, 'transformed', query, params, use_dict_factory=True)
        if currency != 'eth':
            return result

        for row in result:
            row['address'] = eth_address_to_hex(row['address'])

        return result

    # @Timer(text="Timer: get_address_id {:.2f}")
    def get_address_id(self, currency, address):
        prefix = self.scrub_prefix(currency, address)
        table = "address_by_address_prefix"
        if currency == 'eth':
            address = eth_address_from_hex(address)
            table = "address_ids_by_address_prefix"
            prefix = prefix.upper()
        query = (
            f"SELECT address_id FROM {table} "
            "WHERE address_prefix = %s AND address = %s")
        prefix_length = self.get_prefix_lengths(currency)['address']
        result = self.execute(currency, 'transformed',
            query, [prefix[:prefix_length], address])
        return result.one()['address_id'] if result else None

    # @Timer(text="Timer: get_address_id_id_group {:.2f}")
    def get_address_id_id_group(self, currency, address):
        address_id = self.get_address_id(currency, address)
        if not address_id:
            raise RuntimeError("Address {} not found in currency {}"
                               .format(address, currency))
        id_group = self.get_id_group(currency, address_id)
        return address_id, id_group

    def get_id_group(self, keyspace, id_):
        return floor(int(id_) / self.parameters[keyspace]['bucket_size'])

    def get_block_id_group(self, keyspace, id_):
        return floor(int(id_) / self.parameters[keyspace]['block_bucket_size'])

    def get_tx_id_group(self, keyspace, id_):
        return floor(int(id_) / self.parameters[keyspace]['tx_bucket_size'])

    # @Timer(text="Timer: get_address {:.2f}")
    def get_address(self, currency, address):
        address_id, address_id_group = \
            self.get_address_id_id_group(currency, address)
        query = ("SELECT * FROM address WHERE address_id = %s"
                 " AND address_id_group = %s")
        result = self.execute(currency, 'transformed', query, [address_id, address_id_group], use_dict_factory=True)
        if not result:
            return None

        result = result.one()

        return self.finish_addresses(currency, [result])[0]

    # @Timer(text="Timer: list_tags_by_address {:.2f}")
    def list_tags_by_address(self, currency, address):
        address_id, address_id_group = \
            self.get_address_id_id_group(currency, address)

        query = ("SELECT * FROM address_tags WHERE address_id = %s "
                 "and address_id_group = %s")
        results = self.execute(currency, 'transformed', query, [address_id, address_id_group])
        if results is None:
            return []
        for tag in results.current_rows:
            tag['address'] = address
        return results.current_rows

    @eth
    # @Timer(text="Timer: get_address_entity_id {:.2f}")
    def get_address_entity_id(self, currency, address):
        address_id, address_id_group = \
            self.get_address_id_id_group(currency, address)

        query = "SELECT cluster_id FROM address WHERE " \
                "address_id_group = %s AND address_id = %s "
        result = self.execute(currency, 'transformed', query, [address_id_group, address_id])
        if not result:
            return None
        return result.one()['cluster_id']

    @eth
    # @Timer(text="Timer: list_address_links {:.2f}")
    def list_address_links(self, currency, address, neighbor):

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
        results = self.execute(currency, 'transformed', query, [address_id_group, address_id,
                                          neighbor_id])
        if not results.current_rows:
            return []

        txs = results.current_rows[0]['tx_list']
        query = "SELECT * FROM address_transactions WHERE " \
                "address_id_group = %s AND address_id = %s AND " \
                "tx_id IN %s"
        results1 = self.execute(currency, 'transformed', query, [address_id_group, address_id,
                                           ValueSequence(txs)])
        results2 = self.execute(currency, 'transformed', query, [neighbor_id_group, neighbor_id,
                                           ValueSequence(txs)])

        if not results1.current_rows or not results2.current_rows:
            return []

        links = dict()
        for row in results1.current_rows:
            index = row['tx_id']
            links[index] = dict()
            links[index]['input_value'] = row['value']
        for row in results2.current_rows:
            index = row['tx_id']
            links[index]['output_value'] = row['value']

        for row in self.list_txs_by_ids(currency, txs):
            links[row['tx_id']]['tx_hash'] = row['tx_hash']
            links[row['tx_id']]['height'] = row['block_id']
            links[row['tx_id']]['timestamp'] = row['timestamp']

        return links.values()

    # @Timer(text="Timer: list_matching_addresses {:.2f}")
    def list_matching_addresses(self, currency, expression):
        prefix_lengths = self.get_prefix_lengths(currency)
        if len(expression) < prefix_lengths['address']:
            return []
        table = "address_by_address_prefix"
        norm = identity
        prefix = self.scrub_prefix(currency, expression)
        prefix = prefix[:prefix_lengths['address']]
        if currency == 'eth':
            # eth addresses are case insensitive
            expression = expression.lower()
            table = "address_ids_by_address_prefix"
            norm = eth_address_to_hex
            prefix = prefix.upper()
        query = f"SELECT address FROM {table} WHERE address_prefix = %s"
        result = None
        paging_state = None
        rows = []
        while result is None or paging_state is not None:
            result = self.execute(currency, 'transformed',
                        query,
                        [prefix],
                        paging_state=paging_state, fetch_size=SEARCH_PAGE_SIZE)
            rows += [norm(row['address']) for row in result
                     if norm(row['address']).startswith(expression)]
        return rows

    @eth
    # @Timer(text="Timer: list_entity_tags_by_entity {:.2f}")
    def list_entity_tags_by_entity(self, currency, entity):
        entity = int(entity)
        group = self.get_id_group(currency, entity)
        query = ("SELECT * FROM cluster_tags "
                 "WHERE cluster_id_group = %s and cluster_id = %s")
        results = self.execute(currency, 'transformed', query, [group, entity])

        if results is None:
            return []
        return results.current_rows

    @eth
    # @Timer(text="Timer: list_address_tags_by_entity {:.2f}")
    def list_address_tags_by_entity(self, currency, entity):
        entity = int(entity)
        group = self.get_id_group(currency, entity)
        query = ("SELECT * FROM cluster_address_tags "
                 "WHERE cluster_id_group = %s and cluster_id = %s")
        results = self.execute(currency, 'transformed', query, [group, entity], use_dict_factory=True)

        if results is None:
            return []
        ids = [row['address_id'] for row in results.current_rows]
        addresses = self.get_addresses_by_ids(currency, ids, True)
        for (row, address) in zip(results.current_rows, addresses):
            row['address'] = address['address']
        return results.current_rows

    @eth
    # @Timer(text="Timer: get_entity {:.2f}")
    def get_entity(self, currency, entity):
        entity_id_group = self.get_id_group(currency, entity)
        entity = int(entity)
        query = ("SELECT * FROM cluster "
                 "WHERE cluster_id_group = %s AND cluster_id = %s ")
        result = self.execute(currency, 'transformed', query, [entity_id_group, entity], use_dict_factory=True)
        if not result:
            return None
        result = result.one()
        return self.finish_entities(currency, [result])[0]

    @eth
    # @Timer(text="Timer: list_entities {:.2f}")
    def list_entities(self, currency, ids, page=None, pagesize=None,
                      fields=['*']):
        fetch_size = min(pagesize or SMALL_PAGE_SIZE, SMALL_PAGE_SIZE)
        paging_state = from_hex(page)
        flds = ','.join(fields)
        query = f"SELECT {flds} FROM cluster"
        has_ids = isinstance(ids, list)
        if has_ids:
            query += " WHERE cluster_id_group = %s AND cluster_id = %s"
            params = [[self.get_id_group(currency, id),
                       id] for id in ids]
            result = self.concurrent_with_args(currency, 'transformed', query, params, use_dict_factory=True)
            paging_state = None
        else:
            result = self.execute(currency, 'transformed', query, paging_state=paging_state, use_dict_factory=True, fetch_size=fetch_size)
            paging_state = result.paging_state
            result = result.current_rows

        with_txs = '*' in fields \
            or 'first_tx_id' in fields \
            or 'last_tx_id' in fields
        return self.finish_entities(currency, result, with_txs),\
            to_hex(paging_state)

    @eth
    # @Timer(text="Timer: list_entity_addresses {:.2f}")
    def list_entity_addresses(self, currency, entity, page=None,
                              pagesize=None):
        paging_state = from_hex(page)
        entity_id_group = self.get_id_group(currency, entity)
        entity = int(entity)
        query = ("SELECT address_id FROM cluster_addresses "
                 "WHERE cluster_id_group = %s AND cluster_id = %s")
        fetch_size = min(pagesize or BIG_PAGE_SIZE, BIG_PAGE_SIZE)
        results = self.execute(currency, 'transformed', query, [entity_id_group, entity],
                                  paging_state=paging_state, use_dict_factory=True, fetch_size=fetch_size)
        if results is None:
            return []

        params = [(self.get_id_group(currency, row['address_id']),
                   row['address_id']) for row in results.current_rows]
        query = "SELECT * FROM address WHERE " \
                "address_id_group = %s and address_id = %s"
        result = self.concurrent_with_args(currency, 'transformed', query, params, use_dict_factory=True)

        return self.finish_addresses(currency, result), \
            to_hex(results.paging_state)

    # @Timer(text="Timer: list_neighbors {:.2f}")
    def list_neighbors(self, currency, id, is_outgoing, node_type,
                       targets, include_labels, page, pagesize):
        orig_node_type = node_type
        if node_type == 'address':
            id = self.get_address_id(currency, id)
        elif node_type == 'entity':
            id = int(id)
            node_type = 'cluster'
            if currency == 'eth':
                node_type = 'address'

        if is_outgoing:
            direction, this, that = ('outgoing', 'src', 'dst')
        else:
            direction, this, that = ('incoming', 'dst', 'src')

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

        basequery = (f"SELECT * FROM {node_type}_{direction}_relations WHERE "
                     f"{this}_{node_type}_id_group = %s AND "
                     f"{this}_{node_type}_id = %s {sec_condition}")
        if has_targets:
            if len(targets) == 0:
                return None

            query = basequery.replace('*', f'{that}_{node_type}_id')
            targets = ','.join(map(str, targets))
            query += f' AND {that}_{node_type}_id in ({targets})'
        else:
            query = basequery
        fetch_size = min(pagesize or BIG_PAGE_SIZE, BIG_PAGE_SIZE)
        paging_state = from_hex(page)
        results = self.execute(currency, 'transformed', query, parameters,
                                  paging_state=paging_state, use_dict_factory=True, fetch_size=fetch_size)
        paging_state = results.paging_state
        results = results.current_rows
        if has_targets:
            params = []
            query = basequery + f" AND {that}_{node_type}_id = %s"
            for row in results:
                p = parameters.copy()
                p.append(row[f'{that}_{node_type}_id'])
                params.append(p)
            results = self.concurrent_with_args(currency, 'transformed', query, params, use_dict_factory=True)

        if orig_node_type == 'entity' and currency == 'eth':
            for neighbor in results:
                neighbor[that + '_cluster_id'] = neighbor[that + '_address_id']

        if orig_node_type == 'address':
            ids = [row[that+'_address_id'] for row in results]
            addresses = self.get_addresses_by_ids(currency, ids, False)
            for (row, address) in zip(results, addresses):
                row[f'{that}_address'] = address['address']
                row['total_received'] = address['total_received']
                row['total_spent'] = address['total_spent']
        else:
            ids = [row[that+'_cluster_id'] for row in results]
            entities, _ = self.list_entities(currency, ids, fields=[
                                            'cluster_id',
                                            'total_received',
                                            'total_spent'])
            for (row, entity) in zip(results, entities):
                row[f'{that}_entity'] = entity['cluster_id']
                row['total_received'] = entity['total_received']
                row['total_spent'] = entity['total_spent']

        field = 'value' if currency == 'eth' else 'estimated_value'
        for neighbor in results:
            neighbor['value'] = \
                self.markup_currency(currency, neighbor[field])

        if include_labels:
            self.include_labels(currency, node_type, that, results)

        return results, to_hex(paging_state)

    @eth
    # @Timer(text="Timer: include_labels {:.2f}")
    def include_labels(self, currency, node_type, that, nodes):
        for node in nodes:
            node['labels'] = []
        if node_type == 'cluster':
            key = f'{that}_cluster_id'
            params = [(self.get_id_group(currency, row[key]), row[key])
                      for row in nodes if row[f'has_{that}_labels']]
            query = ('select cluster_id, label from cluster_tags where '
                     'cluster_id_group = %s and cluster_id = %s')
            results = self.concurrent_with_args(
                currency, 'transformed', query, params, one=False)
            i = 0
            for result in results:
                while nodes[i][key] != result.one()['cluster_id']:
                    i += 1
                nodes[i]['labels'] = [row['label'] for row in result]
        else:
            key = f'{that}_address_id'
            params = [[row[key], self.get_id_group(currency, row[key])]
                      for row in nodes if row[f'has_{that}_labels']]
            query = ('select address_id, label from address_tags where '
                     'address_id = %s and address_id_group = %s')
            results = self.concurrent_with_args(
                currency, 'transformed', query, params, one=False)
            i = 0
            for result in results:
                while nodes[i][key] != result.one()['address_id']:
                    i += 1
                nodes[i]['labels'] = [row['label'] for row in result]

        return nodes

    # @Timer(text="Timer: list_address_tags {:.2f}")
    def list_address_tags(self, currency, label):
        prefix_length = self.get_prefix_lengths(currency)['label']
        label_norm_prefix = label[:prefix_length]
        query = ("SELECT * FROM address_tag_by_label WHERE "
                 "label_norm_prefix = %s and label_norm = %s")
        rows = self.execute(currency, 'transformed', query, [label_norm_prefix, label])
        if rows is None:
            return []
        return rows

    @eth
    # @Timer(text="Timer: list_entity_tags {:.2f}")
    def list_entity_tags(self, currency, label):
        prefix_length = self.get_prefix_lengths(currency)['label']
        label_norm_prefix = label[:prefix_length]
        query = ("SELECT * FROM cluster_tag_by_label WHERE "
                 "label_norm_prefix = %s and label_norm = %s")
        rows = self.execute(currency, 'transformed', query, [label_norm_prefix, label])
        if rows is None:
            return []
        return rows

    # @Timer(text="Timer: list_labels {:.2f}")
    def list_labels(self, currency, expression_norm):
        prefix_lengths = self.get_prefix_lengths(currency)
        if len(expression_norm) < prefix_lengths['label']:
            return []
        expression_norm_prefix = expression_norm[:prefix_lengths['label']]
        query = ("SELECT label, label_norm, currency FROM address_tag_by_label"
                 " WHERE label_norm_prefix = %s GROUP BY label_norm_prefix, "
                 "label_norm")
        result = self.execute(currency, 'transformed', query, [expression_norm_prefix])
        if result is None:
            return []
        return result

    # @Timer(text="Timer: list_concepts {:.2f}")
    def list_concepts(self, taxonomy):
        query = "SELECT * FROM concept_by_taxonomy_id WHERE taxonomy = %s"
        rows = self.execute(None, 'tagpacks', query, [taxonomy])
        if rows is None:
            return []
        return rows

    # @Timer(text="Timer: list_taxonomies {:.2f}")
    def list_taxonomies(self, ):
        query = "SELECT * FROM taxonomy_by_key LIMIT 100"
        rows = self.execute(None, 'tagpacks', query)
        if rows is None:
            return []
        return rows

    @eth
    # @Timer(text="Timer: get_tx {:.2f}")
    def get_tx(self, currency, tx_hash):
        result = self.list_txs_by_hashes(currency, [tx_hash])
        if result:
            return result[0]

    # @Timer(text="Timer: list_txs {:.2f}")
    def list_txs(self, currency, page=None):

        paging_state = from_hex(page)
        query = "SELECT * FROM transaction"
        results = self.execute(currency, 'raw', query, paging_state=paging_state)

        if results is None:
            return [], None
        return results.current_rows, to_hex(results.paging_state)

    @new
    # @Timer(text="Timer: list_matching_txs {:.2f}")
    def list_matching_txs(self, currency, expression):
        prefix_lengths = self.get_prefix_lengths(currency)
        if len(expression) < prefix_lengths['tx']:
            return []
        query = ('SELECT tx_hash from transaction_by_tx_prefix where '
                 'tx_prefix=%s')
        results = self.execute(currency, 'raw', query, [expression[:prefix_lengths['tx']]])
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
    # @Timer(text="Timer: list_txs_by_hashes {:.2f}")
    def list_txs_by_hashes(self, currency, hashes):
        prefix = self.get_prefix_lengths(currency)
        params = [[hash[:prefix['tx']],
                   bytearray.fromhex(hash)]
                  for hash in hashes]
        statement = ('SELECT tx_id from transaction_by_tx_prefix where '
                     'tx_prefix=%s and tx_hash=%s')
        result = self.concurrent_with_args(currency, 'raw', statement, params)
        ids = [tx['tx_id'] for tx in result]
        return self.list_txs_by_ids(currency, ids)

    @eth
    # @Timer(text="Timer: list_txs_by_ids {:.2f}")
    def list_txs_by_ids(self, currency, ids):
        params = [[self.get_tx_id_group(currency, id), id] for id in ids]
        statement = ('SELECT * FROM transaction WHERE '
                     'tx_id_group = %s and tx_id = %s')
        return self.concurrent_with_args(currency, 'raw', statement, params)

    # @Timer(text="Timer: list_addresses {:.2f}")
    def list_addresses(self, currency, ids=None, page=None, pagesize=None):
        has_ids = isinstance(ids, list)
        if has_ids:
            prefix_length = self.get_prefix_lengths(currency)['address']
            params = [[self.scrub_prefix(currency, id)[:prefix_length],
                       id] for id in ids]
            table = 'address_by_address_prefix'
            if currency == 'eth':
                table = 'address_ids_by_address_prefix'
                params = [[param[0].upper(),
                           eth_address_from_hex(param[1])] for param in params]
            query = (f"SELECT address_id FROM {table}"
                     " WHERE address_prefix = %s AND address = %s")
            ids = self.concurrent_with_args(currency, 'transformed', query, params)
            query = ("SELECT * FROM address WHERE "
                     "address_id_group = %s AND address_id = %s")
            params = [[self.get_id_group(currency, row['address_id']),
                       row['address_id']] for row in ids]
            result = self.concurrent_with_args(currency, 'transformed', query, params, use_dict_factory=True)
            paging_state = None
        else:
            query = "SELECT * FROM address"
            fetch_size = min(pagesize or SMALL_PAGE_SIZE, SMALL_PAGE_SIZE)
            result = self.execute(currency, 'transformed', query, paging_state=from_hex(page), use_dict_factory=True, fetch_size=fetch_size)
            paging_state = result.paging_state
            result = result.current_rows

        result = self.finish_addresses(currency, result)
        if currency != 'eth':
            return result, to_hex(paging_state)

        return result, to_hex(paging_state)

    def finish_entities(self, currency, rows, with_txs=True):
        return self.finish_addresses(currency, rows, with_txs)

    @eth
    def finish_addresses(self, currency, rows, with_txs=True):
        ids = []
        for row in rows:
            row['total_received'] = \
                self.markup_currency(currency, row['total_received'])
            row['total_spent'] = \
                self.markup_currency(currency, row['total_spent'])

            if not with_txs:
                continue

            ids.append(row['first_tx_id'])
            ids.append(row['last_tx_id'])

        if not with_txs:
            return rows

        TxSummary = namedtuple('TxSummary', ['height', 'timestamp', 'tx_hash'])
        txs = self.list_txs_by_ids(currency, ids)

        for i, tx in enumerate(txs):
            row = rows[i//2]
            if i % 2 == 0:
                row['first_tx'] = TxSummary(
                    tx_hash=tx['tx_hash'],
                    timestamp=tx['timestamp'],
                    height=tx['block_id'])
            else:
                row['last_tx'] = TxSummary(
                    tx_hash=tx['tx_hash'],
                    timestamp=tx['timestamp'],
                    height=tx['block_id'])

        return rows

#####################
# ETHEREUM VARIANTS #
#####################

    # @Timer(text="Timer: get_currency_statistics_eth {:.2f}")
    def get_currency_statistics_eth(self, currency):
        query = "SELECT * FROM summary_statistics LIMIT 1"
        result = self.execute(currency, 'transformed', query).one()
        result['no_clusters'] = 0
        return result

    def scrub_prefix_eth(self, currency, expression):
        # remove 0x prefix
        return expression[2:]

    # @Timer(text="Timer: get_block_eth {:.2f}")
    def get_block_eth(self, currency, height):
        block_group = self.get_block_id_group(currency, height)
        query = ("SELECT * FROM block WHERE block_id_group = %s and"
                 " block_id = %s")
        return self.execute(currency, 'raw', query, [block_group, height]).one()

    # entity = address_id
    # @Timer(text="Timer: get_entity_eth {:.2f}")
    def get_entity_eth(self, currency, entity):
        # mockup entity by address
        id_group = self.get_id_group(currency, entity)
        query = (
            "SELECT * FROM address WHERE "
            "address_id_group = %s AND address_id = %s")
        result = self.execute(currency, 'transformed',
            query, [id_group, entity], use_dict_factory=True)
        if not result:
            return None

        result = result.one()
        entity = self.finish_addresses(currency, [result])[0]
        entity['cluster_id'] = entity['address_id']
        entity['no_addresses'] = 1
        entity.pop('address', None)
        return entity

    # @Timer(text="Timer: list_entities_eth {:.2f}")
    def list_entities_eth(self, currency, ids, page=None, pagesize=None,
                          fields=['*']):
        flds = ','.join(fields)
        query = f"SELECT {flds} FROM address"
        has_ids = isinstance(ids, list)
        if has_ids:
            query += " WHERE address_id_group = %s AND address_id = %s"
            params = [[self.get_id_group(currency, id),
                       id] for id in ids]
            result = self.concurrent_with_args(currency, 'transformed', query, params, use_dict_factory=True)
            paging_state = None
        else:
            fetch_size = min(pagesize or SMALL_PAGE_SIZE, SMALL_PAGE_SIZE)
            result = self.execute(currency, 'transformed', query, paging_state=from_hex(page), use_dict_factory=True, fetch_size=fetch_size)
            paging_state = result.paging_state
            result = result.current_rows

        with_txs = '*' in fields \
            or 'first_tx_id' in fields \
            or 'last_tx_id' in fields
        result = self.finish_addresses(currency, result, with_txs)

        for address in result:
            address['cluster_id'] = address['address_id']
            address['no_addresses'] = 1
        return result, to_hex(paging_state)

    def list_entity_tags_by_entity_eth(self, currency, entity):
        return []

    # @Timer(text="Timer: list_address_tags_by_entity_eth {:.2f}")
    def list_address_tags_by_entity_eth(self, currency, entity):
        query = ("SELECT address FROM address "
                 "WHERE address_id_group=%s and address_id=%s")
        id_id_group = [self.get_id_group(currency, entity), entity]
        result = self.execute(currency, 'transformed', query, id_id_group)
        if result is None or result.one() is None:
            return None
        address = result.one()['address']
        query = ("SELECT * FROM address_tags WHERE address_id_group = %s "
                 "and address_id = %s")
        results = self.execute(currency, 'transformed', query, id_id_group, use_dict_factory=True)
        if results is None:
            return []
        for tag in results.current_rows:
            tag['address'] = eth_address_to_hex(address)
        return results.current_rows

    # @Timer(text="Timer: get_address_entity_id_eth {:.2f}")
    def get_address_entity_id_eth(self, currency, address):
        return self.get_address_id(currency, address)

    # @Timer(text="Timer: list_block_txs_eth {:.2f}")
    def list_block_txs_eth(self, currency, height):
        height_group = self.get_block_id_group(currency, height)
        query = ("SELECT txs FROM block_transactions WHERE "
                 "block_id_group = %s and block_id = %s")
        result = self.execute(currency, 'transformed', query, [height_group, height])
        if result is None:
            raise RuntimeError(
                    f'block {height} not found in currency {currency}')
        return self.list_txs_by_ids(currency, result.one()['txs'])

    # @Timer(text="Timer: get_secondary_id_group_eth {:.2f}")
    def get_secondary_id_group_eth(self, table, id_group):
        column_prefix = ''
        if table == 'address_incoming_relations':
            column_prefix = 'dst_'
        elif table == 'address_outgoing_relations':
            column_prefix = 'src_'

        query = (f"SELECT max_secondary_id FROM {table}_"
                 f"secondary_ids WHERE {column_prefix}address_id_group = %s")
        result = self.execute('eth', 'transformed', query, [id_group])
        return 0 if result.one() is None else \
            result.one()['max_secondary_id']

    # @Timer(text="Timer: list_address_txs_eth {:.2f}")
    def list_address_txs_eth(self, currency, address,
                             page=None, pagesize=None):
        paging_state = from_hex(page)
        address_id, id_group = self.get_address_id_id_group(currency, address)
        secondary_id_group = \
            self.get_secondary_id_group_eth('address_transactions', id_group)
        sec_in = self.sec_in(secondary_id_group)
        query = ("SELECT transaction_id, value FROM address_transactions "
                 "WHERE address_id_group = %s and "
                 f"address_id_secondary_group in {sec_in}"
                 " and address_id = %s")
        fetch_size = min(pagesize or BIG_PAGE_SIZE, BIG_PAGE_SIZE)
        result = self.execute(currency, 'transformed', query,
                                 [id_group,
                                  address_id],
                                 paging_state=paging_state, use_dict_factory=True, fetch_size=fetch_size)
        if result is None:
            raise RuntimeError(
                    f'address {address} not found in currency {currency}')
        txs = [row['transaction_id'] for row in result.current_rows]
        paging_state = result.paging_state
        for (row1, row2) in zip(
                result.current_rows,
                self.list_txs_by_ids(currency, txs)):
            row1['tx_hash'] = row2['hash']
            row1['height'] = row2['block_id']
            row1['timestamp'] = row2['block_timestamp']
        return result.current_rows, to_hex(paging_state)

    # @Timer(text="Timer: list_txs_by_ids_eth {:.2f}")
    def list_txs_by_ids_eth(self, currency, ids):
        params = [[self.get_id_group(currency, id), id] for id in ids]
        statement = (
            'SELECT transaction from transaction_ids_by_transaction_id_group'
            ' where transaction_id_group = %s and transaction_id = %s')
        result = self.concurrent_with_args(currency, 'transformed', statement, params)
        return self.list_txs_by_hashes(currency,
                                       [row['transaction'] for row in result])

    # @Timer(text="Timer: list_txs_by_hashes_eth {:.2f}")
    def list_txs_by_hashes_eth(self, currency, hashes):
        prefix = self.get_prefix_lengths(currency)
        params = [[hash.hex()[:prefix['tx']], hash]
                  for hash in hashes]
        statement = (
            'SELECT hash, block_id, block_timestamp, value from '
            'transaction where hash_prefix=%s and hash=%s')
        return self.concurrent_with_args(currency, 'raw', statement, params)

    # @Timer(text="Timer: list_address_links_eth {:.2f}")
    def list_address_links_eth(self, currency, address, neighbor):
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
        result = self.execute(currency, 'transformed', query, [id_group, address_id,
                                             neighbor_id])
        if result is None or result.one() is None:
            return [], None
        txs = result.one()['transaction_ids']
        return self.list_txs_by_ids(currency, txs)

    # @Timer(text="Timer: get_tx_eth {:.2f}")
    def get_tx_eth(self, currency, tx_hash):
        query = (
            'SELECT hash, block_id, block_timestamp, value from '
            'transaction where hash_prefix=%s and hash=%s')
        prefix_length = self.get_prefix_lengths(currency)
        prefix = tx_hash[:prefix_length['tx']]
        result = self.execute(currency, 'raw', query, [prefix, bytearray.fromhex(tx_hash)])
        if result is None:
            return None
        return result.one()

    # @Timer(text="Timer: list_entity_addresses_eth {:.2f}")
    def list_entity_addresses_eth(self, currency, entity, page=None,
                                  pagesize=None):
        address = self.get_addresses_by_ids(currency, [entity])[0]
        if address is None:
            return None
        return self.finish_addresses(currency, [address]), None

    def list_entity_tags_eth(self, currency, label):
        return []

    # @Timer(text="Timer: include_labels_eth {:.2f}")
    def include_labels_eth(self, currency, node_type, that, nodes):
        for node in nodes:
            node['labels'] = []
        if node_type == 'cluster':
            pass
        else:
            key = f'{that}_address_id'
            params = [[row[key],
                       self.get_id_group(currency, row[key])]
                      for row in nodes if row[f'has_{that}_labels']]
            query = ('select address_id, label from address_tags where '
                     'address_id=%s and address_id_group=%s')
            results = self.concurrent_with_args(
                currency, 'transformed', query, params, one=False)
            i = 0
            for result in results:
                while nodes[i][key] != result.one()['address_id']:
                    i += 1
                nodes[i]['labels'] = [row['label'] for row in result]

        return nodes

##################################
# VARIANTS USING NEW DATA SCHEME #
##################################

    def markup_values(self, currency, fiat_values):
        values = []
        for (fiat, curr) in zip(
                fiat_values,
                self.parameters[currency]['fiat_currencies']):
            values.append({'code': curr.lower(), 'value': fiat})
        return values

    def markup_currency(self, currency, values):
        Values = namedtuple('Values', values._fields)
        values = values._asdict()
        values['fiat_values'] = \
            self.markup_values(currency, values['fiat_values'])
        return Values(**values)

    def markup_rates(self, currency, row):
        row['rates'] = self.markup_values(currency, row['fiat_values'])
        return row

    # @Timer(text="Timer: list_matching_txs_new {:.2f}")
    def list_matching_txs_new(self, currency, expression):
        prefix_lengths = self.get_prefix_lengths(currency)
        if len(expression) < prefix_lengths['tx']:
            return []
        query = ('SELECT transaction from transaction_ids_by_transaction_pre'
                 'fix where transaction_prefix = %s')
        prefix = expression[:prefix_lengths['tx']].upper()
        results = self.execute(currency, 'transformed', query, [prefix])
        if results is None:
            return []
        for row in results.current_rows:
            row['tx_hash'] = row['transaction']
        return results.current_rows

    # @Timer(text="Timer: list_tags_new {:.2f}")
    def list_tags_new(self, currency, label):
        prefix_length = self.get_prefix_lengths(currency)['label']
        label_norm_prefix = label[:prefix_length]

        query = ("SELECT * FROM address_tag_by_label WHERE label_norm_prefix"
                 "= %s and label_norm = %s")
        rows = self.execute(currency, 'transformed', query, [label_norm_prefix, label])
        if rows is None:
            return []
        return rows

    def sec_in(self, id):
        return "(" + ','.join(map(str, range(0, id+1))) + ")"

    def finish_addresses_eth(self, currency, rows, with_txs=True):
        ids = []
        for row in rows:
            row['address'] = eth_address_to_hex(row['address'])
            row['cluster_id'] = row['address_id']
            row['total_received'] = \
                self.markup_currency(currency, row['total_received'])
            row['total_spent'] = \
                self.markup_currency(currency, row['total_spent'])
            if not with_txs:
                continue

            ids.append(row['first_tx_id'])
            ids.append(row['last_tx_id'])

        if not with_txs:
            return rows

        TxSummary = namedtuple('TxSummary', ['height', 'timestamp', 'tx_hash'])
        txs = self.list_txs_by_ids(currency, ids)

        for i, tx in enumerate(txs):
            row = rows[i//2]
            if i % 2 == 0:
                row['first_tx'] = TxSummary(
                    height=tx['block_id'],
                    timestamp=tx['block_timestamp'],
                    tx_hash=tx['hash'])
            else:
                row['last_tx'] = TxSummary(
                    height=tx['block_id'],
                    timestamp=tx['block_timestamp'],
                    tx_hash=tx['hash'])
        return rows
