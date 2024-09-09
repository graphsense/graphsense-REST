import re
import time
import asyncio
import heapq
from async_lru import alru_cache
from typing import Sequence, Optional, Tuple
from functools import partial
from itertools import product
from collections import namedtuple, UserDict
from cassandra import InvalidRequest, ConsistencyLevel
from cassandra.protocol import ProtocolException
from cassandra.cluster import (EXEC_PROFILE_DEFAULT, Cluster, ExecutionProfile,
                               NoHostAvailable)
from cassandra.policies import DCAwareRoundRobinPolicy, TokenAwarePolicy
from cassandra.query import SimpleStatement, dict_factory, ValueSequence
from math import floor, ceil

from gsrest.util.eth_logs import decode_db_logs
from gsrest.errors import (NetworkNotFoundException, BadUserInputException,
                           BadConfigError, NotFoundException,
                           BlockNotFoundException, AddressNotFoundException,
                           ClusterNotFoundException, DBInconsistencyException,
                           nodeNotFoundException, TransactionNotFoundException)

from gsrest.util import is_eth_like
from gsrest.util.address import (address_to_user_format)
from gsrest.util.evm import (bytes_to_hex, strip_0x, hex_str_to_bytes)
from gsrest.util.tron import partial_tron_to_partial_evm
from gsrest.util.node_balances import get_balances
from gsrest.util.id_group import calculate_id_group_with_overflow
from gsrest.db.node_type import NodeType
import logging
from pprint import PrettyPrinter

SMALL_PAGE_SIZE = 1000
BIG_PAGE_SIZE = 5000
SEARCH_PAGE_SIZE = 100


class NetworkParameters(UserDict):

    def __getitem__(self, network):
        if network not in self:
            raise NetworkNotFoundException(network)
        return super().__getitem__(network)


def to_hex(paging_state):
    return paging_state.hex() if paging_state else paging_state


def bytes_from_hex(h_str: str) -> bytes:
    if isinstance(h_str, str) and h_str.startswith("0x"):
        h_str = h_str[2:]
    return bytes.fromhex(h_str) if h_str else None


def tx_hash_from_hex(tx_hash_str: str) -> bytes:
    try:
        return bytes_from_hex(tx_hash_str)
    except ValueError:
        raise BadUserInputException(
            f"{tx_hash_str} does not look like a valid "
            "transaction hash.")


def page_from_hex(page):
    try:
        return bytes_from_hex(page)
    except ValueError:
        # bytes.fromHex throws value error if non hex chars are found
        raise BadUserInputException(
            f"The requested next page token ({page}) "
            "is not formatted correctly. "
            "Only use the next_page token found in the response.")


def transaction_ordering_key(tx_id_key, tx):
    ref = tx.get("tx_reference", [None, None])
    trace_index = ref[0] or 0
    log_index = ref[1] or 0
    return (tx[tx_id_key], -trace_index, -log_index)


def identity1(x):
    return x


def identity2(y, x):
    return x


def fmt(v):
    if isinstance(v, str):
        return "'" + v + "'"
    if isinstance(v, bytes):
        return "0x" + v.hex()
    return str(v)


def replaceFrom(keyspace, query):
    r = re.compile(r'\s+FROM\s+', re.IGNORECASE)
    return r.sub(f' FROM {keyspace}.', query)


def replacePerc(query, named=False):
    if not named:
        r = re.compile(r'%s', re.IGNORECASE)
        return r.sub('?', query)
    else:
        r = re.compile(r'%\((\S+?)\)s', re.IGNORECASE)
        return r.sub(r':\1', query)


def one(result):
    if result is not None:
        return result.one()
    return None


def build_token_tx(token_currency, tx, token_tx, log):
    token_from = token_tx["data"].get("from", "decoding error")
    token_to = token_tx["data"].get("to", "decoding error")
    value = token_tx["data"].get("value", "decoding error")
    return {
        "currency": token_currency,
        "block_id": tx["block_id"],
        "block_timestamp": tx["block_timestamp"],
        "tx_hash": tx["tx_hash"],
        "from_address": hex_str_to_bytes(strip_0x(token_from["value"])),
        "to_address": hex_str_to_bytes(strip_0x(token_to["value"])),
        "token_tx_id": log["log_index"],
        "value": value["value"]
    }


class BytesPrettyPrinter(PrettyPrinter):

    def format(self, object, context, maxlevels, level):
        if isinstance(object, bytes):
            x = object.hex()
            return (x[0:24] + "...", True, False)
        return PrettyPrinter.format(self, object, context, maxlevels, level)


class Result:

    def __init__(self, current_rows, params, paging_state):
        self.current_rows = current_rows
        self.params = params
        self.paging_state = paging_state

    def __len__(self):
        return len(self.current_rows)

    def __getitem__(self, key):
        return self.current_rows[key]

    def is_empty(self):
        return self.current_rows is None or not self.current_rows

    def one(self):
        if self.is_empty():
            return None
        return self.current_rows[0]


TxSummary = namedtuple('TxSummary', ['height', 'timestamp', 'tx_hash'])


def get_tx_id_column_name(network: str) -> str:
    return 'transaction_id' if is_eth_like(network) else 'tx_id'


# helper functions
def wc(cl, cond):
    return f"AND {cl} " if cond else ""


def merge_address_txs_subquery_results(
    result_sets: Sequence[Result],
    ascending: bool,
    fetch_size: int,
    tx_id_keys: str = "tx_id",
    fetched_limit: Optional[int] = None
) -> Tuple[Sequence[dict], Optional[int]]:
    """Merges sub results of the address txs queries per asset and direction

    Args:
        result_sets (Sequence[Result]): List of result sets,
            one per parameter tuple
        fetch_size (int): number of items return at most
        tx_id_keys (str): name of the tx_id column
        fetched_limit (int): The limit that was used to fetch the result sets

    Returns:
        Tuple[Sequence[dict], Optional[int]]: A merged list of ordered
            transactions and the highest id included in this results set,
            this is considered as the page for subsequent queries.
    """

    # find the least common tx_id where we then cut the result sets
    border_tx_id = None
    has_pages = False
    total_results_len = 0
    for results in result_sets:
        if not results:
            continue
        total_results_len += len(results)
        if fetched_limit and len(results) < fetched_limit:
            continue
        has_pages = True
        if border_tx_id is None:
            border_tx_id = results[-1][tx_id_keys]
            continue
        order = min if ascending else max
        border_tx_id = order(border_tx_id, results[-1][tx_id_keys])

    # cut result_sets so that we only have the overlapping rows below/above
    # the border_tx_id
    # filtered out rows could be overlapping with yet not retrieved result sets
    candidates = [
        v for results in result_sets for v in results
        if border_tx_id is None or ascending and v[tx_id_keys] <= border_tx_id
        or not ascending and v[tx_id_keys] >= border_tx_id
    ]

    # Merge overlapping result sets by given sort order (uses a priority
    # queue; heapq)
    # fetch_sized items or less are returned
    precedence = heapq.nsmallest if ascending else heapq.nlargest
    results = precedence(fetch_size,
                         candidates,
                         key=partial(transaction_ordering_key, tx_id_keys))

    # use the last tx_id as page handle
    border_tx_id = results[-1][tx_id_keys] \
        if results and (has_pages or total_results_len >= fetch_size) else None
    return results, border_tx_id


def build_select_address_txs_statement(network: str, node_type: NodeType,
                                       cols: Optional[Sequence[str]],
                                       with_lower_bound: bool,
                                       with_upper_bound: bool,
                                       with_tx_id: bool, ascending: bool,
                                       limit: int) -> str:
    # prebuild useful helpers and conditions
    eth_like = is_eth_like(network)
    tx_id_col = get_tx_id_column_name(network)

    # Select and shared where clause
    # Build select statement
    columns = (",".join(cols) if cols is not None else "*")

    query = (f"SELECT {columns} from {node_type}_transactions "
             f"WHERE {node_type}_id = %(id)s "
             f"AND {node_type}_id_group = %(g_id)s "
             "AND is_outgoing = %(is_outgoing)s ")

    # conditional where clause, loop independent
    query += wc(f"{node_type}_id_secondary_group = %(s_d_group)s", eth_like)

    query += wc("currency = %(currency)s", eth_like)

    # conditional where clause, loop dependent
    if not with_tx_id:
        if ascending:
            query += wc(f"{tx_id_col} > %(tx_id_lower_bound)s",
                        with_lower_bound)
            query += wc(f"{tx_id_col} <= %(tx_id_upper_bound)s",
                        with_upper_bound)
        else:
            query += wc(f"{tx_id_col} >= %(tx_id_lower_bound)s",
                        with_lower_bound)
            query += wc(f"{tx_id_col} < %(tx_id_upper_bound)s",
                        with_upper_bound)
    else:
        query += wc(f"{tx_id_col} = %(tx_id)s", True)

    ordering = "ASC" if ascending else "DESC"
    # Ordering statement
    ordering_statement = ("ORDER BY " +
                          (f" currency {ordering}," if eth_like else "") +
                          f" {tx_id_col} {ordering}")

    return f"{query} {ordering_statement} LIMIT {limit}"


class Cassandra:

    def eth(func):

        def check(*args, **kwargs):
            self = args[0]
            currency = args[1]
            if (is_eth_like(currency)):
                # first look for currency specific
                # then fallback to eth.
                do = func.__name__ + "_" + currency
                if not hasattr(self, do):
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
            if (is_eth_like(currency)):
                do = func.__name__ + "_new"
                if hasattr(self, do) and callable(getattr(self, do)):
                    f = getattr(self, do)
                    args = args[1:]
                    return f(*args, **kwargs)
            return func(*args, **kwargs)

        return check

    def __init__(self, config, logger):
        self.logger = logger
        if 'currencies' not in config:
            raise BadConfigError('Missing config property: currencies')
        if 'nodes' not in config:
            raise BadConfigError('Missing config property: nodes')
        self.config = config
        self.prepared_statements = {}
        self.connect()
        self.parameters = NetworkParameters()
        for currency in config['currencies']:
            self.check_keyspace(config['currencies'][currency]['raw'])
            self.check_keyspace(config['currencies'][currency]['transformed'])
            self.load_parameters(currency)

    def connect(self):
        try:
            cl = ConsistencyLevel.name_to_value.get(
                self.config.get("consistency_level", "LOCAL_ONE"),
                ConsistencyLevel.LOCAL_ONE)

            exec_prof = ExecutionProfile(
                request_timeout=60,
                row_factory=dict_factory,
                load_balancing_policy=TokenAwarePolicy(
                    DCAwareRoundRobinPolicy()),
                consistency_level=cl)
            self.cluster = Cluster(
                self.config['nodes'],
                protocol_version=5,
                connect_timeout=60,
                execution_profiles={EXEC_PROFILE_DEFAULT: exec_prof})
            self.session = self.cluster.connect()
            # self.session.row_factory = dict_factory
            if self.logger:
                self.logger.info(f'Connection ready. Using CL: {cl}')
        except NoHostAvailable:
            retry = self.config.get('retry_interval', None)
            retry = 5 if retry is None else retry
            if self.logger:
                self.logger.error(
                    f'Could not connect. Retrying in {retry} secs.')
            time.sleep(retry)
            self.connect()

    def check_keyspace(self, keyspace):
        query = ("SELECT * FROM system_schema.keyspaces "
                 "where keyspace_name = %s")
        result = self.session.execute(query, [keyspace])
        if one(result) is None:
            raise BadConfigError("Keyspace {} does not exist".format(keyspace))

    @eth
    def load_token_configuration(self, currency):
        return None

    def load_token_configuration_eth(self, currency):
        query = "SELECT * FROM token_configuration"
        return {
            row["currency_ticker"]: row
            for row in self.execute(currency, "transformed", query)
        }

    async def fix_timestamp(self,
                            currency,
                            item,
                            timestamp_col="block_timestamp",
                            block_id_col="block_id"):
        if currency == "trx" and item[timestamp_col] < 500000000:
            # TODO block timestamp in tx is currently
            # wrong / we divide by 1000 to get from
            # mili to seconds. But it appears to be
            # wrong in the txs.
            block = await self.get_block_timestamp_eth(currency,
                                                       item[block_id_col])
            if block is not None:
                item[timestamp_col] = block["timestamp"]
            else:
                self.logger.warning(
                    f"Could not load block {item[block_id_col]}, "
                    "to fix timestamp.")

    def load_parameters(self, keyspace):
        currency = keyspace
        self.parameters[keyspace] = {}
        for kind in ['raw', 'transformed']:
            query = "SELECT * FROM configuration"
            result = self.execute(keyspace, kind, query)
            if one(result) is None:
                raise BadConfigError(
                    f"No configuration table found for {kind} keyspace {{}}".
                    format(keyspace))
            for key, value in result.one().items():
                self.parameters[keyspace][key] = value

        self.parameters[keyspace][
            "token_config"] = self.load_token_configuration(keyspace)

        # check schema for compatibility and set parameter flags
        keyspace_name = self.get_keyspace_mapping(keyspace, "transformed")

        if keyspace == "eth":
            query = ("SELECT column_name FROM system_schema.columns "
                     "WHERE keyspace_name = %s AND "
                     "table_name = 'block_transactions';")
            result = self.session.execute(query, (keyspace_name, ))
            self.parameters[currency]["use_flat_block_txs"] = ("tx_id" in [
                x["column_name"] for x in result
            ]) and keyspace == "eth"
        else:
            self.parameters[currency]["use_flat_block_txs"] = False

        query = (
            "SELECT column_name FROM system_schema.columns "
            "WHERE keyspace_name = %s AND table_name = 'address_transactions';"
        )
        result = self.session.execute(query, (keyspace_name, ))
        self.parameters[currency]["use_legacy_log_index"] = ("log_index" in [
            x["column_name"] for x in result
        ]) and keyspace == "eth"

        query = ("SELECT table_name FROM system_schema.tables "
                 "WHERE keyspace_name = %s ;")
        result = self.session.execute(query, (keyspace_name, ))
        self.parameters[currency]["use_delta_updater_v1"] = (
            "new_addresses" in [x["table_name"] for x in result])

        keyspace_name = self.get_keyspace_mapping(keyspace, "raw")
        result = self.session.execute(query, (keyspace_name, ))

        self.parameters[currency]["tx_graph_available"] = (
            "transaction_spending" in [x["table_name"] for x in result])

    def get_prefix_lengths(self, currency):
        if currency not in self.parameters:
            raise NetworkNotFoundException(currency)
        p = self.parameters[currency]
        return \
            {'address': p['address_prefix_length'],
             'tx': p['tx_prefix_length']}

    def get_supported_currencies(self):
        return self.config['currencies'].keys()

    def get_token_configuration(self, currency):
        eth_config = self.parameters.get(currency, None)
        return eth_config["token_config"] if eth_config is not None else {}

    def get_balance_provider(self, currency):
        provider = self.config['currencies'][currency].get(
            "balance_provider", None)
        if provider is not None:
            return partial(get_balances, provider)
        else:
            return None

    def get_keyspace_mapping(self, currency, keyspace_type):
        if currency is None:
            raise BadUserInputException('Missing currency')
        if keyspace_type not in ('raw', 'transformed'):
            raise BadUserInputException(
                f'Unknown keyspace type {keyspace_type}')
        if currency not in self.config['currencies']:
            raise BadUserInputException(
                f'Unknown currency in config: {currency}')
        return self.config['currencies'][currency][keyspace_type]

    def close(self):
        self.cluster.shutdown()

    def execute(self,
                currency,
                keyspace_type,
                query,
                params=None,
                paging_state=None,
                fetch_size=None):
        keyspace = self.get_keyspace_mapping(currency, keyspace_type)
        q = replaceFrom(keyspace, query)
        # self.logger.debug(f'{query} {params}')
        q = SimpleStatement(q, fetch_size=fetch_size)

        try:
            result = self.session.execute(q, params, paging_state=paging_state)
        except NoHostAvailable:
            self.connect()
            result = self.execute(currency,
                                  keyspace_type,
                                  query,
                                  params=params,
                                  paging_state=paging_state,
                                  fetch_size=fetch_size)

        return result

    async def execute_async(self,
                            currency,
                            keyspace_type,
                            query,
                            params=[],
                            paging_state=None,
                            fetch_size=None,
                            autopaging=False):
        try:
            result = await self.execute_async_lowlevel(
                currency,
                keyspace_type,
                query,
                params=params,
                paging_state=paging_state,
                fetch_size=fetch_size)
        except ProtocolException as e:
            if 'Invalid value for the paging state' not in str(e):
                raise e
            raise BadUserInputException(
                'Invalid value for page. Please use handle from '
                'previous requests.')
        if not autopaging:
            return result

        if result.paging_state is None:
            return result

        more = await self.execute_async(currency,
                                        keyspace_type,
                                        query,
                                        params=params,
                                        paging_state=result.paging_state,
                                        fetch_size=fetch_size,
                                        autopaging=True)

        for row in more.current_rows:
            result.current_rows.append(row)
        return result

    def execute_async_lowlevel(self,
                               currency,
                               keyspace_type,
                               query,
                               params=[],
                               paging_state=None,
                               fetch_size=None):
        named_params = isinstance(params, dict)
        keyspace = self.get_keyspace_mapping(currency, keyspace_type)
        query = replaceFrom(keyspace, query)
        q = replacePerc(query, named=named_params)

        prep = self.prepared_statements.get(q, None)
        if prep is None:
            self.prepared_statements[q] = prep = self.session.prepare(q)
        try:
            prep.fetch_size = int(fetch_size) if fetch_size else None
            # self.session.default_timeout = 60
            response_future = self.session.execute_async(
                prep, params, timeout=60, paging_state=paging_state)
            loop = asyncio.get_event_loop()
            future = loop.create_future()

            def on_done(result):
                if future.cancelled():
                    loop.call_soon_threadsafe(future.set_result, None)
                    return
                result = Result(current_rows=result,
                                params=params,
                                paging_state=response_future._paging_state)
                if self.logger.level == logging.DEBUG:
                    if named_params:
                        formatted = query
                        for k, v in params.items():
                            formatted = formatted.replace(
                                "%(" + k + ")s", fmt(v))
                    else:
                        formatted = query % tuple([fmt(v) for v in params])
                    self.logger.debug(formatted)
                    # pp = BytesPrettyPrinter()
                    # self.logger.debug(pp.pformat(result.current_rows))
                    self.logger.debug(
                        f'result size {len(result.current_rows)}')
                loop.call_soon_threadsafe(future.set_result, result)

            def on_err(result):
                loop.call_soon_threadsafe(future.set_exception, result)

            response_future.add_callbacks(on_done, on_err)
            return future
        except NoHostAvailable:
            self.connect()
            return self.execute_async_lowlevel(currency,
                                               keyspace_type,
                                               query,
                                               params=params,
                                               paging_state=paging_state,
                                               fetch_size=fetch_size)

    async def concurrent_with_args(self,
                                   currency,
                                   keyspace_type,
                                   query,
                                   params,
                                   filter_empty=True,
                                   return_one=True,
                                   keep_meta=False):
        aws = [
            self.execute_async(currency,
                               keyspace_type,
                               query,
                               param,
                               autopaging=True) for param in params
        ]
        results = []
        for result in await asyncio.gather(*aws):
            if filter_empty and result is None:
                continue
            if return_one:
                o = one(result)
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
                results.extend(result.current_rows)
            else:
                results.append(result)
        return results

    @alru_cache(ttl=5)
    async def get_currency_statistics(self, currency):
        query = "SELECT * FROM summary_statistics LIMIT 1"
        result = await self.execute_async(currency, 'transformed', query)
        stats = one(result)
        if self.parameters[currency]["use_delta_updater_v1"]:
            try:
                query = "SELECT * FROM delta_updater_status LIMIT 1"
                result = await self.execute_async(currency, 'transformed',
                                                  query)
                result = one(result)
                if result:
                    stats['no_blocks'] = result['last_synced_block'] + 1
                    stats['timestamp'] =\
                        int(result['last_synced_block_timestamp'].timestamp())\
                        if 'last_synced_block_timestamp' in result else\
                        stats['timestamp']

            except InvalidRequest as e:
                if 'delta_updater_status' not in str(e):
                    raise e

        if is_eth_like(currency):
            stats['no_clusters'] = 0

        return stats

    @eth
    async def get_block(self, currency, height):
        query = ("SELECT * FROM block WHERE block_id_group = %s "
                 "AND block_id = %s")
        return (await self.execute_async(
            currency, 'raw', query,
            [self.get_block_id_group(currency, height), height])).one()

    async def list_block_txs(self, currency, height):
        tx_ids = await self.list_block_txs_ids(currency, height)
        if tx_ids is None:
            raise BlockNotFoundException(currency, height)
        tx_ids = sorted(list(set(tx_ids)))
        return await self.list_txs_by_ids(currency,
                                          tx_ids,
                                          include_token_txs=True)

    @alru_cache(maxsize=1000)
    async def get_rates(self, currency, height):
        query = "SELECT * FROM exchange_rates WHERE block_id = %s"
        result = await self.execute_async(currency, 'transformed', query,
                                          [height])
        result = one(result)
        if result is None:
            return None
        return self.markup_rates(currency, result)

    # async def list_rates(self, currency, heights):
    #     result = await self.concurrent_with_args(
    #         currency, 'transformed',
    #         "SELECT * FROM exchange_rates WHERE block_id = %s",
    #         [[h] for h in heights])
    #     for row in result:
    #         self.markup_rates(currency, row)
    #     return result

    async def list_rates(self, currency, heights):
        aws = [self.get_rates(currency, h) for h in heights]
        return await asyncio.gather(*aws)

    async def list_address_txs(self,
                               currency,
                               address,
                               direction,
                               min_height=None,
                               max_height=None,
                               order=None,
                               token_currency=None,
                               page=None,
                               pagesize=None):
        return await self.list_txs_by_node_type(currency,
                                                NodeType.ADDRESS,
                                                address,
                                                direction,
                                                min_height=min_height,
                                                max_height=max_height,
                                                order=order,
                                                token_currency=token_currency,
                                                page=page,
                                                pagesize=pagesize)

    async def list_entity_txs(self,
                              currency,
                              entity,
                              direction,
                              min_height=None,
                              max_height=None,
                              order=None,
                              token_currency=None,
                              page=None,
                              pagesize=None):
        return await self.list_txs_by_node_type(currency,
                                                NodeType.CLUSTER,
                                                entity,
                                                direction,
                                                min_height=min_height,
                                                max_height=max_height,
                                                order=order,
                                                token_currency=token_currency,
                                                page=page,
                                                pagesize=pagesize)

    @eth
    async def list_txs_by_node_type(self,
                                    currency,
                                    node_type: NodeType,
                                    id,
                                    direction,
                                    min_height=None,
                                    max_height=None,
                                    order=None,
                                    token_currency=None,
                                    page=None,
                                    pagesize=None):
        try:
            page = int(page) if page is not None else None
        except ValueError:
            raise BadUserInputException(f"Page {page} is not an integer")
        ascending = order == 'asc'

        first_tx_id, upper_bound = \
            await self.resolve_tx_id_range_by_block(currency,
                                                    min_height,
                                                    max_height)

        fetch_size = min(pagesize or BIG_PAGE_SIZE, BIG_PAGE_SIZE)
        include_assets = [currency.upper()]

        results, paging_state = await self.list_address_txs_ordered(
            network=currency,
            node_type=node_type,
            id=id,
            tx_id_lower_bound=first_tx_id,
            tx_id_upper_bound=upper_bound,
            is_outgoing=(direction == 'out'
                         if direction is not None else None),
            include_assets=include_assets,
            ascending=ascending,
            page=page,
            fetch_size=fetch_size)

        txs = await self.list_txs_by_ids(currency,
                                         [row['tx_id'] for row in results],
                                         filter_empty=False)

        rows = []
        for (row, tx) in zip(results, txs):
            if tx is None:
                continue
            row['tx_hash'] = tx['tx_hash']
            row['height'] = tx['block_id']
            row['timestamp'] = tx['timestamp']
            row['coinbase'] = tx['coinbase']
            rows.append(row)

        return rows, str(paging_state) if paging_state is not None else None

    async def resolve_tx_id_range_by_block(
            self, network: str, min_height: Optional[int],
            max_height: Optional[int]) -> Tuple[Optional[int], Optional[int]]:
        stats = await self.get_currency_statistics(network)
        if not stats:
            return None, None
        last_height = stats['no_blocks'] - 1
        first_tx_id = last_tx_id = None
        max_tries = 100
        if min_height is not None:
            orig_min_height = min_height
            former_txs = []
            while not former_txs:
                former_txs = await self.list_block_txs_ids(network, min_height)
                if former_txs is None:
                    raise BadUserInputException(
                        f'Minimum block height {min_height} does not exist')
                if former_txs:
                    break
                # try one block higher until txs are found
                min_height += 1
                if min_height > last_height:
                    break
                if min_height - orig_min_height > max_tries:
                    raise BadUserInputException(
                        f'Block {orig_min_height} does not contains '
                        'transactions')
            first_tx_id = min(former_txs) if former_txs else None
        if max_height is not None:
            orig_max_height = max_height
            latter_txs = []
            while not latter_txs:
                latter_txs = await self.list_block_txs_ids(network, max_height)
                if latter_txs is None:
                    raise BadUserInputException(
                        f'Maximum block height {max_height} does not exist')
                if latter_txs:
                    break
                # try one block lower until txs are found
                max_height -= 1
                if max_height < 0:
                    break
                if orig_max_height - max_height > max_tries:
                    raise BadUserInputException(
                        f'Block {orig_max_height} does not contains '
                        'transactions')
            last_tx_id = max(latter_txs) + 1 if latter_txs else None
        return first_tx_id, last_tx_id

    @eth
    async def list_block_txs_ids(self, currency, height):
        height_group = self.get_block_id_group(currency, height)
        query = ("SELECT txs FROM block_transactions "
                 "WHERE block_id_group=%s and block_id=%s")
        result = await self.execute_async(
            currency, 'raw', query, [height_group, int(height)])

        if one(result) is None:
            return None
        return [tx.tx_id for tx in result.one()['txs']]

    async def list_block_txs_ids_eth(self, currency, height):
        if not self.parameters[currency]["use_flat_block_txs"]:
            if height is None:
                return None
            height_group = self.get_id_group(currency, height)
            query = ("SELECT txs FROM block_transactions "
                     "WHERE block_id_group=%s and block_id=%s")
            result = await self.execute_async(
                currency, 'transformed', query,
                [height_group, int(height)])
            if one(result) is None:
                return None
            return result.one()['txs']
        else:
            return await self.list_block_txs_ids_trx(currency, height)

    async def list_block_txs_ids_trx(self, currency, height):
        if height is None:
            return None
        height_group = self.get_id_group(currency, height)
        query = ("SELECT tx_id FROM block_transactions "
                 "WHERE block_id_group=%s and block_id=%s")
        result = await self.execute_async(
            currency,
            'transformed',
            query, [height_group, int(height)],
            autopaging=True)
        res = [r["tx_id"] for r in result.current_rows]
        return res

    async def get_addresses_by_ids(self,
                                   currency,
                                   address_ids,
                                   address_only=False):
        params = [(self.get_id_group(currency, address_id), address_id)
                  for address_id in address_ids]
        fields = 'address, address_id, address_id_group' \
            if address_only else '*'
        query = (f"SELECT {fields} FROM address WHERE "
                 "address_id_group = %s and address_id = %s")
        result = await self.concurrent_with_args(currency, 'transformed',
                                                 query, params)

        return result

    async def get_new_address(self, currency, address):
        if not self.parameters[currency]["use_delta_updater_v1"]:
            return None
        prefix = self.scrub_prefix(currency, address)
        if is_eth_like(currency):
            prefix = prefix.upper()
        prefix_length = self.get_prefix_lengths(currency)['address']
        query = ("SELECT * FROM new_addresses "
                 "WHERE address_prefix = %s AND address = %s")
        try:
            result = await self.execute_async(
                currency, 'transformed', query,
                [prefix[:prefix_length], address])
            return one(result)
        except InvalidRequest as e:
            if 'new_addresses' not in str(e):
                raise e

        return None

    async def get_address_id(self, currency, address):
        prefix = self.scrub_prefix(currency, address)
        if is_eth_like(currency):
            prefix = prefix.upper()
        query = ("SELECT address_id FROM address_ids_by_address_prefix "
                 "WHERE address_prefix = %s AND address = %s")
        prefix_length = self.get_prefix_lengths(currency)['address']
        result = await self.execute_async(currency, 'transformed', query,
                                          [prefix[:prefix_length], address])
        result = one(result)
        if not result:
            return None

        return result['address_id']

    async def get_address_id_id_group(self, currency, address):
        address_id = await self.get_address_id(currency, address)
        if address_id is None:
            raise AddressNotFoundException(currency, address)
        id_group = self.get_id_group(currency, address_id)
        return address_id, id_group

    def get_id_group(self, keyspace, id_):
        if keyspace not in self.parameters:
            raise NetworkNotFoundException(keyspace)
        bucket_size = self.parameters[keyspace]['bucket_size']
        gid = floor(int(id_) / bucket_size)
        if gid.bit_length() > 31:
            # tron tx_id are long and the group is int
            # thus we need to also consider overflows in this case
            # additionally spark does not calculate ids on int basis but
            # based on floats which can lead to rounding errors.
            gid = calculate_id_group_with_overflow(id_, bucket_size)
        return gid

    def get_block_id_group(self, keyspace, id_):
        if keyspace not in self.parameters:
            raise NetworkNotFoundException(keyspace)
        return floor(int(id_) / self.parameters[keyspace]['block_bucket_size'])

    @eth
    def get_tx_id_group(self, keyspace, id_):
        if keyspace not in self.parameters:
            raise NetworkNotFoundException(keyspace)
        return floor(int(id_) / self.parameters[keyspace]['tx_bucket_size'])

    def get_tx_id_group_eth(self, keyspace, id_):
        return self.get_id_group(keyspace, id_)

    async def new_address(self, currency, address):
        data = await self.get_new_address(currency, address)
        if data is None:
            raise AddressNotFoundException(currency, address)
        Values = namedtuple('Values', ['value', 'fiat_values'])
        zero_values = \
            Values(
                value=0,
                fiat_values=[
                    {'code': c.lower(), 'value': 0.0}
                    for c in self.parameters[currency]['fiat_currencies']]
            )
        return {
            'address':
            address,
            'cluster_id':
            data['address_id'],
            'first_tx':
            TxSummary(data['block_id'], data['timestamp'], data['tx_hash']),
            'last_tx':
            TxSummary(data['block_id'], data['timestamp'], data['tx_hash']),
            'no_incoming_txs':
            0,
            'no_outgoing_txs':
            0,
            'total_received':
            zero_values,
            'total_spent':
            zero_values,
            'in_degree':
            0,
            'out_degree':
            0,
            'balance':
            0,
            'status':
            'new'
        }

    async def new_entity(self, currency, address):
        data = await self.new_address(currency, address)
        data['no_addresses'] = 1
        data['root_address'] = address
        return data

    async def get_address_by_address_id(self, currency, address_id):
        address_id_group = self.get_id_group(currency, address_id)
        query = ("SELECT address FROM address WHERE address_id = %s"
                 " AND address_id_group = %s")
        result = await self.execute_async(currency, 'transformed', query,
                                          [address_id, address_id_group])
        result = one(result)
        if not result:
            if not is_eth_like(currency):
                return None
            raise AddressNotFoundException(currency,
                                           address_id,
                                           no_external_txs=True)
        return result["address"]

    async def get_address(self, currency, address):
        address_id, address_id_group = \
            await self.get_address_id_id_group(currency, address)
        query = ("SELECT * FROM address WHERE address_id = %s"
                 " AND address_id_group = %s")
        result = await self.execute_async(currency, 'transformed', query,
                                          [address_id, address_id_group])
        result = one(result)
        if not result:
            if not is_eth_like(currency):
                return None
            raise AddressNotFoundException(currency,
                                           address,
                                           no_external_txs=True)

        return await self.finish_address(currency, result)

    @eth
    async def get_address_entity_id(self, currency, address):
        address_id, address_id_group = \
            await self.get_address_id_id_group(currency, address)

        query = "SELECT cluster_id FROM address WHERE " \
                "address_id_group = %s AND address_id = %s "
        result = await self.execute_async(currency, 'transformed', query,
                                          [address_id_group, address_id])
        result = one(result)
        if not result:
            raise DBInconsistencyException(
                f'address {address} in {currency} with id '
                f'{address_id} and id_group {address_id_group} '
                f'not found in address table')
        return result['cluster_id']

    async def list_address_links(self,
                                 currency,
                                 address,
                                 neighbor,
                                 min_height=None,
                                 max_height=None,
                                 order=None,
                                 page=None,
                                 pagesize=None):
        return await self.list_links(currency,
                                     NodeType.ADDRESS,
                                     address,
                                     neighbor,
                                     min_height=min_height,
                                     max_height=max_height,
                                     order=order,
                                     page=page,
                                     pagesize=pagesize)

    async def list_entity_links(self,
                                currency,
                                address,
                                neighbor,
                                min_height=None,
                                max_height=None,
                                order=None,
                                page=None,
                                pagesize=None):
        return await self.list_links(currency,
                                     NodeType.CLUSTER,
                                     address,
                                     neighbor,
                                     min_height=min_height,
                                     max_height=max_height,
                                     order=order,
                                     page=page,
                                     pagesize=pagesize)

    async def list_links(self,
                         currency,
                         node_type: NodeType,
                         id,
                         neighbor,
                         min_height=None,
                         max_height=None,
                         order=None,
                         page=None,
                         pagesize=None):
        try:
            page = int(page) if page is not None else None
        except ValueError:
            raise BadUserInputException(f"Page {page} is not an integer")

        ascending = order == 'asc'

        if node_type == NodeType.ADDRESS:
            src_node = await self.get_address(currency, id)
            dst_node = await self.get_address(currency, neighbor)
        else:
            src_node = await self.get_entity(currency, id)
            dst_node = await self.get_entity(currency, neighbor)

        if src_node is None:
            raise nodeNotFoundException(currency, node_type, id)

        if dst_node is None:
            raise nodeNotFoundException(currency, node_type, neighbor)

        is_outgoing = src_node['no_outgoing_txs'] < dst_node['no_incoming_txs']

        if is_outgoing:
            first = id
            second = neighbor
            is_outgoing = True
            first_value = 'input_value'
            second_value = 'output_value'
        else:
            first = neighbor
            second = id
            is_outgoing = False
            first_value = 'output_value'
            second_value = 'input_value'

        if is_eth_like(currency):
            token_config = self.get_token_configuration(currency)
            include_assets = list(token_config.keys())
            include_assets.append(currency.upper())
        else:
            include_assets = [currency.upper()]

        tx_id_lower_bound, tx_id_upper_bound = \
            await self.resolve_tx_id_range_by_block(currency,
                                                    min_height,
                                                    max_height)

        final_results = []
        fetch_size = min(pagesize or SMALL_PAGE_SIZE, SMALL_PAGE_SIZE)
        while len(final_results) < fetch_size:
            fs_it = fetch_size - len(final_results)
            results1, new_page = await self.list_address_txs_ordered(
                network=currency,
                node_type=node_type,
                id=first,
                tx_id_lower_bound=tx_id_lower_bound,
                tx_id_upper_bound=tx_id_upper_bound,
                is_outgoing=is_outgoing,
                include_assets=include_assets,
                ascending=ascending,
                page=page,
                fetch_size=fs_it)

            self.logger.debug(f'results1 {len(results1)} {new_page}')

            tx_id = 'transaction_id' if is_eth_like(currency) else 'tx_id'

            first_tx_ids = \
                [(row[tx_id], row['tx_reference']) for row in results1] \
                if is_eth_like(currency) else \
                [(row[tx_id], None) for row in results1]

            assets = set([currency.upper()])
            if is_eth_like(currency):
                for row in results1:
                    assets.add(row['currency'])

            assets = list(assets)

            results2, _ = await self.list_address_txs_ordered(
                network=currency,
                node_type=node_type,
                id=second,
                tx_id_lower_bound=None,
                tx_id_upper_bound=None,
                # is_outgoing=not is_outgoing,
                # fetch both directions regardless, this is needed since for
                # some transactions the total flow is an inflow but it is an
                # outflowat the same time. If we would not fetch both
                # directions we would miss these transactions.
                is_outgoing=None,
                include_assets=assets,
                ascending=ascending,
                tx_ids=first_tx_ids,  # limit second set by tx ids of first set
                page=page,
                fetch_size=fs_it)
            self.logger.debug(f'results2 {len(results2)} {page}')

            if is_eth_like(currency):
                results2 = await self.normalize_address_transactions(
                    currency, results2)
            else:
                results1 = {row[tx_id]: row for row in results1}
                tx_ids = [row[tx_id] for row in results2]
                txs = await self.list_txs_by_ids(currency, tx_ids)

                if len(results2) != len(txs):
                    raise DBInconsistencyException(
                        'result sets for txs intersection not equal')

                # merge address_transactions and raw transaction sets
                for (row, tx) in zip(results2, txs):
                    row[second_value] = row['value']
                    row[first_value] = results1[row[tx_id]]['value']

                    for k, v in tx.items():
                        row[k] = v

            if is_eth_like(currency):
                # TODO probably this check is no longer necessary
                # since we filtered on tx_ref level already
                # in list_address_txs_ordered
                if node_type == NodeType.CLUSTER:
                    neighbor = dst_node['root_address']
                    id = src_node['root_address']
                # Token/Trace transactions might not be between the requested
                # nodes so only keep the relevant ones
                before = len(results2)
                results2 = [
                    tx for tx in results2 if tx["to_address"] == neighbor
                    and tx["from_address"] == id
                ]
                self.logger.info(f'pruned {before - len(results2)}')
            final_results.extend(results2)

            page = new_page
            self.logger.debug(f'next page {page}')
            if page is None:
                break

        self.logger.debug(f'final_results len {len(final_results)}')

        return final_results, str(page) if page is not None else None

    async def list_matching_addresses(self, currency, expression, limit=10):

        prefix_lengths = self.get_prefix_lengths(currency)
        expression_orginal = expression

        postprocess_address = identity1
        if currency == 'trx':
            postprocess_address = partial_tron_to_partial_evm

        expression = postprocess_address(expression)

        if len(expression) < prefix_lengths['address']:
            return []
        norm = identity2
        prefix = self.scrub_prefix(currency, expression)
        prefix = prefix[:prefix_lengths['address']]

        if is_eth_like(currency):
            # eth addresses are case insensitive
            expression = expression.lower()
            norm = address_to_user_format
            prefix = prefix.upper()
        else:
            expression = expression_orginal
        rows = []

        if len(prefix) < 1:
            return []

        async def collect(query):
            paging_state = None
            while len(rows) < limit:
                result = await self.execute_async(currency,
                                                  'transformed',
                                                  query, [prefix],
                                                  paging_state=paging_state)
                if result.is_empty():
                    break
                rows.extend([
                    norm(currency, row['address'])
                    for row in result.current_rows if postprocess_address(
                        norm(currency, row['address'])).startswith(expression)
                ])
                paging_state = result.paging_state
                if paging_state is None:
                    break

        query = "SELECT address FROM address_ids_by_address_prefix "\
                "WHERE address_prefix = %s"

        await collect(query)

        if len(rows) < limit:
            query = "SELECT address FROM new_addresses "\
                    "WHERE address_prefix = %s"
            if self.parameters[currency]["use_delta_updater_v1"]:
                try:
                    await collect(query)
                except InvalidRequest as e:
                    if 'new_addresses' not in str(e):
                        raise e
            rows = sorted(rows)
        return rows[0:limit]

    @eth
    async def get_entity(self, currency, entity):
        entity_id_group = self.get_id_group(currency, entity)
        entity = int(entity)
        query = ("SELECT * FROM cluster "
                 "WHERE cluster_id_group = %s AND cluster_id = %s ")
        result = await self.execute_async(currency, 'transformed', query,
                                          [entity_id_group, entity])
        result = one(result)
        if not result:
            raise ClusterNotFoundException(currency, entity)
        return (await self.finish_entities(currency, [result]))[0]

    @eth
    async def list_entities(self,
                            currency,
                            ids,
                            page=None,
                            pagesize=None,
                            fields=['*']):
        fetch_size = min(pagesize or SMALL_PAGE_SIZE, SMALL_PAGE_SIZE)
        paging_state = page_from_hex(page)
        flds = ','.join(fields)
        query = f"SELECT {flds} FROM cluster"
        has_ids = isinstance(ids, list)
        if has_ids:
            query += " WHERE cluster_id_group = %s AND cluster_id = %s"
            params = [[self.get_id_group(currency, id), id] for id in ids]
            result = await self.concurrent_with_args(currency, 'transformed',
                                                     query, params)
            paging_state = None
        else:
            result = await self.execute_async(currency,
                                              'transformed',
                                              query,
                                              paging_state=paging_state,
                                              fetch_size=fetch_size)
            paging_state = result.paging_state
            result = result.current_rows

        with_txs = '*' in fields \
            or 'first_tx_id' in fields \
            or 'last_tx_id' in fields
        return await self.finish_entities(currency, result, with_txs), \
            to_hex(paging_state)

    @eth
    async def list_entity_addresses(self,
                                    currency,
                                    entity,
                                    page=None,
                                    pagesize=None):
        paging_state = page_from_hex(page)
        entity_id_group = self.get_id_group(currency, entity)
        entity = int(entity)
        query = ("SELECT address_id FROM cluster_addresses "
                 "WHERE cluster_id_group = %s AND cluster_id = %s")
        fetch_size = min(pagesize or SMALL_PAGE_SIZE, SMALL_PAGE_SIZE)
        results = await self.execute_async(currency,
                                           'transformed',
                                           query, [entity_id_group, entity],
                                           paging_state=paging_state,
                                           fetch_size=fetch_size)
        if results is None:
            return []

        params = [(self.get_id_group(currency,
                                     row['address_id']), row['address_id'])
                  for row in results.current_rows]
        query = "SELECT * FROM address WHERE " \
                "address_id_group = %s and address_id = %s"
        result = await self.concurrent_with_args(currency, 'transformed',
                                                 query, params)

        return await self.finish_addresses(currency, result), \
            to_hex(results.paging_state)

    async def list_neighbors(self, currency, id, is_outgoing,
                             node_type: NodeType, targets, page, pagesize):
        orig_node_type = node_type
        orig_id = id
        if node_type == NodeType.ADDRESS:
            id = await self.get_address_id(currency, id)
            if id is None:
                # check if new address exists
                if await self.get_new_address(currency, orig_id):
                    return [], None
                raise AddressNotFoundException(currency, orig_id)

        elif node_type == NodeType.CLUSTER:
            id = int(id)
            if is_eth_like(currency):
                node_type = NodeType.ADDRESS

        if is_outgoing:
            direction, this, that = ('outgoing', 'src', 'dst')
        else:
            direction, this, that = ('incoming', 'dst', 'src')

        id_group = self.get_id_group(currency, id)
        base_parameters = [id_group, id]
        has_targets = isinstance(targets, list)
        sec_condition = ''
        if is_eth_like(currency):
            secondary_id_group = \
                await self.get_id_secondary_group_eth(
                    currency,
                    f'address_{direction}_relations',
                    id_group)
            sec_in = self.sec_in(secondary_id_group)
            sec_condition = \
                f' AND {this}_address_id_secondary_group in %s'
            base_parameters.append(sec_in)

        basequery = (f"SELECT * FROM {node_type}_{direction}_relations WHERE "
                     f"{this}_{node_type}_id_group = %s AND "
                     f"{this}_{node_type}_id = %s {sec_condition}")
        params = base_parameters.copy()
        if has_targets:
            if len(targets) == 0:
                return None, None

            query = basequery.replace('*', f'{that}_{node_type}_id')
            targets = ValueSequence(targets)
            query += f' AND {that}_{node_type}_id in %s'
            params.append(targets)
        else:
            query = basequery
        fetch_size = min(pagesize or BIG_PAGE_SIZE, BIG_PAGE_SIZE)
        paging_state = page_from_hex(page)
        results = await self.execute_async(currency,
                                           'transformed',
                                           query,
                                           params,
                                           paging_state=paging_state,
                                           fetch_size=fetch_size)
        paging_state = results.paging_state
        results = results.current_rows
        if has_targets:
            params = []
            query = basequery + f" AND {that}_{node_type}_id = %s"
            for row in results:
                p = base_parameters.copy()
                p.append(row[f'{that}_{node_type}_id'])
                params.append(p)
            results = await self.concurrent_with_args(currency, 'transformed',
                                                      query, params)

        if orig_node_type == NodeType.CLUSTER and is_eth_like(currency):
            for neighbor in results:
                neighbor['address_id'] = \
                    neighbor[that + '_cluster_id'] = \
                    neighbor[that + '_address_id']

        if orig_node_type == NodeType.ADDRESS:
            ids = [row[that + '_address_id'] for row in results]
            addresses = await self.get_addresses_by_ids(currency,
                                                        ids,
                                                        address_only=True)

            if len(addresses) != len(ids):
                address_ids = [address['address'] for address in addresses]
                self.log_missing(address_ids, ids, node_type, query, params)

            for (row, address) in zip(results, addresses):
                row[that + '_address'] = address['address']

        field = 'value' if is_eth_like(currency) else 'estimated_value'
        for neighbor in results:
            neighbor['value'] = \
                self.markup_currency(currency, neighbor[field])
            if "token_values" in neighbor and neighbor[
                    "token_values"] is not None:
                neighbor['token_values'] = \
                    {k: self.markup_currency(currency, v)
                     for k, v in neighbor["token_values"].items()}

        if is_eth_like(currency):
            for row in results:
                row['address_id'] = row[that + '_address_id']

        return results, to_hex(paging_state)

    @eth
    async def get_spending_txs(self, currency, tx_hash, io_index):
        if not self.parameters[currency]["tx_graph_available"]:
            # for value err msg is visible to the user.
            raise BadUserInputException(
                f"{currency} does not yet support transaction linking.")
        prefix = self.get_prefix_lengths(currency)
        if isinstance(io_index, int):
            query = ('SELECT * from transaction_spending where '
                     'spending_tx_prefix=%s and spending_tx_hash=%s '
                     'and spending_input_index=%s')
            params = [
                tx_hash[:prefix['tx']],
                bytearray.fromhex(tx_hash), io_index
            ]
        else:
            query = ('SELECT * from transaction_spending where '
                     'spending_tx_prefix=%s and spending_tx_hash=%s')
            params = [tx_hash[:prefix['tx']], bytearray.fromhex(tx_hash)]

        result = await self.execute_async(currency, 'raw', query, params)
        return result

    async def get_spending_txs_eth(self, currency, tx_hash, io_index):
        # we raise a value error here,
        # that makes the error msg visible to the user.
        raise BadUserInputException(
            f"Currency {currency} does not support transaction level linking")

    @eth
    async def get_spent_in_txs(self, currency, tx_hash, io_index):
        if not self.parameters[currency]["tx_graph_available"]:
            # for value err msg is visible to the user.
            raise BadUserInputException(
                f"{currency} does not yet support transaction linking.")
        prefix = self.get_prefix_lengths(currency)
        if isinstance(io_index, int):
            query = ('SELECT * from transaction_spent_in where '
                     'spent_tx_prefix=%s and spent_tx_hash=%s '
                     'and spent_output_index=%s')
            params = [
                tx_hash[:prefix['tx']],
                bytearray.fromhex(tx_hash), io_index
            ]
        else:
            query = ('SELECT * from transaction_spent_in where '
                     'spent_tx_prefix=%s and spent_tx_hash=%s')
            params = [tx_hash[:prefix['tx']], bytearray.fromhex(tx_hash)]

        result = await self.execute_async(currency, 'raw', query, params)
        return result

    async def get_spent_in_txs_eth(self, currency, tx_hash, io_index):
        # we raise a value error here,
        # that makes the error msg visible to the user.
        raise BadUserInputException(
            f"Currency {currency} does not support transaction level linking")

    @eth
    def get_tx(self, currency, tx_hash):
        return self.get_tx_by_hash(currency, tx_hash)

    @eth
    async def list_token_txs(self, currency, tx_hash, log_index=None):
        return []

    async def list_token_txs_eth(self, currency, tx_hash, log_index=None):
        tx = await self.get_tx(currency, tx_hash)
        return await self.fetch_token_transactions(currency, tx, log_index)

    async def fetch_token_transaction(self, currency, tx, log_index):
        r = await self.fetch_token_transactions(currency, tx, log_index)
        if len(r) != 1:
            raise NotFoundException(f"Found {len(r)} logs for token "
                                    f"tx {tx['tx_hash']}:"
                                    f"{log_index}")
        return r[0]

    async def fetch_token_transactions(self, currency, tx, log_index=None):
        transfer_topic = bytes_from_hex("0xddf252ad1be2c89b69c2b068fc378da"
                                        "a952ba7f163c4a11628f55a4df523b3ef")
        token_tx_logs = await self.get_logs_in_block_eth(currency,
                                                         tx["block_id"],
                                                         topic=transfer_topic,
                                                         log_index=log_index)
        supported_tokens = {
            v["token_address"]: v
            for v in self.get_token_configuration(currency).values()
        }

        logs_to_decode = [
            tt for tt in token_tx_logs.current_rows
            if tt["address"] in supported_tokens
            and tt["tx_hash"] == tx["tx_hash"]
        ]
        decoded_token_txs = zip(decode_db_logs(logs_to_decode), logs_to_decode)

        return [
            build_token_tx(supported_tokens[log["address"]]["currency_ticker"],
                           tx, token_tx, log)
            for (token_tx, log) in decoded_token_txs
        ]

    async def fetch_transaction_trace(self, currency, tx, trace_index):
        r = await self.get_traces_in_block(currency, tx["block_id"],
                                           trace_index)
        result = r.current_rows
        if len(result) != 1:
            raise NotFoundException(f"Found {len(result)} trace in "
                                    f"tx {tx['tx_hash']}:"
                                    f"{trace_index}")
        return result[0]

    async def get_logs_in_block_eth(self,
                                    currency,
                                    block_id,
                                    topic=None,
                                    log_index=None):
        block_group = self.get_block_id_group(currency, block_id)
        query = ('SELECT * from log where '
                 'block_id_group=%s and block_id=%s')
        params = [block_group, block_id]

        if topic is not None:
            query += " and topic0=%s"
            params += [topic]

        if log_index is not None:
            query += " and log_index=%s"
            params += [log_index]

        return await self.execute_async(currency, 'raw', query, params)

    async def get_traces_in_block(self, currency, block_id, trace_index=None):
        block_group = self.get_block_id_group(currency, block_id)
        query = ('SELECT * from trace where '
                 'block_id_group=%s and block_id=%s')

        params = [block_group, block_id]
        if trace_index is not None:
            query += " and trace_index=%s"
            params += [trace_index]

        return await self.execute_async(currency, 'raw', query, params)

    async def list_matching_txs(self, currency, expression, limit):
        prefix_lengths = self.get_prefix_lengths(currency)

        # should be safe for btc txs too. They are hex encoded.
        # so 0x should never be content. For base58 encoded btc adresses
        # there also no 0 character used.
        if expression.startswith("0x"):
            expression = expression[2:]

        if len(expression) < prefix_lengths['tx']:
            return []

        if is_eth_like(currency):
            prefix = expression[:prefix_lengths['tx']].upper()
            kind = 'transformed'
            key = 'transaction'
            query = ('SELECT transaction from transaction_ids_by_transaction_'
                     'prefix where transaction_prefix = %s')
        else:
            prefix = expression[:prefix_lengths['tx']]
            kind = 'raw'
            key = 'tx_hash'
            query = ('SELECT tx_hash from transaction_by_tx_prefix where '
                     'tx_prefix=%s')

        paging_state = True
        rows = []
        while paging_state and len(rows) < limit:
            if paging_state is True:
                paging_state = None
            result = await self.execute_async(currency,
                                              kind,
                                              query, [prefix],
                                              paging_state=paging_state)
            if result.is_empty():
                break

            # fix leading zero handling, assumption all tx hashes are 32 bytes
            # which is true for btc-like currencies and ethereum
            txs = [
                row[key].rjust(32, b'\x00').hex()
                for row in result.current_rows
            ]

            rows += [
                tx for tx in txs if tx.startswith(expression)
                or tx.lstrip('0').startswith(expression.lstrip('0'))
            ]

            paging_state = result.paging_state

        return rows[0:limit]

    def scrub_prefix(self, currency, expression):
        if isinstance(expression, bytes):
            expression = bytes_to_hex(expression)

        if currency == 'eth':
            expression = strip_0x(expression)

        if currency not in self.parameters:
            raise NetworkNotFoundException(currency)

        bech32_prefix = self.parameters[currency].get('bech_32_prefix', '')
        return expression[len(bech32_prefix):] \
            if expression.startswith(bech32_prefix) \
            else expression

    @eth
    async def list_txs_by_hashes(self,
                                 currency,
                                 hashes,
                                 include_token_txs=False):
        prefix = self.get_prefix_lengths(currency)
        params = [[hash[:prefix['tx']],
                   bytearray.fromhex(hash)] for hash in hashes]
        statement = ('SELECT tx_id from transaction_by_tx_prefix where '
                     'tx_prefix=%s and tx_hash=%s')
        result = await self.concurrent_with_args(currency, 'raw', statement,
                                                 params)
        ids = (tx['tx_id'] for tx in result)
        return await self.list_txs_by_ids(currency,
                                          ids,
                                          include_token_txs=include_token_txs)

    @eth
    async def get_tx_by_hash(self, currency, tx_hash: bytes):
        prefix = self.get_prefix_lengths(currency)
        try:
            params = [tx_hash[:prefix['tx']], bytearray.fromhex(tx_hash)]
        except ValueError:
            raise BadUserInputException(
                f"{tx_hash} does not look like a valid "
                "transaction hash.")
        statement = ('SELECT tx_id from transaction_by_tx_prefix where '
                     'tx_prefix=%s and tx_hash=%s')
        result = await self.execute_async(currency, 'raw', statement, params)
        result = one(result)
        if not result:
            raise TransactionNotFoundException(currency, tx_hash)
        result = await self.get_tx_by_id(currency, result['tx_id'])
        if not result:
            raise DBInconsistencyException(
                f"transaction {tx_hash} with id {result['tx_id']} in network "
                f'{currency} not found')
        return result

    @eth
    async def list_txs_by_ids(self,
                              currency,
                              ids,
                              filter_empty=True,
                              include_token_txs=False):
        params = ([self.get_tx_id_group(currency, id), id] for id in ids)
        statement = ('SELECT * FROM transaction WHERE '
                     'tx_id_group = %s and tx_id = %s')
        return await self.concurrent_with_args(currency,
                                               'raw',
                                               statement,
                                               params,
                                               filter_empty=filter_empty)

    @eth
    async def get_tx_by_id(self, currency, id):
        params = [self.get_tx_id_group(currency, id), id]
        statement = ('SELECT * FROM transaction WHERE '
                     'tx_id_group = %s and tx_id = %s')
        return (await self.execute_async(currency, 'raw', statement,
                                         params)).one()

    async def finish_entities(self, currency, rows, with_txs=True):
        aws = [
            self.finish_entity(currency, row, with_txs=with_txs)
            for row in rows
        ]
        return await asyncio.gather(*aws)

    @eth
    async def finish_entity(self, currency, row, with_txs=True):
        a = await self.get_addresses_by_ids(currency, [row['cluster_id']],
                                            address_only=True)
        row['root_address'] = a[0]['address']
        return await self.finish_address(currency, row, with_txs)

    async def finish_entity_eth(self, currency, row, with_txs=True):
        row['root_address'] = row['address']
        return await self.finish_address(currency, row, with_txs)

    async def finish_addresses(self, currency, rows, with_txs=True):
        aws = [
            self.finish_address(currency, row, with_txs=with_txs)
            for row in rows
        ]
        return await asyncio.gather(*aws)

    @eth
    async def finish_address(self, currency, row, with_txs=True):
        row['total_received'] = \
            self.markup_currency(currency, row['total_received'])
        row['total_spent'] = \
            self.markup_currency(currency, row['total_spent'])

        await self.add_balance(currency, row)

        if not with_txs:
            return row

        aws = [
            self.get_tx_by_id(currency, id)
            for id in [row['first_tx_id'], row['last_tx_id']]
        ]
        [tx1, tx2] = await asyncio.gather(*aws)

        if not tx1 or not tx2:
            raise DBInconsistencyException(
                f"first or last transaction not found as referenced by {row}")

        row['first_tx'] = TxSummary(tx_hash=tx1['tx_hash'],
                                    timestamp=tx1['timestamp'],
                                    height=tx1['block_id'])

        row['last_tx'] = TxSummary(tx_hash=tx2['tx_hash'],
                                   timestamp=tx2['timestamp'],
                                   height=tx2['block_id'])

        if 'address' in row:
            is_dirty = await self.is_address_dirty(currency, row['address'])
            row['status'] = 'dirty' if is_dirty else 'clean'

        return row

    async def finish_address_eth(self, currency, row, with_txs=True):
        row['cluster_id'] = row['address_id']
        row['total_received'] = \
            self.markup_currency(currency, row['total_received'])
        row['total_spent'] = \
            self.markup_currency(currency, row['total_spent'])

        tr = row['total_tokens_received']
        if tr is not None:
            row['total_tokens_received'] = {
                k: self.markup_currency(currency, v)
                for k, v in tr.items()
            }

        ts = row['total_tokens_spent']
        if ts is not None:
            row['total_tokens_spent'] = {
                k: self.markup_currency(currency, v)
                for k, v in ts.items()
            }

        await self.add_balance(currency, row)

        if not with_txs:
            return row

        aws = [
            self.get_tx_by_id(currency, id)
            for id in [row['first_tx_id'], row['last_tx_id']]
        ]

        [tx1, tx2] = await asyncio.gather(*aws)

        if not tx1 or not tx2:
            raise DBInconsistencyException(
                f"first or last transaction not found as referenced by {row}")

        row['first_tx'] = TxSummary(tx_hash=tx1['tx_hash'],
                                    timestamp=tx1['block_timestamp'],
                                    height=tx1['block_id'])

        row['last_tx'] = TxSummary(tx_hash=tx2['tx_hash'],
                                   timestamp=tx2['block_timestamp'],
                                   height=tx2['block_id'])

        is_dirty = await self.is_address_dirty(currency, row['address'])
        row['status'] = 'dirty' if is_dirty else 'clean'

        return row

    async def is_address_dirty(self, currency, address):
        if not self.parameters[currency]["use_delta_updater_v1"]:
            return False

        prefix = self.scrub_prefix(currency, address)
        if is_eth_like(currency):
            prefix = prefix.upper()
        prefix_length = self.get_prefix_lengths(currency)['address']
        query = ("SELECT address FROM dirty_addresses "
                 "WHERE address_prefix = %s AND address = %s")
        try:
            result = await self.execute_async(
                currency, 'transformed', query,
                [prefix[:prefix_length], address])

            result = one(result)
            if result:
                return True
        except InvalidRequest as e:
            if 'dirty_addresses' not in str(e):
                raise e

        return False

    @eth
    async def add_balance(self, currency, row):
        row['balance'] = row['total_received'].value - row['total_spent'].value

    async def add_balance_eth(self, currency, row):
        token_config = self.get_token_configuration(currency)
        token_currencies = list(token_config.keys())
        balance_currencies = [currency.upper()] + token_currencies

        balance_provider = self.get_balance_provider(currency)

        results = None
        if balance_provider is not None:
            # load balance from alternative provider.
            try:
                results = await balance_provider(currency, row["address"],
                                                 token_config)
            except Exception as e:
                self.logger.warning(
                    f"Could not fetch balances over alternative provider: {e}")

        if results is None:
            # load results from gs database
            if 'address_id_group' not in row:
                row['address_id_group'] = \
                    self.get_id_group(currency, row['address_id'])
            query = 'SELECT balance from balance where address_id=%s '\
                    'and address_id_group=%s ' \
                    "and currency=%s"

            results = {
                c: one(await self.execute_async(
                    currency, 'transformed', query,
                    [row['address_id'], row['address_id_group'], c]))
                for c in balance_currencies
            }

        if results[currency.upper()] is None:
            results[currency.upper()] = {
                'balance':
                row['total_received'].value - row['total_spent'].value
            }
        row['balance'] = results[currency.upper()]["balance"]

        if currency == "trx":
            # our self compute balances can get negative for now
            # since we have not implemented all special tx types
            # in our logic yet
            row['balance'] = max(row['balance'], 0)

        # TODO: Some accounts have negative balances, this does not make sense.
        # for now we cap with 0 in case of negative
        # Exp. for now is that we either lost some token txs somewhere or
        # the events do not represent all transfers
        # (e.g. the initial distribution) was hardcoded in the token contract
        # so no events exist. Future solution to have accurate balances
        # would be to query the node directly
        token_balances = {
            c: max(b["balance"], 0)
            for c, b in results.items() if c in token_config and b is not None
        }
        row["token_balances"] = None if len(
            token_balances) == 0 else token_balances

    # ETH Variants

    def scrub_prefix_eth(self, currency, expression):
        # remove 0x prefix
        expression = bytes_to_hex(expression)
        if expression.startswith("0x"):
            return expression[2:]
        else:
            return expression

    async def get_block_eth(self, currency, height):
        block_group = self.get_block_id_group(currency, height)
        query = ("SELECT * FROM block WHERE block_id_group = %s and"
                 " block_id = %s")
        return (await self.execute_async(currency, 'raw', query,
                                         [block_group, height])).one()

    @alru_cache(maxsize=1000)
    async def get_block_timestamp_eth(self, currency, height):
        block_group = self.get_block_id_group(currency, height)
        query = ("SELECT timestamp FROM block WHERE block_id_group = %s and"
                 " block_id = %s")
        return (await self.execute_async(currency, 'raw', query,
                                         [block_group, height])).one()

    # entity = address_id
    async def get_entity_eth(self, currency, entity):
        # mockup entity by address
        id_group = self.get_id_group(currency, entity)
        query = ("SELECT * FROM address WHERE "
                 "address_id_group = %s AND address_id = %s")
        result = await self.execute_async(currency, 'transformed', query,
                                          [id_group, entity])
        result = one(result)
        if not result:
            return None

        entity = (await self.finish_entities(currency, [result]))[0]
        entity['cluster_id'] = entity['address_id']
        entity['no_addresses'] = 1
        entity.pop('address', None)
        return entity

    async def list_entities_eth(self,
                                currency,
                                ids,
                                page=None,
                                pagesize=None,
                                fields=['*']):
        fields = ['address_id' if i == 'cluster_id' else i for i in fields]
        if '*' not in fields:
            fields += ['address_id', 'address_id_group']
        flds = ','.join(fields)
        query = f"SELECT {flds} FROM address"
        has_ids = isinstance(ids, list)
        if has_ids:
            query += " WHERE address_id_group = %s AND address_id = %s"
            params = [[self.get_id_group(currency, id), id] for id in ids]
            result = await self.concurrent_with_args(currency, 'transformed',
                                                     query, params)
            paging_state = None
        else:
            fetch_size = min(pagesize or SMALL_PAGE_SIZE, SMALL_PAGE_SIZE)
            result = await self.execute_async(currency,
                                              'transformed',
                                              query,
                                              paging_state=page_from_hex(page),
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

    async def get_address_entity_id_eth(self, currency, address):
        address_id = await self.get_address_id(currency, address)
        if address_id is None:
            raise AddressNotFoundException(currency,
                                           address,
                                           no_external_txs=True)
        return address_id

    async def get_id_secondary_group_eth(self, currency, table, id_group):
        column_prefix = ''
        if table == 'address_incoming_relations':
            column_prefix = 'dst_'
        elif table == 'address_outgoing_relations':
            column_prefix = 'src_'

        query = (f"SELECT max_secondary_id FROM {table}_"
                 f"secondary_ids WHERE {column_prefix}address_id_group = %s")
        result = (await self.execute_async(currency, 'transformed', query,
                                           [id_group])).one()
        return 0 if result is None else \
            result['max_secondary_id']

    async def list_address_txs_ordered(
            self,
            network: str,
            node_type: NodeType,
            id,
            tx_id_lower_bound: Optional[int],
            tx_id_upper_bound: Optional[int],
            is_outgoing: Optional[bool],
            include_assets: Sequence[Tuple[str, bool]],
            page: Optional[int],
            fetch_size: int,
            cols: Optional[Sequence[str]] = None,
            tx_ids: Optional[Sequence[Tuple[int, Optional[dict]]]] = None,
            ascending: bool = False) -> Tuple[Sequence[dict], Optional[int]]:
        """Loads a address transactions in execution order
        it allows to only get out- or incoming transaction or only
        transactions of a certain asset (token), for a given address id

        Args:
            network (str): base currency / network
            node_type (str): NodeType (ADDRESS/CLUSTER)
            item_id (int): address/cluster id
            item_id_group (int): address/cluster id group
            tx_id_lower_bound (Optional[int]): tx id lower bound
            tx_id_upper_bound (Optional[int]): tx id upper bound
            is_outgoing (Optional[bool]): if True fetch only outgoing, if False
                fetch only incoming, if None fetch both directions
            include_assets (Sequence[Tuple[str, bool]]): a list of tuples with
                assets to include
            page (Optional[int]): a page id (tx id bound)
            fetch_size (int): how much to fetch per page
            cols (Optional[Sequence[str]], optional): which columns to select
                None means *
            tx_ids (Optional[Sequence[int]]): limit result to given tx_ids
            ascending (Optional[bool]): sort list ascending if True or
                descending if False
        """

        if node_type == NodeType.ADDRESS:
            item_id, item_id_group = \
                await self.get_address_id_id_group(network, id)
        else:
            if is_eth_like(network):
                node_type = NodeType.ADDRESS
            item_id = id
            item_id_group = self.get_id_group(network, id)

        item_id_secondary_group = [0]
        if is_eth_like(network):
            secondary_id_group = \
                await self.get_id_secondary_group_eth(network,
                                                      'address_transactions',
                                                      item_id_group)

            item_id_secondary_group = self.sec_in(secondary_id_group)

        directions = [is_outgoing
                      ] if is_outgoing is not None else [False, True]
        results = []
        """
            Keep retrieving pages until the demanded fetch_size is fulfilled
            or there are no more pages
        """
        while len(results) < fetch_size:
            fs_it = fetch_size - len(results)

            if not ascending:
                this_tx_id_lower_bound = tx_id_lower_bound
                if page is not None and tx_id_upper_bound is not None:
                    this_tx_id_upper_bound = min(page, tx_id_upper_bound)
                elif tx_id_upper_bound is not None:
                    this_tx_id_upper_bound = tx_id_upper_bound
                else:
                    this_tx_id_upper_bound = page
            else:
                this_tx_id_upper_bound = tx_id_upper_bound
                if page is not None and tx_id_lower_bound is not None:
                    this_tx_id_lower_bound = max(page, tx_id_lower_bound)
                elif tx_id_lower_bound is not None:
                    this_tx_id_lower_bound = tx_id_lower_bound
                else:
                    this_tx_id_lower_bound = page

            # prebuild useful conditions, dependent on loop
            has_upper_bound = this_tx_id_upper_bound is not None

            has_lower_bound = this_tx_id_lower_bound is not None

            # divide fetch_size by number of result sets
            fs_junk = ceil(fs_it / (len(include_assets) + 2))

            cql_stmt = build_select_address_txs_statement(
                network,
                node_type,
                cols,
                with_lower_bound=has_lower_bound,
                with_upper_bound=has_upper_bound,
                limit=fs_junk,
                ascending=ascending,
                with_tx_id=(tx_ids is not None))

            # prepare parameters for the query junks one for each direction
            # and asset tuple
            params_junks = [{
                "id": item_id,
                "g_id": item_id_group,
                "tx_id_lower_bound": this_tx_id_lower_bound,
                "tx_id_upper_bound": this_tx_id_upper_bound,
                "s_d_group": s_d_group,
                "currency": asset,
                "is_outgoing": is_outgoing,
                "tx_id": tx_id,
                "tx_ref": tx_ref
            } for is_outgoing, asset, s_d_group, (tx_id, tx_ref) in product(
                directions, include_assets, item_id_secondary_group, [(
                    0, None)] if tx_ids is None else tx_ids)]

            def tx_ref_match(a, b):
                return a[0] == b[0] and \
                    a[1] == b[1]

            async def fetch(stmt, params):
                res = await self.execute_async(network, 'transformed',
                                               cql_stmt, params)
                if params['tx_ref'] is None:
                    return res

                res.current_rows = [
                    r for r in res
                    if tx_ref_match(r['tx_reference'], params['tx_ref'])
                ]
                return res

            # run one query per direction, asset and secondary group id
            aws = [fetch(cql_stmt, p) for p in params_junks]

            # collect and merge results
            more_results, page = merge_address_txs_subquery_results(
                [r.current_rows for r in await asyncio.gather(*aws)],
                ascending,
                fs_it,
                'transaction_id' if is_eth_like(network) else 'tx_id',
                fetched_limit=fs_junk)

            self.logger.debug(f'list tx ordered page {page}')
            self.logger.debug(f'more_results len {len(more_results)}')

            results.extend(more_results)
            if page is None:
                # no more data expected end loop
                break

        return results, page

    async def list_txs_by_node_type_eth(self,
                                        currency,
                                        node_type,
                                        address,
                                        direction,
                                        min_height=None,
                                        max_height=None,
                                        order=None,
                                        token_currency=None,
                                        page=None,
                                        pagesize=None):
        try:
            page = int(page) if page is not None else None
        except ValueError:
            raise BadUserInputException(f"Page {page} is not an integer")
        ascending = order == 'asc'

        if node_type == NodeType.CLUSTER:
            node_type = NodeType.ADDRESS
            address = await self.get_address_by_address_id(currency, address)

        if not token_currency:
            token_config = self.get_token_configuration(currency)
            include_assets = list(token_config.keys())
            include_assets.append(currency.upper())
        else:
            include_assets = [token_currency.upper()]

        first_tx_id, upper_bound = \
            await self.resolve_tx_id_range_by_block(currency,
                                                    min_height,
                                                    max_height)

        fetch_size = min(pagesize or BIG_PAGE_SIZE, BIG_PAGE_SIZE)

        results, paging_state = await self.list_address_txs_ordered(
            network=currency,
            node_type=node_type,
            id=address,
            tx_id_lower_bound=first_tx_id,
            tx_id_upper_bound=upper_bound,
            is_outgoing=(direction == 'out'
                         if direction is not None else None),
            include_assets=include_assets,
            ascending=ascending,
            page=page,
            fetch_size=fetch_size)

        results = await self.normalize_address_transactions(currency, results)

        for row in results:
            row['value'] *= (-1 if row['is_outgoing'] else 1)

        return results, str(paging_state) if paging_state is not None else None

    async def normalize_address_transactions(self, currency, txs):
        use_legacy_log_index = self.parameters[currency][
            "use_legacy_log_index"]

        tx_ids = [tx['transaction_id'] for tx in txs]

        full_txs = {
            tx_id: tx_row
            for tx_id, tx_row in zip(
                tx_ids, await self.list_txs_by_ids(currency, tx_ids))
        }
        for addr_tx in txs:
            # fix log index field with new tx_refstruct
            if not use_legacy_log_index:
                addr_tx["log_index"] = addr_tx["tx_reference"].log_index
                addr_tx["trace_index"] = addr_tx["tx_reference"].trace_index

            full_tx = full_txs[addr_tx['transaction_id']]
            if addr_tx["log_index"] is not None:
                token_tx = await self.fetch_token_transaction(
                    currency, full_tx, addr_tx["log_index"])

                addr_tx['to_address'] = token_tx['to_address']
                addr_tx['from_address'] = token_tx['from_address']
                addr_tx['currency'] = token_tx["currency"]
                addr_tx['token_tx_id'] = addr_tx["log_index"]
                addr_tx["type"] = "erc20"
                value = token_tx['value']

            elif currency == "trx" and addr_tx["trace_index"] is not None:
                trace = await self.fetch_transaction_trace(
                    currency, full_tx, addr_tx["trace_index"])

                addr_tx['from_address'] = trace['caller_address']
                addr_tx['to_address'] = trace['transferto_address']
                addr_tx["type"] = "internal"
                value = trace["call_value"]
            elif currency == "eth" and addr_tx["trace_index"] is not None:
                trace = await self.fetch_transaction_trace(
                    currency, full_tx, addr_tx["trace_index"])

                addr_tx['from_address'] = trace['from_address']
                addr_tx['to_address'] = trace['to_address']
                addr_tx["type"] = "internal"
                value = trace["value"]
            else:
                addr_tx['to_address'] = full_tx['to_address']
                addr_tx['from_address'] = full_tx['from_address']
                addr_tx['currency'] = currency
                addr_tx["type"] = "external"
                value = full_tx['value']

            contract_creation = full_tx.get('contract_creation', None)

            addr_tx['contract_creation'] = contract_creation
            addr_tx['tx_hash'] = full_tx['tx_hash']
            addr_tx['height'] = full_tx['block_id']

            addr_tx['timestamp'] = full_tx['block_timestamp']
            addr_tx['value'] = value
            addr_tx.pop("log_index")

            await self.fix_timestamp(currency,
                                     addr_tx,
                                     timestamp_col="timestamp",
                                     block_id_col="height")
        return txs

    async def list_txs_by_ids_eth(self,
                                  currency,
                                  ids,
                                  include_token_txs=False):
        params = [[self.get_tx_id_group(currency, id), id] for id in ids]
        statement = (
            'SELECT transaction from transaction_ids_by_transaction_id_group'
            ' where transaction_id_group = %s and transaction_id = %s')
        result = await self.concurrent_with_args(currency,
                                                 'transformed',
                                                 statement,
                                                 params,
                                                 filter_empty=False)

        return await self.list_txs_by_hashes(
            currency, [row['transaction'] for row in result],
            include_token_txs=include_token_txs)

    async def get_tx_by_id_eth(self, currency, id):
        params = [self.get_tx_id_group(currency, id), id]
        statement = (
            'SELECT transaction from transaction_ids_by_transaction_id_group'
            ' where transaction_id_group = %s and transaction_id = %s')
        result = await self.execute_async(currency, 'transformed', statement,
                                          params)
        result = one(result)
        if not result:
            return None
        try:
            return \
                await self.get_tx_by_hash_eth(currency, result['transaction'])
        except TransactionNotFoundException:
            raise DBInconsistencyException(
                f"transaction {bytes_to_hex(result['transaction'])} "
                f"with id {id} in network {currency} not found')")

    async def list_txs_by_hashes_eth(self,
                                     currency,
                                     hashes,
                                     include_token_txs=False):
        prefix = self.get_prefix_lengths(currency)
        params = [[hash.hex()[:prefix['tx']], hash] for hash in hashes]
        statement = ('SELECT tx_hash, block_id, block_timestamp, value, '
                     'from_address, to_address, receipt_contract_address from '
                     'transaction where tx_hash_prefix=%s and tx_hash=%s')
        result = await self.concurrent_with_args(currency, 'raw', statement,
                                                 params)

        result_with_tokens = []
        for row in result:

            to_address = row['to_address']
            if to_address is None:
                # this is a contract creation transaction
                # set recipient to newly created contract
                # and mark tx as creation
                row['to_address'] = row['receipt_contract_address']
                row['contract_creation'] = True
            else:
                # normal transaction
                row['to_address'] = to_address
                # result['contract_creation'] = False

            result_with_tokens.append(row)
            if include_token_txs:
                token_txs = await self.fetch_token_transactions(currency, row)
                for ttx in token_txs:
                    result_with_tokens.append(ttx)

        return result_with_tokens

    async def get_tx_by_hash_eth(self, currency, tx_hash):
        prefix = self.get_prefix_lengths(currency)
        try:
            params = [tx_hash.hex()[:prefix['tx']], tx_hash]
        except ValueError:
            raise BadUserInputException(
                f"{tx_hash} does not look like a valid "
                "transaction hash.")
        statement = ('SELECT tx_hash, block_id, block_timestamp, value, '
                     'from_address, to_address, receipt_contract_address from '
                     'transaction where tx_hash_prefix=%s and tx_hash=%s')

        result = await self.execute_async(currency, 'raw', statement, params)
        result = one(result)

        if not result:
            raise TransactionNotFoundException(currency, tx_hash)

        await self.fix_timestamp(currency, result)

        to_address = result['to_address']
        if to_address is None:
            # this is a contract creation transaction
            # set recipient to newly created contract and mark tx as creation
            result['to_address'] = result['receipt_contract_address']
            result['contract_creation'] = True
        else:
            # normal transaction
            result['to_address'] = to_address
            # result['contract_creation'] = False
        return result

    def get_tx_eth(self, currency, tx_hash: str):
        return self.get_tx_by_hash(currency, tx_hash_from_hex(tx_hash))

    async def list_entity_addresses_eth(self,
                                        currency,
                                        entity,
                                        page=None,
                                        pagesize=None):
        addresses = await self.get_addresses_by_ids(currency, [entity])
        return await self.finish_addresses(currency, addresses), None

    def markup_values(self, currency, fiat_values):
        values = []
        fcurs = self.parameters[currency]['fiat_currencies']

        if fiat_values is None:
            fiat_values = [0.0 for _ in fcurs]

        for (fiat, curr) in zip(fiat_values, fcurs):
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

    def sec_in(self, id):
        return ValueSequence(range(0, id + 1))

    def log_missing(self, ids1, ids2, node_type, query, params):
        missing = []
        for id in ids2:
            if id not in ids1:
                missing.append(id)
        self.logger.critical(f'nodes existing in `{query}` {params} but not '
                             f'in {node_type} table: {missing}')
