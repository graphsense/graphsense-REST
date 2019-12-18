from cassandra.query import SimpleStatement
from flask import abort

from gsrest.db.cassandra import get_session
from gsrest.service.rates_service import get_rates
from gsrest.model.blocks import Block, BlockTxs

BLOCKS_PAGE_SIZE = 100


def get_block(currency, height):
    session = get_session(currency, 'raw')

    query = "SELECT * FROM block WHERE height = %s"
    result = session.execute(query, [height])
    if result:
        return Block.from_row(result[0]).to_dict()
    abort(404, "Block {} not found in currency {}".format(height, currency))


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

    query = "SELECT * FROM block_transactions WHERE height = %s"
    results = session.execute(query, [height])

    if results:
        rates = get_rates(currency, height)

        block_txs = BlockTxs.from_row(results[0],
                                      rates['rates']).to_dict()

        return block_txs
    abort(404, "Block {} not found in currency {}".format(height, currency))
