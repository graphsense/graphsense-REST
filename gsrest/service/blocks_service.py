from cassandra.query import SimpleStatement

from gsrest.db.cassandra import get_session
from gsrest.model.blocks import Block, BlockTxs

# TODO: handle failing queries

BLOCKS_PAGE_SIZE = 100


def get_block(currency, height):
    session = get_session(currency, 'raw')

    query = "SELECT * FROM block WHERE height = %s"
    result = session.execute(query, [height])

    return Block.from_row(result[0]).to_dict() if result else None


def list_blocks(currency, paging_state=None):
    session = get_session(currency, 'raw')

    query = "SELECT * FROM block"
    statement = SimpleStatement(query, fetch_size=BLOCKS_PAGE_SIZE)
    results = session.execute(statement, paging_state=paging_state)

    paging_state = results.paging_state
    block_list = [Block.from_row(row).to_dict()
                  for row in results.current_rows]

    return paging_state, block_list


def list_block_txs(currency, height):
    session = get_session(currency, 'raw')

    query = "SELECT * FROM block_txs WHERE height = %s"
    results = session.execute(query, [height])

    block_txs = None
    if results:
        block_txs = BlockTxs.from_row(
            results[0]).to_dict()

    return block_txs
