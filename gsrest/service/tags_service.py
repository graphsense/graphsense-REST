import json
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.concept import Concept

from openapi_server.models.actor import Actor
from openapi_server.models.actor_context import ActorContext
from gsrest.db.util import tagstores, tagstores_with_paging, dt_to_int


def address_tag_from_row(row):
    return AddressTag(address=row['address'],
                      entity=row['gs_cluster_id'],
                      label=row['label'],
                      category=row['category'],
                      abuse=row['abuse'],
                      source=row['source'],
                      lastmod=dt_to_int(row['lastmod']),
                      tagpack_is_public=row['is_public'],
                      tagpack_uri=row['tagpack'] if row['is_public'] else None,
                      tagpack_creator=row['creator'],
                      tagpack_title=row['title'],
                      confidence=row['confidence'],
                      confidence_level=row['level'],
                      is_cluster_definer=bool(row['is_cluster_definer']),
                      currency=row['currency'].upper())


def actor_context_from_row(context_str):
    if context_str is None:
        return None
    ctx = json.loads(context_str)
    return ActorContext(
        uris=ctx.get("uris", None),
        images=ctx.get("images", None),
        refs=ctx.get("refs", None),
        coingecko_ids=ctx.get("coingecko_ids", None),
        defilama_ids=ctx.get("defilama_ids", None),
        twitter_handle=ctx.get("twitter_handle", None),
        github_organisation=ctx.get("github_organisation", None),
        legal_name=ctx.get("legal_name", None),
    )


def actor_from_row(row, jurisdictions, categories):
    return Actor(id=row["id"],
                 uri=row["uri"],
                 label=row["label"],
                 jurisdictions=[x["country_id"] for x in jurisdictions],
                 categories=[x["category_id"] for x in categories],
                 context=actor_context_from_row(row["context"]))


async def get_actor(request, actor):
    actor_cr = await tagstores(request.app['tagstores'], lambda x: x,
                               'get_actor', actor)

    categories = await tagstores(request.app['tagstores'], lambda x: x,
                                 'get_actor_categories', actor)

    jurisdictions = await tagstores(request.app['tagstores'], lambda x: x,
                                    'get_actor_jurisdictions', actor)

    actor_row = actor_cr

    if len(actor_row) == 0:
        raise RuntimeError(f"Actor {actor} not found.")
    else:
        return actor_from_row(actor_row[0], jurisdictions, categories)


async def get_actor_tags(request, actor, page=None, pagesize=None):
    fun = 'list_address_tags_for_actor'
    to_obj = address_tag_from_row

    if pagesize is None:
        pagesize = 100
    pagesize = min(pagesize, 100)

    tags, next_page = await tagstores_with_paging(
        request.app['tagstores'], to_obj, fun, page, pagesize, actor,
        request.app['show_private_tags'])

    return AddressTags(next_page=next_page, address_tags=tags)


async def list_address_tags(request, label, page=None, pagesize=None):
    fun = 'list_address_tags'
    to_obj = address_tag_from_row

    if pagesize is None:
        pagesize = 100
    pagesize = min(pagesize, 100)

    tags, next_page = await tagstores_with_paging(
        request.app['tagstores'], to_obj, fun, page, pagesize, label,
        request.app['show_private_tags'])

    return AddressTags(next_page=next_page, address_tags=tags)


async def list_concepts(request, taxonomy):
    return await tagstores(
        request.app['tagstores'],
        lambda row: Concept(id=row['id'],
                            label=row['label'],
                            description=row['description'],
                            taxonomy=row['taxonomy'],
                            uri=row['source']), 'list_concepts', taxonomy)


async def list_taxonomies(request):
    return await tagstores(
        request.app['tagstores'],
        lambda row: Taxonomy(taxonomy=row['id'], uri=row['source']),
        'list_taxonomies')
