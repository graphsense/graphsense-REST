from cassandra.query import SimpleStatement

from gsrest.db.cassandra import get_session
from openapi_server.models.tx import Tx
from openapi_server.models.txs import Txs
from openapi_server.models.tx_value import TxValue
from gsrest.service.rates_service import get_rates, list_rates
from gsrest.model.common import convert_value

TXS_PAGE_SIZE = 100
TX_PREFIX_LENGTH = 5


def from_row(row, rates):
    return Tx(
            tx_hash=row.tx_hash,
            coinbase=row.coinbase,
            height=row.height,
            inputs=[TxValue(address=i.address,
                            value=convert_value(i.value, rates))
                    for i in row.inputs],
            outputs=[TxValue(address=i.address,
                             value=convert_value(i.value, rates))
                     for i in row.outputs],
            timestamp=row.timestamp,
            total_input=convert_value(row.total_input, rates),
            total_output=convert_value(row.total_output, rates))


def get_tx(currency, tx_hash):
    session = get_session(currency, 'raw')

    query = "SELECT * FROM transaction WHERE tx_prefix = %s AND tx_hash = %s"
    result = session.execute(query, [tx_hash[:TX_PREFIX_LENGTH],
                                     bytearray.fromhex(tx_hash)])
    if result is None:
        raise RuntimeError('Transaction {} in keyspace {} not found'
                           .format(tx_hash, currency))

    result = result.one()

    rates = get_rates(currency, result.height)['rates']
    return from_row(result, {result.height: rates})


def list_txs(currency, page=None):
    session = get_session(currency, 'raw')

    paging_state = bytes.fromhex(page) if page else None
    query = "SELECT * FROM transaction"
    statement = SimpleStatement(query, fetch_size=TXS_PAGE_SIZE)
    results = session.execute(statement, paging_state=paging_state)

    paging_state = results.paging_state
    heights = [row.height for row in results.current_rows]
    rates = list_rates(currency, heights)
    tx_list = [from_row(row, rates[row.height])
               for row in results.current_rows]

    return Txs(next_page=paging_state, txs=tx_list)


def list_matching_txs(currency, expression, leading_zeros):
    session = get_session(currency, 'raw')
    query = 'SELECT tx_hash from transaction where tx_prefix = %s'
    results = session.execute(query, [expression[:TX_PREFIX_LENGTH]])
    txs = ["0" * leading_zeros + str(hex(int.from_bytes(row.tx_hash,
                                                        byteorder="big")))[2:]
           for row in results]
    return [tx for tx in txs if tx.startswith(expression)]
