from gsrest.db import get_connection
from openapi_server.models.block import Block
from openapi_server.models.blocks import Blocks
from gsrest.service.rates_service import get_rates
from flask import Response, stream_with_context
from gsrest.util.csvify import create_download_header, to_csv
from gsrest.service.txs_service import from_row


def block_from_row(currency, row):
    if currency == 'eth':
        return Block(
                height=row['block_id'],
                block_hash=row['block_hash'].hex(),
                no_txs=row['transaction_count'],
                timestamp=row['timestamp'])
    return Block(
            height=row['block_id'],
            block_hash=row['block_hash'].hex(),
            no_txs=row['no_transactions'],
            timestamp=row['timestamp'])


def get_block(currency, height):
    db = get_connection()
    row = db.get_block(currency, height)
    if not row:
        raise RuntimeError("Block {} not found".format(height))
    return block_from_row(currency, row)


def list_blocks(currency, page=None):
    db = get_connection()
    results, paging_state = db.list_blocks(currency, page)
    block_list = [block_from_row(currency, row)
                  for row in results.current_rows]

    return Blocks(blocks=block_list, next_page=paging_state)


async def list_block_txs(currency, height):
    db = get_connection()
    txs = db.list_block_txs(currency, height)

    if txs is None:
        raise RuntimeError("Block {} not found".format(height))
    rates = get_rates(currency, height)

    return [from_row(currency, tx, rates['rates'])
            for tx in txs]


def list_block_txs_csv(currency, height):
    def query_function(_):
        result = list_block_txs(currency, height)
        txs = [tx.to_dict() for tx in result]
        return None, txs
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                        'transactions of block {} ({}).csv'
                        .format(height, currency.upper())))
