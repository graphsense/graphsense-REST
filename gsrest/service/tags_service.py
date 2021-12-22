from openapi_server.models.address_tag import AddressTag
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.entity_tag import EntityTag
from openapi_server.models.entity_tags import EntityTags
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.concept import Concept
from gsrest.util.string_edit import alphanumeric_lower
from gsrest.db.util import tagstores, tagstores_with_paging, dt_to_int


async def list_tags(request, currency, label, level, page=None,
                    pagesize=None):

    if level == 'address':
        fun = 'list_address_tags'

        def to_obj(row):
            return AddressTag(
                address=row['address'],
                label=row['label'],
                category=row['category'],
                abuse=row['abuse'],
                tagpack_uri=row['tagpack'],
                source=row['source'],
                lastmod=dt_to_int(row['lastmod']),
                active=True,
                currency=row['currency'].upper())
    else:
        fun = 'list_entity_tags'

        def to_obj(row):
            return EntityTag(
                entity=row['cluster_id'],
                label=row['label'],
                category=row['category'],
                abuse=row['abuse'],
                tagpack_uri=row['tagpack'],
                source=row['source'],
                lastmod=dt_to_int(row['lastmod']),
                active=True,
                currency=row['currency'].upper())

    label = alphanumeric_lower(label)
    tags, next_page = await tagstores_with_paging(
        request.app['tagstores'], to_obj, fun, page, pagesize, currency, label)
    print(f'tags {tags}')

    if level == 'address':
        return AddressTags(next_page=next_page, address_tags=tags)
    return EntityTags(next_page=next_page, entity_tags=tags)


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
