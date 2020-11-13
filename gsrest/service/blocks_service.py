from gsrest.db import get_connection
from openapi_server.models.block import Block
from openapi_server.models.blocks import Blocks
from openapi_server.models.block_txs import BlockTxs
from openapi_server.models.block_tx_summary import BlockTxSummary
from gsrest.util.values import convert_value
from gsrest.service.rates_service import get_rates
from flask import Response, stream_with_context
from gsrest.util.csvify import create_download_header, to_csv


def get_block(currency, height) -> Block:
    db = get_connection()
    row = db.get_block(currency, height)
    if not row:
        raise RuntimeError("Block {} not found".format(height))
    return Block(
            height=row.height,
            block_hash=row.block_hash.hex(),
            no_txs=row.no_transactions,
            timestamp=row.timestamp)


def list_blocks(currency, page=None):
    db = get_connection()
    results, paging_state = db.list_blocks(currency, page)
    block_list = [Block(
                    height=row.height,
                    block_hash=row.block_hash.hex(),
                    no_txs=row.no_transactions,
                    timestamp=row.timestamp)
                  for row in results.current_rows]

    return Blocks(paging_state, block_list)


def list_block_txs(currency, height):
    db = get_connection()
    result = db.list_block_txs(currency, height)

    if result is None:
        raise RuntimeError("Block {} not found".format(height))
    rates = get_rates(currency, height)

    tx_summaries = \
        [BlockTxSummary(
         no_inputs=tx.no_inputs,
         no_outputs=tx.no_outputs,
         total_input=convert_value(tx.total_input, rates['rates']),
         total_output=convert_value(tx.total_output, rates['rates']),
         tx_hash=tx.tx_hash.hex()
         )
         for tx in result.txs]

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
