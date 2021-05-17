from gsrest.db import get_connection
from openapi_server.models.block import Block
from openapi_server.models.block_eth import BlockEth
from openapi_server.models.blocks import Blocks
from openapi_server.models.blocks_eth import BlocksEth
from openapi_server.models.txs import Txs
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


def get_block_eth(height) -> BlockEth:
    db = get_connection()
    row = db.get_block_eth(height)
    if not row:
        raise RuntimeError("Ethereum Block {} not found".format(height))
    return BlockEth(
            height=row.number,
            block_hash=row.hash.hex(),
            no_txs=row.transaction_count,
            timestamp=row.timestamp)


def list_blocks_eth(page=None):
    db = get_connection()
    results, paging_state = db.list_blocks_eth(page)
    block_list = [BlockEth(
                    height=row.number,
                    block_hash=row.hash.hex(),
                    no_txs=row.transaction_count,
                    timestamp=row.timestamp)
                  for row in results.current_rows]

    return BlocksEth(paging_state, block_list)


def list_block_txs_eth(height):
    db = get_connection()
    result = db.list_block_txs_eth(height)

    if result is None:
        raise RuntimeError("Block {} not found".format(height))

    rates = get_rates('eth', height)
    txs = \
        [TxAccount(
         tx_hash=tx.hash.hex(),
         timestamp=tx.block_timestamp,
         height=tx.block_number,
         values=convert_value(tx.value, rates['rates']))
         for tx in result]

    return Txs(next_page=None, txs=txs)


def list_block_txs_csv_eth(height):
    def query_function(_):
        result = list_block_txs_eth(height)
        txs = [tx.to_dict() for tx in result.txs]
        return None, txs
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                        'transactions of block {} ({}).csv'
                        .format(height, 'ETH')))
