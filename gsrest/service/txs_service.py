import asyncio
from gsrest.db import get_connection
from openapi_server.models.txs import Txs
from openapi_server.models.tx_utxo import TxUtxo
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.tx_value import TxValue
from gsrest.service.rates_service import get_rates, list_rates
from gsrest.util.values import convert_value


def from_row(currency, row, rates):
    if currency == 'eth':
        return TxAccount(
            tx_hash=row['tx_hash'].hex(),
            timestamp=row['block_timestamp'],
            height=row['block_id'],
            value=convert_value(currency, row['value'], rates))
    return TxUtxo(
            tx_hash=row['tx_hash'].hex(),
            coinbase=row['coinbase'],
            height=row['block_id'],
            inputs=io_from_rows(currency, row['inputs'], rates)
            if row['inputs'] else [],
            outputs=io_from_rows(currency, row['outputs'], rates)
            if row['outputs'] else [],
            timestamp=row['timestamp'],
            total_input=convert_value(currency, row['total_input'], rates),
            total_output=convert_value(currency, row['total_output'], rates))


def io_from_rows(currency, values, rates):
    return [TxValue(address=i.address,
                    value=convert_value(currency, i.value, rates))
            for i in values if i.address is not None]


async def get_tx(currency, tx_hash):
    db = get_connection()
    result = await db.get_tx(currency, tx_hash)
    # TODO result is a generator, never None!
    if result is None:
        raise RuntimeError('Transaction {} in keyspace {} not found'
                           .format(tx_hash, currency))

    rates = get_rates(currency, result['block_id'])['rates']
    result = from_row(currency, result, rates)
    return result


def get_tx_io(currency, tx_hash, io):
    result = get_tx(currency, tx_hash)
    if currency == 'eth':
        raise RuntimeError('get_tx_io not implemented for ETH')
    return getattr(result, io)


async def list_txs(currency, page=None):
    db = get_connection()
    results, paging_state = db.list_txs(currency, page)

    def acc(row):
        return row['block_id'] if currency == 'eth' else row['block_id']

    heights = [acc(row) for row in results]
    rates = list_rates(currency, heights)
    tx_list = [from_row(currency, row, rates[acc(row)])
               for row in results]

    return Txs(next_page=paging_state, txs=tx_list)


def list_matching_txs(currency, expression):
    db = get_connection()
    results = db.list_matching_txs(currency, expression)

    leading_zeros = 0
    pos = 0
    # leading zeros will be lost when casting to int
    while expression[pos] == "0":
        pos += 1
        leading_zeros += 1

    txs = ["0" * leading_zeros + str(hex(int.from_bytes(row['tx_hash'],
                                                        byteorder="big")))[2:]
           for row in results]
    return [tx for tx in txs if tx.startswith(expression)]
