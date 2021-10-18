import re
import time
import asyncio
from collections import namedtuple
from cassandra.cluster import Cluster, NoHostAvailable
from cassandra.query import SimpleStatement, dict_factory
from cassandra.concurrent import execute_concurrent_with_args
from math import floor
from flask import current_app
# from codetiming import Timer

from gsrest.util.exceptions import BadConfigError

SMALL_PAGE_SIZE = 10
BIG_PAGE_SIZE = 10
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


class Result:
    def __init__(self, current_rows, params, paging_state):
        self.current_rows = current_rows
        self.params = params
        self.paging_state = paging_state

    def is_empty(self):
        return self.current_rows is None or not self.current_rows

    def one(self):
        if self.is_empty():
            return None
        return self.current_rows[0]


class Cassandra:
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
        self.connect()
        self.check_keyspace(config['tagpacks'])
        self.parameters = {}
        for currency in config['currencies']:
            self.check_keyspace(config['currencies'][currency]['raw'])
            self.check_keyspace(config['currencies'][currency]['transformed'])
            self.load_parameters(currency)

    def connect(self):
        try:
            self.cluster = Cluster(self.config['nodes'])
            self.session = self.cluster.connect()
            self.session.row_factory = dict_factory
            current_app.logger.info('Connection ready.')
        except NoHostAvailable:
            retry = self.config['retry_interval']
            retry = 5 if retry is None else retry
            current_app.logger.error(
                f'Could not connect. Retrying in {retry} secs.')
            time.sleep(retry)
            self.connect()

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
            result = self.execute(keyspace, kind, query)
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

    def execute(self, currency, keyspace_type, query,
                params=None, paging_state=None, fetch_size=None):
        keyspace = self.get_keyspace_mapping(currency, keyspace_type)
        q = replaceFrom(keyspace, query)
        q = SimpleStatement(q, fetch_size=fetch_size)
        try:
            result = self.session.execute(q, params, paging_state=paging_state)
        except NoHostAvailable:
            self.connect()
            result = self.execute(currency, keyspace_type, query,
                                  params=params,
                                  paging_state=paging_state,
                                  fetch_size=fetch_size)

        return result

    def execute_async(self, currency, keyspace_type, query,
                      params=None, paging_state=None, fetch_size=None):
        keyspace = self.get_keyspace_mapping(currency, keyspace_type)
        q = replaceFrom(keyspace, query)
        q = SimpleStatement(q, fetch_size=fetch_size)
        try:
            response_future = self.session.execute_async(
                q, params,
                paging_state=paging_state)
            loop = asyncio.get_event_loop()
            future = loop.create_future()

            def on_done(result):
                result = Result(current_rows=result,
                                params=params,
                                paging_state=response_future._paging_state)
                loop.call_soon_threadsafe(future.set_result, result)

            def on_err(result):
                loop.call_soon_threadsafe(future.set_exception, result)

            response_future.add_callbacks(on_done, on_err)
            return future
        except NoHostAvailable:
            self.connect()
            return self.execute_async(currency, keyspace_type, query,
                                      params=params,
                                      paging_state=paging_state,
                                      fetch_size=fetch_size)

    async def concurrent_with_args(self, currency, keyspace_type, query,
                                   params, filter_empty=True, one=True,
                                   results_generator=False,
                                   keep_meta=False):
        aws = [self.execute_async(currency, keyspace_type, query, param)
               for param in params]
        results = []
        for result in await asyncio.gather(*aws):
            if filter_empty and result is None:
                continue
            if one:
                o = result.one()
                if not keep_meta:
                    result = o
                else:
                    result.current_rows = [o]
                if o:
                    results.append(result)
                else:
                    if not filter_empty:
                        results.append(result)
                continue
            if not keep_meta:
                results.append(result.current_rows)
            else:
                results.append(result)
        return results
    #TODO: automatic page iteration missing

    @eth
    # @Timer(text="Timer: stats {:.2f}")
    async def get_currency_statistics(self, currency):
        query = "SELECT * FROM summary_statistics LIMIT 1"
        result = await self.execute_async(currency, 'transformed', query)
        return result.one()

    @eth
    # @Timer(text="Timer: get_block {:.2f}")
    async def get_block(self, currency, height):
        query = ("SELECT * FROM block WHERE block_id_group = %s "
                 "AND block_id = %s")
        return (await self.execute_async(
                            currency, 'raw', query,
                            [self.get_block_id_group(currency, height), height]
                            )).one()

    # @Timer(text="Timer: list_blocks {:.2f}")
    async def list_blocks(self, currency, page=None):
        paging_state = from_hex(page)

        query = "SELECT * FROM block"
        results = await self.execute_async(currency, 'raw', query,
                                           paging_state=paging_state)

        return results.current_rows, to_hex(results.paging_state)

    @eth
    async def list_block_txs(self, currency, height):
        height_group = self.get_block_id_group(currency, height)
        query = ("SELECT txs FROM block_transactions WHERE "
                 "block_id_group = %s and block_id = %s")
        result = await self.execute_async(currency, 'raw', query,
                                          [height_group, height])
        if result is None or result.one() is None:
            return None
        txs = [tx.tx_id for tx in result.one()['txs']]
        return await self.list_txs_by_ids(currency, txs)

    # @Timer(text="Timer: get_rates {:.2f}")
    async def get_rates(self, currency, height):
        query = "SELECT * FROM exchange_rates WHERE block_id = %s"
        result = await self.execute_async(currency, 'transformed', query,
                                          [height])
        if result is None:
            return None
        result = result.one()
        return self.markup_rates(currency, result)

    # @Timer(text="Timer: list_rates {:.2f}")
    async def list_rates(self, currency, heights):
        result = await self.concurrent_with_args(
            currency,
            'transformed',
            "SELECT * FROM exchange_rates WHERE block_id = %s",
            [[h] for h in heights])
        for row in result:
            self.markup_rates(currency, row)
        return result

    async def list_address_txs(self, currency, address, page=None,
                               pagesize=None):
        return await self.list_txs_by_node_type(
            currency, 'address', address, page=page, pagesize=pagesize)

    def list_entity_txs(self, currency, entity, page=None,
                        pagesize=None):
        return self.list_txs_by_node_type(
            currency, 'cluster', entity, page=page, pagesize=pagesize)

    @eth
    # @Timer(text="Timer: list_address_txs {:.2f}")
    async def list_txs_by_node_type(self, currency, node_type, id, page=None,
                                    pagesize=None):
        paging_state = from_hex(page)
        if node_type == 'address':
            id, id_group = \
                await self.get_address_id_id_group(currency, id)
        else:
            id_group = self.get_id_group(currency, id)

        query = f"SELECT * FROM {node_type}_transactions " \
                f"WHERE {node_type}_id = %s AND {node_type}_id_group = %s"
        fetch_size = min(pagesize or BIG_PAGE_SIZE, BIG_PAGE_SIZE)
        results = await self.execute_async(currency, 'transformed', query,
                                           [id, id_group],
                                           paging_state=paging_state,
                                           fetch_size=fetch_size)
        if results is None:
            raise RuntimeError(
                f'{node_type} {id} not found in currency {currency}')

        txs = await self.list_txs_by_ids(
                currency,
                [row['tx_id'] for row in results.current_rows],
                filter_empty=False)
        rows = []
        for (row, tx) in zip(results.current_rows, txs):
            if tx is None:
                continue
            row['tx_hash'] = tx['tx_hash']
            row['height'] = tx['block_id']
            row['timestamp'] = tx['timestamp']
            rows.append(row)

        return rows, to_hex(results.paging_state)

    # @Timer(text="Timer: get_addresses_by_ids {:.2f}")
    async def get_addresses_by_ids(self, currency, address_ids,
                                   address_only=False):
        params = [(self.get_id_group(currency, address_id),
                   address_id) for address_id in address_ids]
        fields = 'address' if address_only else '*'
        query = (f"SELECT {fields} FROM address WHERE "
                 "address_id_group = %s and address_id = %s")
        result = await self.concurrent_with_args(
                    currency, 'transformed', query, params)

        for row in result:
            if currency == 'eth':
                row['address'] = \
                    eth_address_to_hex(row['address'])
        return result

    # @Timer(text="Timer: get_address_id {:.2f}")
    async def get_address_id(self, currency, address):
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
        result = await self.execute_async(
                              currency, 'transformed',
                              query, [prefix[:prefix_length], address])
        return result.one()['address_id'] if result else None

    # @Timer(text="Timer: get_address_id_id_group {:.2f}")
    async def get_address_id_id_group(self, currency, address):
        address_id = await self.get_address_id(currency, address)
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
    async def get_address(self, currency, address):
        address_id, address_id_group = \
            await self.get_address_id_id_group(currency, address)
        query = ("SELECT * FROM address WHERE address_id = %s"
                 " AND address_id_group = %s")
        result = await self.execute_async(currency, 'transformed', query,
                                          [address_id, address_id_group])
        if not result:
            return None

        result = result.one()

        return await self.finish_address(currency, result)

    # @Timer(text="Timer: list_tags_by_address {:.2f}")
    async def list_tags_by_address(self, currency, address):
        address_id, address_id_group = \
            await self.get_address_id_id_group(currency, address)

        query = ("SELECT * FROM address_tags WHERE address_id = %s "
                 "and address_id_group = %s")
        results = await self.execute_async(currency, 'transformed', query,
                                           [address_id, address_id_group])
        if results is None:
            return []
        for tag in results.current_rows:
            tag['address'] = address
        return results.current_rows

    @eth
    # @Timer(text="Timer: get_address_entity_id {:.2f}")
    async def get_address_entity_id(self, currency, address):
        address_id, address_id_group = \
            await self.get_address_id_id_group(currency, address)

        query = "SELECT cluster_id FROM address WHERE " \
                "address_id_group = %s AND address_id = %s "
        result = await self.execute_async(currency, 'transformed', query,
                                          [address_id_group, address_id])
        result = result.one()
        if not result:
            return None
        return result['cluster_id']

    def list_address_links(self, currency, address, neighbor,
                           page=None, pagesize=None):
        return self.list_links(currency, 'address', address, neighbor,
                               page=page, pagesize=pagesize)

    def list_entity_links(self, currency, address, neighbor,
                          page=None, pagesize=None):
        return self.list_links(currency, 'cluster', address, neighbor,
                               page=page, pagesize=pagesize)

    @eth
    def list_links(self, currency, node_type, id, neighbor,
                   page=None, pagesize=None):
        if node_type == 'address':
            id, id_group = \
                self.get_address_id_id_group(currency, id)
            neighbor_id, neighbor_id_group = \
                self.get_address_id_id_group(currency, neighbor)
        else:
            id_group = self.get_id_group(currency, id)
            neighbor_id = neighbor
            neighbor_id_group = self.get_id_group(currency, neighbor_id)

        if id is None or neighbor_id is None:
            raise RuntimeError("Links between {} and {} not found"
                               .format(id, neighbor))

        query = f"SELECT no_{{direction}}_txs FROM {node_type} " \
                f"WHERE {node_type}_id_group = %s AND {node_type}_id = %s"

        no_outgoing_txs = self.execute(
            currency, 'transformed', query.format(direction='outgoing'),
            [id_group, id]
            ).one()

        if no_outgoing_txs is None:
            return [], None

        no_outgoing_txs = no_outgoing_txs['no_outgoing_txs']

        no_incoming_txs = self.execute(
            currency, 'transformed', query.format(direction='incoming'),
            [neighbor_id_group, neighbor_id]
            ).one()

        if no_incoming_txs is None:
            return [], None

        no_incoming_txs = no_incoming_txs['no_incoming_txs']

        isOutgoing = no_outgoing_txs < no_incoming_txs

        first_id_group, first_id, second_id_group, second_id, \
            first_value, second_value = \
            (id_group, id, neighbor_id_group, neighbor_id,
             'input_value', 'output_value') \
            if isOutgoing \
            else (neighbor_id_group, neighbor_id, id_group, id,
                  'output_value', 'input_value')

        first_query = f"SELECT * FROM {node_type}_transactions WHERE " \
                      f"{node_type}_id_group = %s AND {node_type}_id = %s" \

        second_query = first_query + " AND tx_id = %s"

        fetch_size = min(pagesize or SMALL_PAGE_SIZE, SMALL_PAGE_SIZE)
        paging_state = from_hex(page)
        has_more_pages = True
        count = 0
        links = dict()
        tx_ids = []
        while count < fetch_size and has_more_pages:
            results1 = self.execute(currency, 'transformed', first_query,
                                    [first_id_group, first_id],
                                    paging_state=paging_state,
                                    fetch_size=fetch_size)

            if not results1.current_rows:
                return [], None

            has_more_pages = results1.has_more_pages
            paging_state = results1.paging_state

            params = [[second_id_group, second_id, row['tx_id']]
                      for row in results1.current_rows
                      if row['value'] < 0 and isOutgoing or
                      not isOutgoing and row['value'] > 0]
            results2 = self.concurrent_with_args(
                currency, 'transformed', second_query, params)

            for row in results2:
                index = row['tx_id']
                tx_ids.append(index)
                count += 1
                links[index] = dict()
                links[index][second_value] = row['value']
            for row in results1.current_rows:
                index = row['tx_id']
                if index not in links:
                    continue
                links[index][first_value] = row['value']

        for row in self.list_txs_by_ids(currency, tx_ids):
            links[row['tx_id']]['tx_hash'] = row['tx_hash']
            links[row['tx_id']]['height'] = row['block_id']
            links[row['tx_id']]['timestamp'] = row['timestamp']

        return list(links.values()), to_hex(paging_state)

    async def list_matching_addresses(self, currency, expression):
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
            result = await self.execute_async(
                        currency, 'transformed', query, [prefix],
                        paging_state=paging_state,
                        fetch_size=SEARCH_PAGE_SIZE)
            if result.is_empty():
                break
            rows += [norm(row['address']) for row in result.current_rows
                     if norm(row['address']).startswith(expression)]
            paging_state = result.paging_state
        return rows

    @eth
    # @Timer(text="Timer: list_entity_tags_by_entity {:.2f}")
    async def list_entity_tags_by_entity(self, currency, entity):
        entity = int(entity)
        group = self.get_id_group(currency, entity)
        query = ("SELECT * FROM cluster_tags "
                 "WHERE cluster_id_group = %s and cluster_id = %s")
        results = await self.execute_async(currency, 'transformed', query,
                                           [group, entity])

        if results is None:
            return []
        return results.current_rows

    @eth
    # @Timer(text="Timer: list_address_tags_by_entity {:.2f}")
    async def list_address_tags_by_entity(self, currency, entity):
        entity = int(entity)
        group = self.get_id_group(currency, entity)
        query = ("SELECT * FROM cluster_address_tags "
                 "WHERE cluster_id_group = %s and cluster_id = %s")
        results = await self.execute_async(currency, 'transformed', query,
                                           [group, entity])

        if results is None:
            return []
        ids = [row['address_id'] for row in results.current_rows]
        addresses = await self.get_addresses_by_ids(currency, ids, True)
        for (row, address) in zip(results.current_rows, addresses):
            row['address'] = address['address']
        return results.current_rows

    @eth
    # @Timer(text="Timer: get_entity {:.2f}")
    async def get_entity(self, currency, entity):
        entity_id_group = self.get_id_group(currency, entity)
        entity = int(entity)
        query = ("SELECT * FROM cluster "
                 "WHERE cluster_id_group = %s AND cluster_id = %s ")
        result = await self.execute_async(currency, 'transformed', query,
                                          [entity_id_group, entity])
        result = result.one()
        if not result:
            return None
        return (await self.finish_entities(currency, [result]))[0]

    @eth
    # @Timer(text="Timer: list_entities {:.2f}")
    async def list_entities(self, currency, ids, page=None, pagesize=None,
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
            result = await self.concurrent_with_args(
                        currency, 'transformed', query, params)
            paging_state = None
        else:
            result = await self.execute_async(currency, 'transformed', query,
                                              paging_state=paging_state,
                                              fetch_size=fetch_size)
            paging_state = result.paging_state
            result = result.current_rows

        with_txs = '*' in fields \
            or 'first_tx_id' in fields \
            or 'last_tx_id' in fields
        return await self.finish_entities(currency, result, with_txs),\
            to_hex(paging_state)

    @eth
    # @Timer(text="Timer: list_entity_addresses {:.2f}")
    async def list_entity_addresses(self, currency, entity, page=None,
                                    pagesize=None):
        paging_state = from_hex(page)
        entity_id_group = self.get_id_group(currency, entity)
        entity = int(entity)
        query = ("SELECT address_id FROM cluster_addresses "
                 "WHERE cluster_id_group = %s AND cluster_id = %s")
        fetch_size = min(pagesize or BIG_PAGE_SIZE, BIG_PAGE_SIZE)
        results = await self.execute_async(
                               currency, 'transformed', query,
                               [entity_id_group, entity],
                               paging_state=paging_state,
                               fetch_size=fetch_size)
        if results is None:
            return []

        params = [(self.get_id_group(currency, row['address_id']),
                   row['address_id']) for row in results.current_rows]
        query = "SELECT * FROM address WHERE " \
                "address_id_group = %s and address_id = %s"
        result = self.concurrent_with_args(currency, 'transformed', query,
                                           params, results_generator=True)
        addresses = []
        async for row in result:
            addresses.append(await self.finish_address(currency, row))

        return addresses, to_hex(results.paging_state)

    # @Timer(text="Timer: list_neighbors {:.2f}")
    async def list_neighbors(self, currency, id, is_outgoing, node_type,
                             targets, include_labels, page, pagesize):
        orig_node_type = node_type
        if node_type == 'address':
            id = await self.get_address_id(currency, id)
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
                await self.get_id_secondary_group_eth(
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
        results = await self.execute_async(currency, 'transformed', query,
                                           parameters,
                                           paging_state=paging_state,
                                           fetch_size=fetch_size)
        paging_state = results.paging_state
        results = results.current_rows
        if has_targets:
            params = []
            query = basequery + f" AND {that}_{node_type}_id = %s"
            for row in results:
                p = parameters.copy()
                p.append(row[f'{that}_{node_type}_id'])
                params.append(p)
            results = await self.concurrent_with_args(
                        currency, 'transformed', query, params)

        if orig_node_type == 'entity' and currency == 'eth':
            for neighbor in results:
                neighbor[that + '_cluster_id'] = neighbor[that + '_address_id']

        if orig_node_type == 'address':
            ids = [row[that+'_address_id'] for row in results]
            addresses = await self.get_addresses_by_ids(currency, ids, False)
            for (row, address) in zip(results, addresses):
                row[f'{that}_address'] = address['address']
                row['total_received'] = \
                    self.markup_currency(currency, address['total_received'])
                row['total_spent'] = \
                    self.markup_currency(currency, address['total_spent'])
        else:
            ids = [row[that+'_cluster_id'] for row in results]
            entities, _ = await self.list_entities(currency, ids, fields=[
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
            await self.include_labels(currency, node_type, that, results)

        return results, to_hex(paging_state)

    @eth
    # @Timer(text="Timer: include_labels {:.2f}")
    async def include_labels(self, currency, node_type, that, nodes):
        for node in nodes:
            node['labels'] = []
        if node_type == 'cluster':
            key = f'{that}_cluster_id'
            params = [(self.get_id_group(currency, row[key]), row[key])
                      for row in nodes if row[f'has_{that}_labels']]
            query = ('select cluster_id, label from cluster_tags where '
                     'cluster_id_group = %s and cluster_id = %s')
            results = await self.concurrent_with_args(
                currency, 'transformed', query, params, one=False)
            i = 0
            for result in results:
                while nodes[i][key] != result[0]['cluster_id']:
                    i += 1
                nodes[i]['labels'] = [row['label'] for row in result]
        else:
            key = f'{that}_address_id'
            params = [[row[key], self.get_id_group(currency, row[key])]
                      for row in nodes if row[f'has_{that}_labels']]
            query = ('select address_id, label from address_tags where '
                     'address_id = %s and address_id_group = %s')
            results = await self.concurrent_with_args(
                currency, 'transformed', query, params, one=False)
            i = 0
            for result in results:
                while nodes[i][key] != result[0]['address_id']:
                    i += 1
                nodes[i]['labels'] = [row['label'] for row in result]

        return nodes

    # @Timer(text="Timer: list_address_tags {:.2f}")
    def list_address_tags(self, currency, label):
        prefix_length = self.get_prefix_lengths(currency)['label']
        label_norm_prefix = label[:prefix_length]
        query = ("SELECT * FROM address_tag_by_label WHERE "
                 "label_norm_prefix = %s and label_norm = %s")
        rows = self.execute(currency, 'transformed', query,
                            [label_norm_prefix, label])
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
        rows = self.execute(currency, 'transformed', query,
                            [label_norm_prefix, label])
        if rows is None:
            return []
        return rows

    async def list_labels(self, currency, expression_norm):
        prefix_lengths = self.get_prefix_lengths(currency)
        if len(expression_norm) < prefix_lengths['label']:
            return []
        expression_norm_prefix = expression_norm[:prefix_lengths['label']]
        query = ("SELECT label, label_norm, currency FROM address_tag_by_label"
                 " WHERE label_norm_prefix = %s GROUP BY label_norm_prefix, "
                 "label_norm")
        result = await self.execute_async(currency, 'transformed', query,
                                          [expression_norm_prefix])
        if result.is_empty():
            return []
        return result.current_rows

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
    async def get_tx(self, currency, tx_hash, include_io=False):
        prefix = self.get_prefix_lengths(currency)
        query = ('SELECT tx_id from transaction_by_tx_prefix where '
                 'tx_prefix=%s and tx_hash=%s')
        params = [tx_hash[:prefix['tx']], bytearray.fromhex(tx_hash)]
        result = await self.execute_async(currency, 'raw', query, params)
        result = result.one()
        if not result:
            raise RuntimeError(
                f'Transaction {tx_hash} not found in {currency}')
        id = result['tx_id']
        params = [self.get_tx_id_group(currency, id), id]
        fields = ("tx_hash, coinbase, block_id, timestamp,"
                  "total_input, total_output")
        if include_io:
            fields += ",inputs,outputs"
        query = (f'SELECT {fields} FROM transaction WHERE '
                 'tx_id_group = %s and tx_id = %s')
        result = await self.execute_async(currency, 'raw', query, params)
        return result.one()

    # @Timer(text="Timer: list_txs {:.2f}")
    def list_txs(self, currency, page=None):

        paging_state = from_hex(page)
        query = "SELECT * FROM transaction"
        results = self.execute(currency, 'raw', query,
                               paging_state=paging_state)

        if results is None:
            return [], None
        return results.current_rows, to_hex(results.paging_state)

    @new
    # @Timer(text="Timer: list_matching_txs {:.2f}")
    async def list_matching_txs(self, currency, expression):
        prefix_lengths = self.get_prefix_lengths(currency)
        if len(expression) < prefix_lengths['tx']:
            return []
        query = ('SELECT tx_hash from transaction_by_tx_prefix where '
                 'tx_prefix=%s')
        results = await self.execute_async(currency, 'raw', query,
                                           [expression[:prefix_lengths['tx']]])
        if results.is_empty():
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
    async def list_txs_by_hashes(self, currency, hashes):
        prefix = self.get_prefix_lengths(currency)
        params = [[hash[:prefix['tx']],
                   bytearray.fromhex(hash)]
                  for hash in hashes]
        statement = ('SELECT tx_id from transaction_by_tx_prefix where '
                     'tx_prefix=%s and tx_hash=%s')
        result = await self.concurrent_with_args(currency, 'raw', statement,
                                                 params)
        ids = (tx['tx_id'] for tx in result)
        return await self.list_txs_by_ids(currency, ids)

    @eth
    async def get_tx_by_hash(self, currency, hash):
        prefix = self.get_prefix_lengths(currency)
        params = [hash[:prefix['tx']], bytearray.fromhex(hash)]
        statement = ('SELECT tx_id from transaction_by_tx_prefix where '
                     'tx_prefix=%s and tx_hash=%s')
        result = await self.execute_async(currency, 'raw', statement, params)
        result = result.one()
        if not result:
            return None
        return self.get_tx_by_id(currency, result['tx_id'])

    @eth
    # @Timer(text="Timer: list_txs_by_ids {:.2f}")
    async def list_txs_by_ids(self, currency, ids, filter_empty=True):
        params = ([self.get_tx_id_group(currency, id), id] for id in ids)
        statement = ('SELECT * FROM transaction WHERE '
                     'tx_id_group = %s and tx_id = %s')
        return await self.concurrent_with_args(currency, 'raw', statement,
                                               params,
                                               filter_empty=filter_empty)

    @eth
    async def get_tx_by_id(self, currency, id):
        params = [self.get_tx_id_group(currency, id), id]
        statement = ('SELECT * FROM transaction WHERE '
                     'tx_id_group = %s and tx_id = %s')
        return (await self.execute_async(currency, 'raw', statement, params)
                ).one()

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
            ids = self.concurrent_with_args(currency, 'transformed', query,
                                            params)
            query = ("SELECT * FROM address WHERE "
                     "address_id_group = %s AND address_id = %s")
            params = [[self.get_id_group(currency, row['address_id']),
                       row['address_id']] for row in ids]
            result = self.concurrent_with_args(currency, 'transformed', query,
                                               params)
            paging_state = None
        else:
            query = "SELECT * FROM address"
            fetch_size = min(pagesize or SMALL_PAGE_SIZE, SMALL_PAGE_SIZE)
            result = self.execute(currency, 'transformed', query,
                                  paging_state=from_hex(page),
                                  fetch_size=fetch_size)
            paging_state = result.paging_state
            result = result.current_rows

        result = self.finish_addresses(currency, result)
        if currency != 'eth':
            return result, to_hex(paging_state)

        return result, to_hex(paging_state)

    async def finish_entities(self, currency, rows, with_txs=True):
        return await self.finish_addresses(currency, rows, with_txs)

    async def finish_addresses(self, currency, rows, with_txs=True):
        aws = [self.finish_address(currency, row, with_txs=with_txs)
               for row in rows]
        return await asyncio.gather(*aws)

    @eth
    async def finish_address(self, currency, row, with_txs=True):
        row['total_received'] = \
            self.markup_currency(currency, row['total_received'])
        row['total_spent'] = \
            self.markup_currency(currency, row['total_spent'])

        if not with_txs:
            return row

        TxSummary = namedtuple('TxSummary', ['height', 'timestamp', 'tx_hash'])

        aws = [self.get_tx_by_id(currency, id)
               for id in [row['first_tx_id'], row['last_tx_id']]]
        [tx1, tx2] = await asyncio.gather(*aws)

        if not tx1 or not tx2:
            raise RuntimeError(f"transactions for {row['address']} not found")

        row['first_tx'] = TxSummary(
            tx_hash=tx1['tx_hash'],
            timestamp=tx1['timestamp'],
            height=tx1['block_id'])

        row['last_tx'] = TxSummary(
            tx_hash=tx2['tx_hash'],
            timestamp=tx2['timestamp'],
            height=tx2['block_id'])

        return row

    async def finish_address_eth(self, currency, row, with_txs=True):
        if 'address' in row:
            row['address'] = eth_address_to_hex(row['address'])
        row['cluster_id'] = row['address_id']
        row['total_received'] = \
            self.markup_currency(currency, row['total_received'])
        row['total_spent'] = \
            self.markup_currency(currency, row['total_spent'])

        if not with_txs:
            return row

        TxSummary = namedtuple('TxSummary', ['height', 'timestamp', 'tx_hash'])

        aws = [self.get_tx_by_id(currency, id)
               for id in [row['first_tx_id'], row['last_tx_id']]]

        [tx1, tx2] = await asyncio.gather(*aws)

        if not tx1 or not tx2:
            raise RuntimeError(f"transactions for {row['address']} not found")

        row['first_tx'] = TxSummary(
            tx_hash=tx1['tx_hash'],
            timestamp=tx1['block_timestamp'],
            height=tx1['block_id'])

        row['last_tx'] = TxSummary(
            tx_hash=tx2['tx_hash'],
            timestamp=tx2['block_timestamp'],
            height=tx2['block_id'])
        return row

#####################
# ETHEREUM VARIANTS #
#####################

    # @Timer(text="Timer: get_currency_statistics_eth {:.2f}")
    async def get_currency_statistics_eth(self, currency):
        query = "SELECT * FROM summary_statistics LIMIT 1"
        result = (await self.execute_async(currency, 'transformed', query)
                  ).one()
        if not result:
            return None
        result['no_clusters'] = 0
        return result

    def scrub_prefix_eth(self, currency, expression):
        # remove 0x prefix
        return expression[2:]

    async def get_block_eth(self, currency, height):
        block_group = self.get_block_id_group(currency, height)
        query = ("SELECT * FROM block WHERE block_id_group = %s and"
                 " block_id = %s")
        return (await self.execute_async(currency, 'raw', query,
                                         [block_group, height])).one()

    # entity = address_id
    # @Timer(text="Timer: get_entity_eth {:.2f}")
    async def get_entity_eth(self, currency, entity):
        # mockup entity by address
        id_group = self.get_id_group(currency, entity)
        query = (
            "SELECT * FROM address WHERE "
            "address_id_group = %s AND address_id = %s")
        result = await self.execute_async(currency, 'transformed', query,
                                          [id_group, entity])
        result = result.one()
        if not result:
            return None

        entity = (await self.finish_addresses(currency, [result]))[0]
        entity['cluster_id'] = entity['address_id']
        entity['no_addresses'] = 1
        entity.pop('address', None)
        return entity

    # @Timer(text="Timer: list_entities_eth {:.2f}")
    async def list_entities_eth(self, currency, ids, page=None, pagesize=None,
                                fields=['*']):
        fields = ['address_id' if i == 'cluster_id' else i for i in fields]
        flds = ','.join(fields)
        query = f"SELECT {flds} FROM address"
        has_ids = isinstance(ids, list)
        if has_ids:
            query += " WHERE address_id_group = %s AND address_id = %s"
            params = [[self.get_id_group(currency, id),
                       id] for id in ids]
            result = await self.concurrent_with_args(
                        currency, 'transformed', query, params)
            paging_state = None
        else:
            fetch_size = min(pagesize or SMALL_PAGE_SIZE, SMALL_PAGE_SIZE)
            result = await self.execute_async(currency, 'transformed', query,
                                              paging_state=from_hex(page),
                                              fetch_size=fetch_size)
            paging_state = result.paging_state
            result = result.current_rows

        with_txs = '*' in fields \
            or 'first_tx_id' in fields \
            or 'last_tx_id' in fields
        result = await self.finish_addresses(currency, result, with_txs)

        for address in result:
            address['cluster_id'] = address['address_id']
            address['no_addresses'] = 1
        return result, to_hex(paging_state)

    async def list_entity_tags_by_entity_eth(self, currency, entity):
        return []

    # @Timer(text="Timer: list_address_tags_by_entity_eth {:.2f}")
    async def list_address_tags_by_entity_eth(self, currency, entity):
        query = ("SELECT address FROM address "
                 "WHERE address_id_group=%s and address_id=%s")
        id_id_group = [self.get_id_group(currency, entity), entity]
        result = await self.execute_async(currency, 'transformed', query,
                                          id_id_group)
        result = result.one()
        if result is None:
            return None
        address = result['address']
        query = ("SELECT * FROM address_tags WHERE address_id_group = %s "
                 "and address_id = %s")
        results = await self.execute_async(currency, 'transformed', query,
                                           id_id_group)
        if results is None:
            return []
        for tag in results.current_rows:
            tag['address'] = eth_address_to_hex(address)
        return results.current_rows

    # @Timer(text="Timer: get_address_entity_id_eth {:.2f}")
    def get_address_entity_id_eth(self, currency, address):
        return self.get_address_id(currency, address)

    # @Timer(text="Timer: list_block_txs_eth {:.2f}")
    async def list_block_txs_eth(self, currency, height):
        height_group = self.get_block_id_group(currency, height)
        query = ("SELECT txs FROM block_transactions WHERE "
                 "block_id_group = %s and block_id = %s")
        result = await self.execute_async(currency, 'transformed', query,
                                          [height_group, height])
        if result is None:
            raise RuntimeError(
                    f'block {height} not found in currency {currency}')
        return await self.list_txs_by_ids(currency, result.one()['txs'])

    # @Timer(text="Timer: get_id_secondary_group_eth {:.2f}")
    async def get_id_secondary_group_eth(self, table, id_group):
        column_prefix = ''
        if table == 'address_incoming_relations':
            column_prefix = 'dst_'
        elif table == 'address_outgoing_relations':
            column_prefix = 'src_'

        query = (f"SELECT max_secondary_id FROM {table}_"
                 f"secondary_ids WHERE {column_prefix}address_id_group = %s")
        result = (await self.execute_async('eth', 'transformed', query,
                                           [id_group])).one()
        return 0 if result is None else \
            result['max_secondary_id']

    async def list_txs_by_node_type_eth(self, currency, node_type, address,
                                        page=None, pagesize=None):
        paging_state = from_hex(page)
        if node_type == 'address':
            address_id, id_group = \
                await self.get_address_id_id_group(currency, address)
        else:
            node_type = 'address'
            address_id = address
            id_group = self.get_id_group(currency, address_id)
        secondary_id_group = \
            await self.get_id_secondary_group_eth('address_transactions',
                                                  id_group)

        sec_in = self.sec_in(secondary_id_group)
        query = ("SELECT transaction_id, value FROM address_transactions "
                 "WHERE address_id_group = %s and "
                 f"address_id_secondary_group in {sec_in}"
                 " and address_id = %s")
        fetch_size = min(pagesize or BIG_PAGE_SIZE, BIG_PAGE_SIZE)
        result = await self.execute_async(currency, 'transformed', query,
                                          [id_group, address_id],
                                          paging_state=paging_state,
                                          fetch_size=fetch_size)
        if result is None:
            raise RuntimeError(
                    f'address {address} not found in currency {currency}')
        txs = [row['transaction_id'] for row in result.current_rows]
        paging_state = result.paging_state
        for (row1, row2) in zip(
                result.current_rows,
                await self.list_txs_by_ids(currency, txs)):
            row1['tx_hash'] = row2['tx_hash']
            row1['height'] = row2['block_id']
            row1['timestamp'] = row2['block_timestamp']
            row1['to_address'] = eth_address_to_hex(row2['to_address'])
            row1['from_address'] = eth_address_to_hex(row2['from_address'])
        return result.current_rows, to_hex(paging_state)

    async def list_txs_by_ids_eth(self, currency, ids):
        params = [[self.get_id_group(currency, id), id] for id in ids]
        statement = (
            'SELECT transaction from transaction_ids_by_transaction_id_group'
            ' where transaction_id_group = %s and transaction_id = %s')
        result = await self.concurrent_with_args(currency, 'transformed',
                                                 statement, params)
        return await self.list_txs_by_hashes(currency, [row['transaction']
                                                        for row in result])

    async def get_tx_by_id_eth(self, currency, id):
        params = [self.get_id_group(currency, id), id]
        statement = (
            'SELECT transaction from transaction_ids_by_transaction_id_group'
            ' where transaction_id_group = %s and transaction_id = %s')
        result = await self.execute_async(currency, 'transformed', statement,
                                          params)
        result = result.one()
        if not result:
            return None
        return await self.get_tx_by_hash(currency,
                                         result['transaction'])

    # @Timer(text="Timer: list_txs_by_hashes_eth {:.2f}")
    async def list_txs_by_hashes_eth(self, currency, hashes):
        prefix = self.get_prefix_lengths(currency)
        params = [[hash.hex()[:prefix['tx']], hash]
                  for hash in hashes]
        statement = (
            'SELECT tx_hash, block_id, block_timestamp, value, '
            'from_address, to_address from '
            'transaction where tx_hash_prefix=%s and tx_hash=%s')
        result = await self.concurrent_with_args(currency, 'raw', statement,
                                                 params)
        for row in result:
            row['from_address'] = eth_address_to_hex(row['from_address'])
            row['to_address'] = eth_address_to_hex(row['to_address'])
        return result

    async def get_tx_by_hash_eth(self, currency, hash):
        prefix = self.get_prefix_lengths(currency)
        params = [hash.hex()[:prefix['tx']], hash]
        statement = (
            'SELECT tx_hash, block_id, block_timestamp, value, '
            'from_address, to_address from '
            'transaction where tx_hash_prefix=%s and tx_hash=%s')
        result = await self.execute_async(currency, 'raw', statement, params)
        result = result.one()
        if not result:
            return None
        result['from_address'] = eth_address_to_hex(result['from_address'])
        result['to_address'] = eth_address_to_hex(result['to_address'])
        return result

    # @Timer(text="Timer: list_address_links_eth {:.2f}")
    def list_links_eth(self, currency, node_type, address, neighbor,
                       page=None, pagesize=None):
        if node_type == 'address':
            address_id, address_id_group = \
                self.get_address_id_id_group(currency, address)
            neighbor_id, neighbor_id_group = \
                self.get_address_id_id_group(currency, neighbor)
        else:
            node_type = 'address'
            address_id = address
            address_id_group = self.get_id_group(currency, address)
            neighbor_id = neighbor
            neighbor_id_group = self.get_id_group(currency, neighbor_id)

        address_id_secondary_group = \
            self.get_id_secondary_group_eth('address_transactions',
                                            address_id_group)
        address_id_secondary_group = self.sec_in(address_id_secondary_group)
        neighbor_id_secondary_group = \
            self.get_id_secondary_group_eth('address_transactions',
                                            neighbor_id_group)
        neighbor_id_secondary_group = self.sec_in(neighbor_id_secondary_group)

        if address_id is None or neighbor_id is None:
            raise RuntimeError("Links between {} and {} not found"
                               .format(address, neighbor))

        query = "SELECT no_{direction}_txs FROM address " \
                "WHERE address_id_group = %s AND address_id = %s"

        no_outgoing_txs = self.execute(
            currency, 'transformed', query.format(direction='outgoing'),
            [address_id_group, address_id]
            ).one()['no_outgoing_txs']

        no_incoming_txs = self.execute(
            currency, 'transformed', query.format(direction='incoming'),
            [neighbor_id_group, neighbor_id]
            ).one()['no_incoming_txs']

        first_id_group, first_id, second_id_group, second_id, \
            first_id_secondary_group, second_id_secondary_group = \
            (address_id_group, address_id, neighbor_id_group, neighbor_id,
             address_id_secondary_group, neighbor_id_secondary_group) \
            if no_outgoing_txs < no_incoming_txs \
            else (neighbor_id_group, neighbor_id, address_id_group, address_id,
                  neighbor_id_secondary_group, address_id_secondary_group)

        basequery = "SELECT transaction_id FROM address_transactions WHERE " \
                    "address_id_group = %s AND address_id = %s "
        first_query = basequery + \
            f"AND address_id_secondary_group IN {address_id_secondary_group}"
        second_query = basequery + \
            f"AND address_id_secondary_group IN {neighbor_id_secondary_group}"\
            " AND transaction_id = %s"

        fetch_size = min(pagesize or SMALL_PAGE_SIZE, SMALL_PAGE_SIZE)
        paging_state = from_hex(page)
        has_more_pages = True
        count = 0
        tx_ids = []

        while count < fetch_size and has_more_pages:
            results1 = self.execute(currency, 'transformed', first_query,
                                    [first_id_group, first_id],
                                    paging_state=paging_state,
                                    fetch_size=fetch_size)

            if not results1.current_rows:
                return [], None

            has_more_pages = results1.has_more_pages
            paging_state = results1.paging_state

            params = [[second_id_group, second_id, row['transaction_id']]
                      for row in results1.current_rows]

            results2 = self.concurrent_with_args(
                currency, 'transformed', second_query, params)

            for row in results2:
                tx_ids.append(row['transaction_id'])
                count += 1

        return self.list_txs_by_ids(currency, tx_ids), to_hex(paging_state)

    # @Timer(text="Timer: get_tx_eth {:.2f}")
    async def get_tx_eth(self, currency, tx_hash, include_io=False):
        return await self.get_tx_by_hash(currency,
                                         bytearray.fromhex(tx_hash))

    # @Timer(text="Timer: list_entity_addresses_eth {:.2f}")
    async def list_entity_addresses_eth(self, currency, entity, page=None,
                                        pagesize=None):
        addresses = []
        async for address in self.get_addresses_by_ids(currency, [entity]):
            addresses.append(await self.finish_address(currency, address))
        return addresses, None

    def list_entity_tags_eth(self, currency, label):
        return []

    async def include_labels_eth(self, currency, node_type, that, nodes):
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
            results = await self.concurrent_with_args(
                currency, 'transformed', query, params, one=False)
            i = 0
            for result in results:
                while nodes[i][key] != result[0]['address_id']:
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

    async def list_matching_txs_new(self, currency, expression):
        prefix_lengths = self.get_prefix_lengths(currency)
        if len(expression) < prefix_lengths['tx']:
            return []
        query = ('SELECT transaction from transaction_ids_by_transaction_pre'
                 'fix where transaction_prefix = %s')
        prefix = expression[:prefix_lengths['tx']].upper()
        results = await self.execute_async(currency, 'transformed', query,
                                           [prefix])
        if results.is_empty():
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
        rows = self.execute(currency, 'transformed', query,
                            [label_norm_prefix, label])
        if rows is None:
            return []
        return rows

    def sec_in(self, id):
        return "(" + ','.join(map(str, range(0, id+1))) + ")"

