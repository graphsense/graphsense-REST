from gsrest.db.cassandra import get_session
from gsrest.model.tags import Tag, Concept, Taxonomy
from gsrest.util.checks import LABEL_PREFIX_LENGTH
from gsrest.util.string_edit import alphanumeric_lower


def list_tags(label, currency=None):
    label_norm = alphanumeric_lower(label)
    label_norm_prefix = label_norm[:LABEL_PREFIX_LENGTH]

    session = get_session(currency=currency, keyspace_type='transformed')
    query = "SELECT * FROM tag_by_label WHERE label_norm_prefix = %s and " \
            "label_norm = %s"
    rows = session.execute(query, [label_norm_prefix, label_norm])
    if rows:
        return [Tag.from_address_row(row, row.currency).to_dict()
                for row in rows]
    return None


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
            if row.label_norm.startswith(expression_norm)
            and row.currency.lower() == currency]))
    return list(dict.fromkeys([
        row.label for row in result
        if row.label_norm.startswith(expression_norm)]))


def list_concepts(taxonomy):
    session = get_session(currency=None, keyspace_type='tagpacks')

    query = "SELECT * FROM concept_by_taxonomy_id WHERE taxonomy = %s"
    rows = session.execute(query, [taxonomy])
    return [Concept.from_row(row).to_dict() for row in rows]


def list_taxonomies():
    session = get_session(currency=None, keyspace_type='tagpacks')

    query = "SELECT * FROM taxonomy_by_key LIMIT 100"
    rows = session.execute(query)
    return [Taxonomy.from_row(row).to_dict() for row in rows]
