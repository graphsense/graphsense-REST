import asyncio
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.entity_tag import EntityTag
from openapi_server.models.entity_tags import EntityTags
from openapi_server.models.tags import Tags
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.concept import Concept
from gsrest.util.string_edit import alphanumeric_lower


async def list_tags(request, currency, label, level, page=None,
                    pagesize=None):
    db = request.app['db']
    label = alphanumeric_lower(label)
    tags = []
    fun = db.list_address_tags if level == 'address' else db.list_entity_tags
    tags, next_page = await fun(currency, label, page=page, pagesize=pagesize)

    if level == 'address':
        return AddressTags(
            next_page=next_page,
            address_tags=[AddressTag(
                address=row['address'],
                label=row['label'],
                category=row['category'],
                abuse=row['abuse'],
                tagpack_uri=row['tagpack_uri'],
                source=row['source'],
                lastmod=row['lastmod'],
                active=row['active'],
                currency=row['currency'])
                for row in tags])
    return EntityTags(
            next_page=next_page,
            entity_tags=[EntityTag(
                entity=row['cluster_id'],
                label=row['label'],
                category=row['category'],
                abuse=row['abuse'],
                tagpack_uri=row['tagpack_uri'],
                source=row['source'],
                lastmod=row['lastmod'],
                active=row['active'],
                currency=row['currency'])
                for row in tags])


async def list_concepts(request, taxonomy):
    db = request.app['db']
    rows = await db.list_concepts(taxonomy)

    return [Concept(
            id=row['id'],
            label=row['label'],
            description=row['description'],
            taxonomy=row['taxonomy'],
            uri=row['uri']) for row in rows]


async def list_taxonomies(request):
    aws = [ts.list_taxonomies() for ts in request.app['tagstores']]
    results = await asyncio.gather(*aws)

    return [Taxonomy(taxonomy=row['id'], uri=row['source'])
            for rows in results
            for row in rows]
