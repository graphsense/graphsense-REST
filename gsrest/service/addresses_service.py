from openapi_server.models.address_txs import AddressTxs
from gsrest.service.entities_service import get_entity, from_row
from gsrest.service.rates_service import get_rates
import gsrest.service.common_service as common
from gsrest.service.common_service import cannonicalize_address
from gsrest.errors import (AddressNotFoundException, ClusterNotFoundException,
                           DBInconsistencyException)
from gsrest.util.address import address_to_user_format
from openapi_server.models.neighbor_addresses import NeighborAddresses
from openapi_server.models.neighbor_address import NeighborAddress
import asyncio
from gsrest.db.node_type import NodeType
from gsrest.db.util import tagstores
from gsrest.service.tags_service import address_tag_from_row
from functools import partial
from gsrest.util.tag_summary import get_tag_summary


async def get_best_cluster_tag(request, currency, address):
    address_canonical = cannonicalize_address(currency, address)
    db = request.app['db']

    entity_id = await db.get_address_entity_id(currency, address_canonical)

    tags = await tagstores(request.app['tagstores'], address_tag_from_row,
                           'get_best_entity_tag', currency, entity_id,
                           request.app['request_config']['show_private_tags'])

    if len(tags) > 0:
        return tags[0]
    else:
        return None


async def get_tag_summary_by_address(request,
                                     currency,
                                     address,
                                     include_best_cluster_tag=False):
    address_canonical = cannonicalize_address(currency, address)

    next_page_fn = partial(list_tags_by_address,
                           request,
                           currency,
                           address_canonical,
                           include_best_cluster_tag=include_best_cluster_tag)
    return await get_tag_summary(next_page_fn)


async def get_address(request, currency, address, include_actors=True):
    return await common.get_address(request,
                                    currency,
                                    address,
                                    include_actors=include_actors)


async def list_tags_by_address(request,
                               currency,
                               address,
                               page=None,
                               pagesize=None,
                               include_best_cluster_tag=False):
    address = address_to_user_format(currency, address)

    tagdata = await common.list_tags_by_address(request,
                                                currency,
                                                address,
                                                page=page,
                                                pagesize=pagesize)

    best_cluster_tag = []
    if (include_best_cluster_tag):
        best_cluster_tag = await get_best_cluster_tag(request, currency,
                                                      address)
        if best_cluster_tag is not None:
            best_cluster_tag.inherited_from = "cluster"
            tagdata.address_tags.append(best_cluster_tag)

    return tagdata


async def list_address_txs(request,
                           currency,
                           address,
                           min_height=None,
                           max_height=None,
                           direction=None,
                           order='desc',
                           token_currency=None,
                           page=None,
                           pagesize=None):
    address = cannonicalize_address(currency, address)
    db = request.app['db']
    results, paging_state = \
        await db.list_address_txs(currency=currency,
                                  address=address,
                                  direction=direction,
                                  min_height=min_height,
                                  max_height=max_height,
                                  order=order,
                                  token_currency=token_currency,
                                  page=page,
                                  pagesize=pagesize)

    address_txs = await common.txs_from_rows(
        request, currency, results, db.get_token_configuration(currency))
    return AddressTxs(next_page=paging_state, address_txs=address_txs)


async def list_address_neighbors(request,
                                 currency,
                                 address,
                                 direction,
                                 only_ids=None,
                                 include_labels=False,
                                 include_actors=True,
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
        get_address(request,
                    currency,
                    address_to_user_format(currency, row[dst + '_address']),
                    include_actors=include_actors) for row in results
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
                             min_height=None,
                             max_height=None,
                             order='desc',
                             page=None,
                             pagesize=None):
    address = cannonicalize_address(currency, address)
    neighbor = cannonicalize_address(currency, neighbor)
    db = request.app['db']
    result = await db.list_address_links(currency,
                                         address,
                                         neighbor,
                                         min_height=min_height,
                                         max_height=max_height,
                                         order=order,
                                         page=page,
                                         pagesize=pagesize)

    return await common.links_response(request, currency, result)


async def get_address_entity(request, currency, address):
    address_canonical = cannonicalize_address(currency, address)
    db = request.app['db']
    try:
        entity_id = await db.get_address_entity_id(currency, address_canonical)
    except AddressNotFoundException:
        aws = [
            get_rates(request, currency),
            db.new_entity(currency, address_canonical)
        ]
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
