import asyncio
from typing import Callable, List, Optional

from tagstore.db import ActorPublic, TagPublic, TagstoreDbAsync, Taxonomies

from gsrest.db import get_cached_is_abuse, get_cached_taxonomy_concept_label
from gsrest.errors import NotFoundException
from gsrest.service.common_service import get_tagstore_access_groups, try_get_cluster_id
from openapi_server.models.actor import Actor
from openapi_server.models.actor_context import ActorContext
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.concept import Concept
from openapi_server.models.labeled_item_ref import LabeledItemRef
from openapi_server.models.taxonomy import Taxonomy


def address_tag_from_PublicTag(
    request, pt: TagPublic, entity: Optional[int]
) -> AddressTag:
    abuse = next((x for x in pt.concepts if get_cached_is_abuse(request.app, x)), None)
    return AddressTag(
        address=pt.identifier,
        entity=entity,
        label=pt.label,
        category=pt.primary_concept,
        concepts=pt.additional_concepts,
        actor=pt.actor,
        tag_type=pt.tag_type,
        abuse=abuse,
        source=pt.source,
        lastmod=pt.lastmod,
        tagpack_is_public=pt.group == "public",
        tagpack_uri=pt.tagpack_uri,
        tagpack_creator=pt.creator,
        tagpack_title=pt.tagpack_title,
        confidence=pt.confidence,
        confidence_level=pt.confidence_level,
        is_cluster_definer=pt.is_cluster_definer,
        inherited_from=pt.inherited_from.name.lower() if pt.inherited_from else None,
        currency=pt.network.upper(),
    )


def get_address_tag_result(
    current_page: int, page_size: int, tags: List[AddressTag]
) -> AddressTags:
    tcnt = len(tags)
    np = current_page + 1 if (tcnt > 0 and tcnt == page_size) else None
    return AddressTags(next_page=str(np) if np is not None else None, address_tags=tags)


async def get_entities_dict(request, tags: List[TagPublic]):
    db = request.app["db"]
    queryItems = list({(t.identifier, t.network) for t in tags})
    entityQueries = [try_get_cluster_id(db, n, i) for i, n in queryItems]
    return {q: d for q, d in zip(queryItems, await asyncio.gather(*entityQueries))}


def actor_from_ActorPublic(
    ap: ActorPublic, label_for_idFn: Callable[[Taxonomies, str], str]
) -> Actor:
    has_context = (
        ap.additional_uris
        or ap.image_links
        or ap.online_references
        or ap.coingecko_ids
        or ap.defilama_ids
        or ap.twitter_handles
        or ap.github_organisations
        or ap.legal_name
    )
    return Actor(
        id=ap.id,
        uri=ap.primary_uri,
        label=ap.label,
        jurisdictions=[
            LabeledItemRef(id=x, label=label_for_idFn(Taxonomies.COUNTRY, x))
            for x in ap.jurisdictions
        ],
        categories=[
            LabeledItemRef(id=x, label=label_for_idFn(Taxonomies.CONCEPT, x))
            for x in ap.concepts
        ],
        nr_tags=ap.nr_tags,
        context=ActorContext(
            uris=ap.additional_uris,
            images=ap.image_links,
            refs=ap.online_references,
            coingecko_ids=ap.coingecko_ids,
            defilama_ids=ap.defilama_ids,
            twitter_handle=",".join(ap.twitter_handles),
            github_organisation=",".join(ap.github_organisations),
            legal_name=ap.legal_name,
        )
        if (has_context)
        else None,
    )


async def get_actor(request, actor):
    tsdb = TagstoreDbAsync(request.app["gs-tagstore"])

    a = await tsdb.get_actor_by_id(actor, include_tag_count=True)

    if a is None:
        raise NotFoundException(f"Actor {actor} not found.")
    else:
        return actor_from_ActorPublic(
            a,
            label_for_idFn=lambda t, x: get_cached_taxonomy_concept_label(
                request.app, t, x
            ),
        )


async def get_actor_tags(request, actor, page=None, pagesize=None):
    tsdb = TagstoreDbAsync(request.app["gs-tagstore"])

    page = int(page) if page is not None else 0

    tags = await tsdb.get_tags_by_actorid(
        actor,
        offset=page * (pagesize or 0),
        page_size=pagesize,
        groups=get_tagstore_access_groups(request),
    )

    tagEntities = await get_entities_dict(request, tags)

    return get_address_tag_result(
        page,
        pagesize,
        [
            address_tag_from_PublicTag(
                request, t, tagEntities[(t.identifier, t.network)]
            )
            for t in tags
        ],
    )


async def list_address_tags(request, label, page=None, pagesize=None):
    tsdb = TagstoreDbAsync(request.app["gs-tagstore"])
    page = int(page) if page is not None else 0

    tags = await tsdb.get_tags_by_label(
        label,
        offset=page * (pagesize or 0),
        page_size=pagesize,
        groups=get_tagstore_access_groups(request),
    )

    tagEntities = await get_entities_dict(request, tags)

    return get_address_tag_result(
        page,
        pagesize,
        [
            address_tag_from_PublicTag(
                request, t, tagEntities[(t.identifier, t.network)]
            )
            for t in tags
        ],
    )


async def list_concepts(request, taxonomy):
    taxonomy = taxonomy.lower().strip()
    tsdb = TagstoreDbAsync(request.app["gs-tagstore"])

    # for backwards comp.
    only_abuses = False
    if taxonomy == "entity":
        taxonomy = "concept"

    if taxonomy == "abuse":
        only_abuses = True
        taxonomy = "concept"

    if taxonomy not in [x.value for x in Taxonomies]:
        raise NotFoundException(f"Taxonomy {taxonomy} does not exist.")

    taxs = await tsdb.get_taxonomies({Taxonomies[taxonomy.upper()]})

    result = []

    for k, v in taxs:
        if v is None:
            continue

        for x in v:
            if only_abuses and not x.is_abuse:
                continue
            result.append(
                Concept(
                    id=x.id,
                    label=x.label,
                    description=x.description,
                    taxonomy=x.taxonomy,
                    uri=x.source,
                )
            )

    return result


async def list_taxonomies(request):
    tsdb = TagstoreDbAsync(request.app["gs-tagstore"])

    taxs = await tsdb.get_taxonomies()

    return [
        Taxonomy(
            taxonomy=k,
            uri=(
                "https://github.com/graphsense/"
                "graphsense-tagpack-tool/tree/master/src/tagpack/db"
            ),
        )
        for k, v in taxs
    ]
