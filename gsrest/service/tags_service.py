import asyncio
from gsrest.db import get_connection
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.entity_tag import EntityTag
from openapi_server.models.tags import Tags
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.concept import Concept
from gsrest.util.string_edit import alphanumeric_lower


async def list_tags(label, currency=None):
    db = get_connection()
    label = alphanumeric_lower(label)
    if(currency is None):
        address_tags = []
        aws = [db.list_address_tags(curr, label)
               for curr in db.get_supported_currencies()]
        for tags in await asyncio.gather(*aws):
            address_tags += tags
    else:
        address_tags = await db.list_address_tags(currency, label)

    if(currency is None):
        entity_tags = []
        aws = [db.list_entity_tags(curr, label)
               for curr in db.get_supported_currencies()]
        for tags in await asyncio.gather(*aws):
            entity_tags += tags
    else:
        entity_tags = await db.list_entity_tags(currency, label)

    return Tags(address_tags=[AddressTag(
                                address=row['address'],
                                label=row['label'],
                                category=row['category'],
                                abuse=row['abuse'],
                                tagpack_uri=row['tagpack_uri'],
                                source=row['source'],
                                lastmod=row['lastmod'],
                                active=row['active'],
                                currency=row['currency'])
                              for row in address_tags],
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
                             for row in entity_tags])


async def list_labels(currency, expression):
    # Normalize label
    expression_norm = alphanumeric_lower(expression)
    db = get_connection()
    result = await db.list_labels(currency, expression_norm)

    if currency:
        return list(dict.fromkeys([
            row['label'] for row in result
            if row['label_norm'].startswith(expression_norm) and
            row['currency'].lower() == currency]))
    return list(dict.fromkeys([
        row['label'] for row in result
        if row['label_norm'].startswith(expression_norm)]))


def list_concepts(taxonomy):
    db = get_connection()
    rows = db.list_concepts(taxonomy)

    return [Concept(
            id=row['id'],
            label=row['label'],
            description=row['description'],
            taxonomy=row['taxonomy'],
            uri=row['uri']) for row in rows]


def list_taxonomies():
    db = get_connection()
    rows = db.list_taxonomies()

    return [Taxonomy(taxonomy=row['key'], uri=row['uri']) for row in rows]
