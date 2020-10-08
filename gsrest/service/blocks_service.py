from cassandra.query import SimpleStatement

from gsrest.db.cassandra import get_session
from openapi_server.models.block import Block
from openapi_server.models.blocks import Blocks
from openapi_server.models.block_txs import BlockTxs
from openapi_server.models.block_tx_summary import BlockTxSummary
from openapi_server.models.converted_values import ConvertedValues
import gsrest.model.common
from gsrest.service.rates_service import get_rates
from flask import Response, abort, stream_with_context
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

    if results:
        rates = get_rates(currency, height)

        tx_summaries = \
            [BlockTxSummary(
             no_inputs=tx.no_inputs,
             no_outputs=tx.no_outputs,
             total_input=ConvertedValues.from_dict(
                 gsrest.model.common.ConvertedValues(
                     tx.total_input, rates['rates'])
                 .to_dict()),
             total_output=ConvertedValues.from_dict(
                 gsrest.model.common.ConvertedValues(
                     tx.total_output, rates['rates'])
                 .to_dict()),
             tx_hash=tx.tx_hash.hex()
             )
             for tx in results[0].txs]

        return BlockTxs(height, tx_summaries)

    return None


def list_block_txs_csv(currency, height):
    def query_function(_):
        result = list_block_txs(currency, height)
        if result:
            return None, \
              [{'block_height': result.height,
                'tx_hash': tx.tx_hash,
                'no_inputs': tx.no_inputs,
                'no_outputs': tx.no_outputs,
                'total_input_eur': tx.total_input.eur,
                'total_input_usd': tx.total_input.usd,
                'total_input_value': tx.total_input.value,
                'total_output_eur': tx.total_output.eur,
                'total_output_usd': tx.total_output.usd,
                'total_output_value': tx.total_output.value}
               for tx in result.txs]
        abort(404,
              "Block {} not found in currency {}".format(height, currency))

    try:
        return Response(stream_with_context(to_csv(query_function)),
                        mimetype="text/csv",
                        headers=create_download_header(
                            'transactions of block {} ({}).csv'
                            .format(height, currency.upper())))

    except ValueError:
        abort(404,
              "Block {} not found in currency {}".format(height, currency))
