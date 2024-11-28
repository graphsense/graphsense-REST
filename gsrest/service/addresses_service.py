from typing import List
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
from gsrest.service.tags_service import (get_tagstore_access_groups,
                                         address_tag_from_PublicTag,
                                         get_address_tag_result)
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.address_tags import AddressTags
from gsrest.util import is_eth_like
from tagstore.db import TagstoreDbAsync, TagPublic
from tagstore.algorithms.tag_digest import TagDigest, compute_tag_digest
from openapi_server.models.tag_summary import TagSummary
from openapi_server.models.tag_cloud_entry import TagCloudEntry
from openapi_server.models.label_summary import LabelSummary


def tagSummary_from_tagDigest(td: TagDigest):
    return TagSummary(broad_category=td.broad_concept,
                      tag_count=td.nr_tags,
                      best_actor=td.best_actor,
                      best_label=td.best_label,
                      concept_tag_cloud={
                          k: TagCloudEntry(cnt=v.count, weighted=v.weighted)
                          for k, v in td.concept_tag_cloud.items()
                      },
                      label_summary={
                          key:
                          LabelSummary(label=v.label,
                                       count=v.count,
                                       confidence=v.confidence,
                                       relevance=v.relevance,
                                       creators=v.creators,
                                       sources=v.sources,
                                       concepts=v.concepts,
                                       lastmod=v.lastmod,
                                       inherited_from=v.inherited_from)
                          for (key, v) in td.label_digest.items()
                      })


async def get_best_cluster_tag_raw(request, currency,
                                   address) -> TagPublic | None:
    address_canonical = cannonicalize_address(currency, address)
    db = request.app['db']
    tagstore_db = TagstoreDbAsync(request.app["gs-tagstore"])

    clstr_id = await db.get_address_entity_id(currency, address_canonical)

    return await tagstore_db.get_best_cluster_tag(
        clstr_id, currency.upper(), get_tagstore_access_groups(request))


async def get_best_cluster_tag(request, currency,
                               address) -> AddressTag | None:
    tag = await get_best_cluster_tag_raw(request, currency, address)

    if tag is not None:
        return address_tag_from_PublicTag(tag)

    return None


async def list_tags_by_address_raw(
        request,
        currency,
        address,
        page=None,
        pagesize=None,
        include_best_cluster_tag=False) -> List[TagPublic]:

    address = address_to_user_format(currency, address)

    tsdb = TagstoreDbAsync(request.app["gs-tagstore"])

    if page is None:
        page = 0
    page = int(page)

    tags = list(await
                tsdb.get_tags_by_subjectid(address,
                                           page * (pagesize or 0),
                                           pagesize,
                                           get_tagstore_access_groups(request),
                                           network=currency.upper()))

    if (include_best_cluster_tag and not is_eth_like(currency)):
        best_cluster_tag = await get_best_cluster_tag_raw(
            request, currency, address)
        if best_cluster_tag is not None:
            tags.append(best_cluster_tag)

    return tags


async def get_tag_summary_by_address(request,
                                     currency,
                                     address,
                                     include_best_cluster_tag=False):
    address_canonical = cannonicalize_address(currency, address)

    tags = await list_tags_by_address_raw(
        request,
        currency,
        address_canonical,
        page=None,
        pagesize=None,
        include_best_cluster_tag=include_best_cluster_tag)

    digest = compute_tag_digest(tags)

    return tagSummary_from_tagDigest(digest)


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
                               include_best_cluster_tag=False) -> AddressTags:
    tags = [
        address_tag_from_PublicTag(pt)
        for pt in (await list_tags_by_address_raw(
            request,
            currency,
            address,
            page=page,
            pagesize=pagesize,
            include_best_cluster_tag=include_best_cluster_tag))
    ]

    return get_address_tag_result(page, pagesize, tags)


# async def list_tags_by_address_raw(request,
#                                currency,
#                                address,
#                                page=None,
#                                pagesize=None,
#                                include_best_cluster_tag=False):

#     taglist = await list_tags_by_address_raw_basic(request,
#                                                 currency,
#                                                 address,
#                                                 page=page,
#                                                 pagesize=pagesize)

#     if (include_best_cluster_tag and not is_eth_like(currency)):
#         best_cluster_tag = await get_best_cluster_tag_raw(request, currency,
#                                                       address)
#         if best_cluster_tag is not None:
#             best_cluster_tag.inherited_from = "cluster"
#             taglist.append(best_cluster_tag)

#     return tagdata


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
        return NeighborAddresses(neighbors=[])
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


async def get_address_entity(request, currency, address, include_actors=True):
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
                                include_actors=include_actors)
    except ClusterNotFoundException:
        raise DBInconsistencyException(
            f'entity referenced by {address} in {currency} not found')
