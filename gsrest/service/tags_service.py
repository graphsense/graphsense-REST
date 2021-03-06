from gsrest.db import get_connection
from openapi_server.models.tag import Tag
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.concept import Concept
from gsrest.util.string_edit import alphanumeric_lower


def list_tags(label, currency=None):
    db = get_connection()
    label = alphanumeric_lower(label)
    tags = db.list_tags(label, currency)

    return [Tag(
            address=row.address,
            label=row.label,
            category=row.category,
            abuse=row.abuse,
            tagpack_uri=row.tagpack_uri,
            source=row.source,
            lastmod=row.lastmod,
            active=row.active_address,
            currency=row.currency)
            for row in tags]


def list_labels(currency, expression):
    # Normalize label
    expression_norm = alphanumeric_lower(expression)
    db = get_connection()
    result = db.list_labels(currency, expression_norm)

    if currency:
        return list(dict.fromkeys([
            row.label for row in result
            if row.label_norm.startswith(expression_norm) and
            row.currency.lower() == currency]))
    return list(dict.fromkeys([
        row.label for row in result
        if row.label_norm.startswith(expression_norm)]))


def list_concepts(taxonomy):
    db = get_connection()
    rows = db.list_concepts(taxonomy)

    return [Concept(
            id=row.id,
            label=row.label,
            description=row.description,
            taxonomy=row.taxonomy,
            uri=row.uri) for row in rows]


def list_taxonomies():
    db = get_connection()
    rows = db.list_taxonomies()

    return [Taxonomy(taxonomy=row.key, uri=row.uri) for row in rows]
