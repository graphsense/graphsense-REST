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
            tx_hash=row.hash.hex(),
            timestamp=row.block_timestamp,
            height=row.block_number,
            values=convert_value(row.value, rates))
    return TxUtxo(
            tx_hash=row.tx_hash.hex(),
            coinbase=row.coinbase,
            height=row.height,
            inputs=[TxValue(address=i.address,
                            value=convert_value(i.value, rates))
                    for i in row.inputs if i.address is not None]
            if row.inputs else [],
            outputs=[TxValue(address=i.address,
                             value=convert_value(i.value, rates))
                     for i in row.outputs if i.address is not None]
            if row.outputs else [],
            timestamp=row.timestamp,
            total_input=convert_value(row.total_input, rates),
            total_output=convert_value(row.total_output, rates))


def get_tx(currency, tx_hash):
    db = get_connection()
    result = db.get_tx(currency, tx_hash)

    if result is None:
        raise RuntimeError('Transaction {} in keyspace {} not found'
                           .format(tx_hash, currency))

    height = result.block_number if currency == 'eth' else result.height
    rates = get_rates(currency, height)['rates']
    return from_row(currency, result, rates)


def list_txs(currency, page=None):
    db = get_connection()
    results, paging_state = db.list_txs(currency, page)

    def acc(row):
        return row.block_number if currency == 'eth' else row.height

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

    txs = ["0" * leading_zeros + str(hex(int.from_bytes(row.tx_hash,
                                                        byteorder="big")))[2:]
           for row in results]
    return [tx for tx in txs if tx.startswith(expression)]
