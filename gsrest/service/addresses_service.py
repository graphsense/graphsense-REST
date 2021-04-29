from gsrest.db import get_connection
from openapi_server.models.address_tx import AddressTx
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.link import Link
from openapi_server.models.txs_eth import TxsEth
from openapi_server.models.tx_eth import TxEth
from gsrest.service.entities_service import get_entity_with_tags
from gsrest.service.rates_service import list_rates
import gsrest.service.common_service as common
from gsrest.util.values import convert_value
from flask import Response, stream_with_context
from gsrest.util.csvify import create_download_header, to_csv


def get_address_with_tags(currency, address):
    return common.get_address_with_tags(currency, address)


def list_address_tags(currency, address):
    return common.list_address_tags(currency, address)


def list_address_tags_csv(currency, address):
    def query_function(_):
        tags = common.list_address_tags(currency, address)
        return (None, tags)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                        'tags of address {} ({}).csv'
                        .format(address,
                                currency.upper())))


def list_address_txs(currency, address, page=None, pagesize=None):
    db = get_connection()
    results, paging_state = \
        db.list_address_txs(currency, address, page, pagesize)
    address_txs = []
    if results:
        heights = [row.height for row in results]
        rates = list_rates(currency, heights)
        address_txs = [AddressTx(
                        address=address,
                        height=row.height,
                        timestamp=row.timestamp,
                        tx_hash=row.tx_hash.hex(),
                        value=convert_value(row.value, rates[row.height])
                        )
                       for row in results]
    return AddressTxs(next_page=paging_state, address_txs=address_txs)


def list_address_txs_csv(currency, address):
    def query_function(page_state):
        result = list_address_txs(currency, address, page_state)
        return (result.next_page, result.address_txs)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                            'transactions of address {} ({}).csv'
                            .format(address, currency.upper())))


def list_address_neighbors(currency, address, direction, page=None,
                           pagesize=None):
    return common.list_neighbors(currency, address, direction, 'address',
                                 page=page, pagesize=pagesize)


def list_address_neighbors_csv(currency, address, direction):
    def query_function(page_state):
        result = list_address_neighbors(currency, address, direction,
                                        page_state)
        return (result.next_page, result.neighbors)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                            '{} neighbors of address {} ({}).csv'
                            .format(direction, address, currency.upper())))


def list_address_links(currency, address, neighbor):
    db = get_connection()
    links = db.list_address_links(currency, address, neighbor)

    heights = [row['height'] for row in links]
    rates = list_rates(currency, heights)

    return [Link(tx_hash=e['tx_hash'],
                 height=e['height'],
                 timestamp=e['timestamp'],
                 input_value=convert_value(
                     e['input_value'], rates[e['height']]),
                 output_value=convert_value(
                     e['output_value'], rates[e['height']]),
                 ) for e in links]


def list_address_links_csv(currency, address, neighbor):
    def query_function(_):
        result = list_address_links(currency, address, neighbor)
        return (None, result)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                            'transactions between {} and {} ({}).csv'
                            .format(address, neighbor, currency.upper())))


def get_address_entity(currency, address):
    # from address to complete entity stats
    e = RuntimeError('Entity for address {} not found'.format(address))
    db = get_connection()

    entity_id = db.get_address_entity_id(currency, address)
    if entity_id is None:
        raise e

    result = get_entity_with_tags(currency, entity_id)
    if result is None:
        raise e

    return result


def list_matching_addresses(currency, expression):
    db = get_connection()
    return db.list_matching_addresses(currency, expression)


def list_address_txs_eth(address, page=None, pagesize=None):
    db = get_connection()
    results, paging_state = \
        db.list_address_txs_eth(address, page, pagesize)
    txs = []
    if results:
        heights = [row.block_number for row in results]
        rates = list_rates('eth', heights)
        txs = [TxEth(
         tx_hash=tx.hash.hex(),
         timestamp=tx.block_timestamp,
         height=tx.block_number,
         values=convert_value(tx.value, rates[tx.block_number]))
                       for tx in results]
    return TxsEth(next_page=paging_state, txs=txs)


def list_address_txs_csv_eth(address):
    currency = 'eth'

    def query_function(page_state):
        result = list_address_txs_eth(address, page_state)
        return (result.next_page, result.txs)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                            'transactions of address {} ({}).csv'
                            .format(address, currency.upper())))
