from flask import current_app
from gsrest.db.cassandra import get_session
from openapi_server.models.tag import Tag
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.concept import Concept
from gsrest.util.checks import LABEL_PREFIX_LENGTH
from gsrest.util.string_edit import alphanumeric_lower


def list_tags(label, currency=None):
    if(currency is None):
        tags = []
        for currency in current_app.config['MAPPING']:
            if currency != "tagpacks":
                tags += list_tags(label, currency)
        return tags

    label_norm = alphanumeric_lower(label)
    label_norm_prefix = label_norm[:LABEL_PREFIX_LENGTH]

    session = get_session(currency=currency, keyspace_type='transformed')
    query = "SELECT * FROM tag_by_label WHERE label_norm_prefix = %s and " \
            "label_norm = %s"
    rows = session.execute(query, [label_norm_prefix, label_norm])
    if not rows:
        return []
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
            for row in rows]


def list_labels(currency, expression):
    # Normalize label
    expression_norm = alphanumeric_lower(expression)
    expression_norm_prefix = expression_norm[:LABEL_PREFIX_LENGTH]

    session = get_session(currency=currency, keyspace_type='transformed')
    query = "SELECT label, label_norm, currency FROM tag_by_label WHERE " \
            "label_norm_prefix = %s GROUP BY label_norm_prefix, label_norm"
    result = session.execute(query, [expression_norm_prefix])

    if currency:
        return list(dict.fromkeys([
            row.label for row in result
            if row.label_norm.startswith(expression_norm) and
            row.currency.lower() == currency]))
    return list(dict.fromkeys([
        row.label for row in result
        if row.label_norm.startswith(expression_norm)]))


def list_concepts(taxonomy):
    session = get_session(currency=None, keyspace_type='tagpacks')

    query = "SELECT * FROM concept_by_taxonomy_id WHERE taxonomy = %s"
    rows = session.execute(query, [taxonomy])
    return [Concept(
            id=row.id,
            label=row.label,
            description=row.description,
            taxonomy=row.taxonomy,
            uri=row.uri) for row in rows]


def list_taxonomies():
    session = get_session(currency=None, keyspace_type='tagpacks')

    query = "SELECT * FROM taxonomy_by_key LIMIT 100"
    rows = session.execute(query)
    return [Taxonomy(taxonomy=row.key, uri=row.uri) for row in rows]
