from cassandra.query import SimpleStatement

from gsrest.db.cassandra import get_session
from gsrest.model.txs import Tx

# TODO: handle failing queries

TXS_PAGE_SIZE = 100


def get_tx(currency, txHash):
    session = get_session(currency, 'raw')

    query = "SELECT * FROM transaction WHERE tx_prefix = %s AND tx_hash = %s"
    result = session.execute(query, [txHash[:5], bytearray.fromhex(txHash)])

    return Tx.from_row(result[0]).to_dict() if result else None


def list_txs(currency, paging_state=None):
    session = get_session(currency, 'raw')

    query = "SELECT * FROM transaction"
    statement = SimpleStatement(query, fetch_size=TXS_PAGE_SIZE)
    results = session.execute(statement, paging_state=paging_state)

    paging_state = results.paging_state
    tx_list = [Tx.from_row(row).to_dict()
               for row in results.current_rows]

    return paging_state, tx_list
