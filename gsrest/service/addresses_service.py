from openapi_server.models.address_txs import AddressTxs
from gsrest.service.entities_service import get_entity, from_row
from gsrest.service.rates_service import get_rates
import gsrest.service.common_service as common
from gsrest.service.common_service import cannonicalize_address
from gsrest.errors import *
from gsrest.util.address import address_to_user_format
from openapi_server.models.neighbor_addresses import NeighborAddresses
from openapi_server.models.neighbor_address import NeighborAddress
import asyncio
from gsrest.db.node_type import NodeType


async def get_address(request, currency, address):
    return await common.get_address(request, currency, address)


async def list_tags_by_address(request,
                               currency,
                               address,
                               page=None,
                               pagesize=None):
    address = address_to_user_format(currency, address)
    return await common.list_tags_by_address(request,
                                             currency,
                                             address,
                                             page=page,
                                             pagesize=pagesize)


async def list_address_txs(request,
                           currency,
                           address,
                           min_height=None,
                           max_height=None,
                           direction=None,
                           token_currency=None,
                           page=None,
                           pagesize=None):
    address = cannonicalize_address(currency, address)
    db = request.app['db']
    results, paging_state = \
        await db.list_address_txs(currency, address, direction, min_height,
                                  max_height, token_currency, page, pagesize)

    address_txs = await common.txs_from_rows(
        request, currency, results, db.get_token_configuration(currency))
    return AddressTxs(next_page=paging_state, address_txs=address_txs)


async def list_address_neighbors(request,
                                 currency,
                                 address,
                                 direction,
                                 only_ids=None,
                                 include_labels=False,
                                 page=None,
                                 pagesize=None):
    address = cannonicalize_address(currency, address)
    db = request.app['db']
    if isinstance(only_ids, list):
        aws = [
            db.get_address_id(currency, cannonicalize_address(currency, id))
            for id in only_ids
        ]
        only_ids = await asyncio.gather(*aws)
        only_ids = [id for id in only_ids if id is not None]

    results, paging_state = \
        await common.list_neighbors(request, currency, address, direction,
                                    NodeType.ADDRESS, ids=only_ids,
                                    include_labels=include_labels,
                                    page=page, pagesize=pagesize)
    is_outgoing = "out" in direction
    dst = 'dst' if is_outgoing else 'src'
    relations = []
    if results is None:
        return NeighborAddresses()
    aws = [
        get_address(request, currency,
                    address_to_user_format(currency, row[dst + '_address']))
        for row in results
    ]

    nodes = await asyncio.gather(*aws)

    for row, node in zip(results, nodes):
        nb = NeighborAddress(labels=row['labels'],
                             value=row['value'],
                             no_txs=row['no_transactions'],
                             token_values=row.get("token_values", None),
                             address=node)
        relations.append(nb)

    return NeighborAddresses(next_page=paging_state, neighbors=relations)


async def list_address_links(request,
                             currency,
                             address,
                             neighbor,
                             page=None,
                             pagesize=None):
    address = cannonicalize_address(currency, address)
    neighbor = cannonicalize_address(currency, neighbor)
    db = request.app['db']
    result = await db.list_address_links(currency,
                                         address,
                                         neighbor,
                                         page=page,
                                         pagesize=pagesize)

    return await common.links_response(request, currency, result)


async def get_address_entity(request, currency, address):
    address_canonical = cannonicalize_address(currency, address)
    db = request.app['db']

    try:
        entity_id = await db.get_address_entity_id(currency, address_canonical)
    except AddressNotFoundException:
        aws = [get_rates(request, currency), db.new_entity(
            currency, address_canonical)]
        [rates, entity] = await asyncio.gather(*aws)
        return from_row(currency, entity, rates['rates'],
                        db.get_token_configuration(currency))

    try:
        return await get_entity(request,
                                currency,
                                entity_id,
                                include_actors=True)
    except ClusterNotFoundException:
        raise DBInconsistencyException(
            f'entity referenced by {address} in {currency} not found')
