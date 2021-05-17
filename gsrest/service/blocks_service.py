from gsrest.db import get_connection
from openapi_server.models.block import Block
from openapi_server.models.blocks import Blocks
from openapi_server.models.tx import TxAccount
from openapi_server.models.block_tx_utxo import BlockTxUtxo
from gsrest.util.values import convert_value
from gsrest.service.rates_service import get_rates
from flask import Response, stream_with_context
from gsrest.util.csvify import create_download_header, to_csv


def from_row(currency, row, rates):
    if currency == 'eth':
        return TxAccount(
            tx_hash=row.hash.hex(),
            timestamp=row.block_timestamp,
            height=row.block_number,
            values=convert_value(row.value, rates))
    return BlockTxUtxo(
         no_inputs=row.no_inputs,
         no_outputs=row.no_outputs,
         total_input=convert_value(row.total_input, rates),
         total_output=convert_value(row.total_output, rates),
         tx_hash=row.tx_hash.hex())


def block_from_row(currency, row):
    if currency == 'eth':
        return Block(
                height=row.number,
                block_hash=row.hash.hex(),
                no_txs=row.transaction_count,
                timestamp=row.timestamp)
    return Block(
            height=row.height,
            block_hash=row.block_hash.hex(),
            no_txs=row.no_transactions,
            timestamp=row.timestamp)


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

    return Blocks(paging_state, block_list)


def list_block_txs(currency, height):
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
