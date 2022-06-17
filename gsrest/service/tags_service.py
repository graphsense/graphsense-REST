from openapi_server.models.address_tag import AddressTag
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.concept import Concept
from gsrest.db.util import tagstores, tagstores_with_paging, dt_to_int


def address_tag_from_row(row):
    return AddressTag(
        address=row['address'],
        label=row['label'],
        category=row['category'],
        abuse=row['abuse'],
        source=row['source'],
        lastmod=dt_to_int(row['lastmod']),
        tagpack_is_public=row['is_public'],
        tagpack_uri=row['uri'],
        tagpack_creator=row['creator'],
        tagpack_title=row['title'],
        confidence=row['confidence'],
        confidence_level=row['level'],
        is_cluster_definer=bool(row['is_cluster_definer']),
        currency=row['currency'].upper())


async def list_address_tags(request, label, page=None,
                            pagesize=None):
    fun = 'list_address_tags'
    to_obj = address_tag_from_row

    if pagesize is None:
        pagesize = 100
    pagesize = min(pagesize, 100)

    tags, next_page = await tagstores_with_paging(
        request.app['tagstores'], to_obj, fun, page, pagesize,
        label, request.app['show_private_tags'])

    return AddressTags(next_page=next_page, address_tags=tags)


async def list_concepts(request, taxonomy):
    return await tagstores(
        request.app['tagstores'],
        lambda row:
        Concept(
            id=row['id'],
            label=row['label'],
            description=row['description'],
            taxonomy=row['taxonomy'],
            uri=row['source']),
        'list_concepts',
        taxonomy)


async def list_taxonomies(request):
    return await tagstores(
        request.app['tagstores'],
        lambda row:
        Taxonomy(taxonomy=row['id'], uri=row['source']),
        'list_taxonomies')
