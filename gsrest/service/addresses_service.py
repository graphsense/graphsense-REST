import asyncio
from typing import List, Optional, Tuple

from graphsenselib.utils.address import address_to_user_format
from tagstore.algorithms.tag_digest import TagDigest, compute_tag_digest
from tagstore.db import TagPublic, TagstoreDbAsync

import gsrest.service.common_service as common
from gsrest.db.node_type import NodeType
from gsrest.errors import (
    AddressNotFoundException,
    ClusterNotFoundException,
    DBInconsistencyException,
)
from gsrest.service.blocks_service import get_min_max_height
from gsrest.service.common_service import (
    cannonicalize_address,
    get_tagstore_access_groups,
    try_get_cluster_id,
)
from gsrest.service.entities_service import from_row, get_entity
from gsrest.service.rates_service import get_rates
from gsrest.service.tags_service import (
    address_tag_from_PublicTag,
    get_address_tag_result,
)
from gsrest.util import is_eth_like
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.label_summary import LabelSummary
from openapi_server.models.neighbor_address import NeighborAddress
from openapi_server.models.neighbor_addresses import NeighborAddresses
from openapi_server.models.tag_cloud_entry import TagCloudEntry
from openapi_server.models.tag_summary import TagSummary


def tagSummary_from_tagDigest(td: TagDigest):
    return TagSummary(
        broad_category=td.broad_concept,
        tag_count=td.nr_tags,
        tag_count_indirect=td.nr_tags_indirect,
        best_actor=td.best_actor,
        best_label=td.best_label,
        concept_tag_cloud={
            k: TagCloudEntry(cnt=v.count, weighted=v.weighted)
            for k, v in td.concept_tag_cloud.items()
        },
        label_summary={
            key: LabelSummary(
                label=v.label,
                count=v.count,
                confidence=v.confidence,
                relevance=v.relevance,
                creators=v.creators,
                sources=v.sources,
                concepts=v.concepts,
                lastmod=v.lastmod,
                inherited_from=v.inherited_from,
            )
            for (key, v) in td.label_digest.items()
        },
    )


async def _get_best_cluster_tag_raw(
    request, currency, address
) -> Tuple[int, Optional[TagPublic]]:
    db = request.app["db"]
    tagstore_db = TagstoreDbAsync(request.app["gs-tagstore"])

    clstr_id = await try_get_cluster_id(db, currency, address)

    return clstr_id, await tagstore_db.get_best_cluster_tag(
        clstr_id, currency.upper(), get_tagstore_access_groups(request)
    )


async def get_best_cluster_tag(request, currency, address) -> AddressTag | None:
    clstr_id = tag = await _get_best_cluster_tag_raw(request, currency, address)

    if tag is not None:
        return address_tag_from_PublicTag(request, tag, clstr_id)

    return None


async def list_tags_by_address_raw(
    request, currency, address, page=None, pagesize=None, include_best_cluster_tag=False
) -> List[TagPublic]:
    address = address_to_user_format(currency, address)

    tsdb = TagstoreDbAsync(request.app["gs-tagstore"])

    page = int(page) if page is not None else 0

    tags = list(
        await tsdb.get_tags_by_subjectid(
            address,
            page * (pagesize or 0),
            pagesize,
            get_tagstore_access_groups(request),
            # network=currency.upper(),
        )
    )

    if include_best_cluster_tag and not is_eth_like(currency):
        _, best_cluster_tag = await _get_best_cluster_tag_raw(
            request, currency, address
        )
        if best_cluster_tag is not None:
            is_direct_tag = best_cluster_tag.identifier == address
            if not is_direct_tag:
                tags.append(best_cluster_tag)

    return tags


async def get_tag_summary_by_address(
    request, currency, address, include_best_cluster_tag=False
):
    address_canonical = cannonicalize_address(currency, address)

    tags = await list_tags_by_address_raw(
        request,
        currency,
        address_canonical,
        page=None,
        pagesize=None,
        include_best_cluster_tag=include_best_cluster_tag,
    )

    digest = compute_tag_digest(tags)

    return tagSummary_from_tagDigest(digest)


async def get_address(request, currency, address, include_actors=True):
    return await common.get_address(
        request, currency, address, include_actors=include_actors
    )


async def list_tags_by_address(
    request, currency, address, page=None, pagesize=None, include_best_cluster_tag=False
) -> AddressTags:
    page = int(page) if page is not None else 0
    db = request.app["db"]

    clstr_id = await try_get_cluster_id(db, currency, address)

    tags = [
        address_tag_from_PublicTag(request, pt, clstr_id)
        for pt in (
            await list_tags_by_address_raw(
                request,
                currency,
                address,
                page=page,
                pagesize=pagesize,
                include_best_cluster_tag=include_best_cluster_tag,
            )
        )
    ]

    async def add_foreign_network_clusters(tag):
        if tag.currency != currency:
            tag.entity = await try_get_cluster_id(db, tag.currency, address)
        return tag

    tags = [await add_foreign_network_clusters(t) for t in tags]

    return get_address_tag_result(page, pagesize, tags)


async def list_address_txs(
    request,
    currency,
    address,
    min_height=None,
    max_height=None,
    min_date=None,
    max_date=None,
    direction=None,
    order="desc",
    token_currency=None,
    page=None,
    pagesize=None,
):
    min_b, max_b = await get_min_max_height(
        request, currency, min_height, max_height, min_date, max_date
    )

    address = cannonicalize_address(currency, address)
    db = request.app["db"]
    results, paging_state = await db.list_address_txs(
        currency=currency,
        address=address,
        direction=direction,
        min_height=min_b,
        max_height=max_b,
        order=order,
        token_currency=token_currency,
        page=page,
        pagesize=pagesize,
    )

    address_txs = await common.txs_from_rows(
        request, currency, results, db.get_token_configuration(currency)
    )
    return AddressTxs(next_page=paging_state, address_txs=address_txs)


async def list_address_neighbors(
    request,
    currency,
    address,
    direction,
    only_ids=None,
    include_labels=False,
    include_actors=True,
    page=None,
    pagesize=None,
):
    address = cannonicalize_address(currency, address)
    db = request.app["db"]
    if isinstance(only_ids, list):
        aws = [
            db.get_address_id(currency, cannonicalize_address(currency, id))
            for id in only_ids
        ]
        only_ids = await asyncio.gather(*aws)
        only_ids = [id for id in only_ids if id is not None]

    results, paging_state = await common.list_neighbors(
        request,
        currency,
        address,
        direction,
        NodeType.ADDRESS,
        ids=only_ids,
        include_labels=include_labels,
        page=page,
        pagesize=pagesize,
    )
    is_outgoing = "out" in direction
    dst = "dst" if is_outgoing else "src"
    relations = []
    if results is None:
        return NeighborAddresses(neighbors=[])
    aws = [
        get_address(
            request,
            currency,
            address_to_user_format(currency, row[dst + "_address"]),
            include_actors=include_actors,
        )
        for row in results
    ]

    nodes = await asyncio.gather(*aws)

    for row, node in zip(results, nodes):
        nb = NeighborAddress(
            labels=row["labels"],
            value=row["value"],
            no_txs=row["no_transactions"],
            token_values=row.get("token_values", None),
            address=node,
        )
        relations.append(nb)

    return NeighborAddresses(next_page=paging_state, neighbors=relations)


async def list_address_links(
    request,
    currency,
    address,
    neighbor,
    min_height=None,
    max_height=None,
    min_date=None,
    max_date=None,
    order="desc",
    token_currency=None,
    page=None,
    pagesize=None,
):
    min_b, max_b = await get_min_max_height(
        request, currency, min_height, max_height, min_date, max_date
    )

    address = cannonicalize_address(currency, address)
    neighbor = cannonicalize_address(currency, neighbor)
    db = request.app["db"]
    result = await db.list_address_links(
        currency,
        address,
        neighbor,
        min_height=min_b,
        max_height=max_b,
        order=order,
        token_currency=token_currency,
        page=page,
        pagesize=pagesize,
    )

    return await common.links_response(request, currency, result)


async def get_address_entity(request, currency, address, include_actors=True):
    address_canonical = cannonicalize_address(currency, address)
    db = request.app["db"]
    try:
        entity_id = await db.get_address_entity_id(currency, address_canonical)
    except AddressNotFoundException:
        aws = [get_rates(request, currency), db.new_entity(currency, address_canonical)]
        [rates, entity] = await asyncio.gather(*aws)
        return from_row(
            currency, entity, rates["rates"], db.get_token_configuration(currency)
        )

    try:
        entity = await get_entity(
            request, currency, entity_id, include_actors=include_actors
        )
        # remove inherited indicator from tag.
        if (
            entity is not None
            and entity.best_address_tag is not None
            and entity.best_address_tag.address == address
        ):
            d = entity.best_address_tag.to_dict()
            d.pop("inherited_from")
            entity.best_address_tag = AddressTag.from_dict(d)
        return entity
    except ClusterNotFoundException:
        raise DBInconsistencyException(
            f"entity referenced by {address} in {currency} not found"
        )
