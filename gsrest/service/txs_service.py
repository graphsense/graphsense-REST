from gsrest.db import get_connection
from openapi_server.models.tx import Tx
from openapi_server.models.txs import Txs
from openapi_server.models.tx_eth import TxEth
from openapi_server.models.tx_value import TxValue
from gsrest.service.rates_service import get_rates, list_rates
from gsrest.util.values import convert_value


def from_row(row, rates):
    return Tx(
            tx_hash=row.tx_hash.hex(),
            coinbase=row.coinbase,
            height=row.height,
            inputs=[TxValue(address=i.address,
                            value=convert_value(i.value, rates))
                    for i in row.inputs]
            if row.inputs else [],
            outputs=[TxValue(address=i.address,
                             value=convert_value(i.value, rates))
                     for i in row.outputs]
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

    rates = get_rates(currency, result.height)['rates']
    return from_row(result, rates)


def get_tx_eth(tx_hash):
    db = get_connection()
    result = db.get_tx_eth(tx_hash)

    if result is None:
        raise RuntimeError('Transaction {} in keyspace {} not found'
                           .format(tx_hash, 'ETH'))

    rates = get_rates('eth', result.block_number)['rates']
    return TxEth(
         tx_hash=result.hash.hex(),
         timestamp=result.block_timestamp,
         height=result.block_number,
         values=convert_value(result.value, rates))


def list_txs(currency, page=None):
    db = get_connection()
    results, paging_state = db.list_txs(currency, page)

    heights = [row.height for row in results]
    rates = list_rates(currency, heights)
    tx_list = [from_row(row, rates[row.height])
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
