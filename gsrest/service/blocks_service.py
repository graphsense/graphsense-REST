from cassandra.query import SimpleStatement

from gsrest.db.cassandra import get_session
from openapi_server.models.block import Block
from openapi_server.models.blocks import Blocks
from openapi_server.models.block_txs import BlockTxs
from openapi_server.models.block_tx_summary import BlockTxSummary
from gsrest.model.common import convert_value
from gsrest.service.rates_service import get_rates
from flask import Response, stream_with_context
from gsrest.util.csvify import create_download_header, to_csv
from gsrest.service.problems import notfound, badrequest

BLOCKS_PAGE_SIZE = 100


def get_block(currency, height) -> Block:
    session = get_session(currency, 'raw')

    query = "SELECT * FROM block WHERE height = %s"
    row = session.execute(query, [height]).one()
    if not row:
        return notfound("Block {} not found".format(height))
    return Block(
            height=row.height,
            block_hash=row.block_hash.hex(),
            no_txs=row.no_transactions,
            timestamp=row.timestamp)


def list_blocks(currency, page=None):
    session = get_session(currency, 'raw')
    try:
        paging_state = bytes.fromhex(page) if page else None
    except ValueError as e:
        return badrequest(str(e))

    query = "SELECT * FROM block"
    statement = SimpleStatement(query, fetch_size=BLOCKS_PAGE_SIZE)
    results = session.execute(statement, paging_state=paging_state)

    paging_state = results.paging_state.hex() if results.paging_state else None
    block_list = [Block(
                    height=row.height,
                    block_hash=row.block_hash.hex(),
                    no_txs=row.no_transactions,
                    timestamp=row.timestamp)
                  for row in results.current_rows]

    return Blocks(paging_state, block_list)


def list_block_txs(currency, height):
    session = get_session(currency, 'raw')

    query = "SELECT * FROM block_transactions WHERE height = %s"
    results = session.execute(query, [height])
    if results is None:
        return notfound("Block {} not found".format(height))
    rates = get_rates(currency, height)

    tx_summaries = \
        [BlockTxSummary(
         no_inputs=tx.no_inputs,
         no_outputs=tx.no_outputs,
         total_input=convert_value(tx.total_input, rates['rates']),
         total_output=convert_value(tx.total_output, rates['rates']),
         tx_hash=tx.tx_hash.hex()
         )
         for tx in results[0].txs]

    return BlockTxs(height, tx_summaries)


def list_block_txs_csv(currency, height):
    def query_function(_):
        result = list_block_txs(currency, height)
        txs = [tx.to_dict() for tx in result.txs]
        for tx in txs:
            tx['block_height'] = result.height
        return None, txs
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                        'transactions of block {} ({}).csv'
                        .format(height, currency.upper())))
