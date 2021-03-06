from gsrest.db import get_connection
from openapi_server.models.address_tx import AddressTx
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.link import Link
from gsrest.service.entities_service import get_entity_with_tags
from gsrest.service.rates_service import get_rates, list_rates
import gsrest.service.common_service as commonDAO
from gsrest.util.values import convert_value, compute_balance, make_values
from flask import Response, stream_with_context
from gsrest.util.csvify import create_download_header, to_csv


def get_address_with_tags(currency, address):
    return commonDAO.get_address_with_tags(currency, address)


def list_address_tags(currency, address):
    return commonDAO.list_address_tags(currency, address)


def list_address_tags_csv(currency, address):
    def query_function(_):
        tags = commonDAO.list_address_tags(currency, address)
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
    is_outgoing = "out" in direction
    db = get_connection()
    results, paging_state = db.list_address_relations(
                                    currency,
                                    address,
                                    is_outgoing,
                                    page,
                                    pagesize)
    dst = 'dst' if is_outgoing else 'src'
    rates = get_rates(currency)['rates']
    relations = []
    if results is None:
        return Neighbors()
    for row in results:
        balance = compute_balance(row[dst+'_properties'].total_received.value,
                                  row[dst+'_properties'].total_spent.value)
        relations.append(Neighbor(
            id=row['id'],
            node_type='address',
            labels=row[dst+'_labels']
            if row[dst+'_labels'] is not None else [],
            received=make_values(
                value=row[dst+'_properties'].total_received.value,
                eur=row[dst+'_properties'].total_received.eur,
                usd=row[dst+'_properties'].total_received.usd),
            estimated_value=make_values(
                value=row['estimated_value'].value,
                eur=row['estimated_value'].eur,
                usd=row['estimated_value'].usd),
            balance=convert_value(balance, rates),
            no_txs=row['no_transactions']))
    return Neighbors(next_page=paging_state,
                     neighbors=relations)


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
