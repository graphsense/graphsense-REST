from flask import abort

from gsrest.db.cassandra import get_session
from gsrest.model.tags import Label, Tag
from gsrest.util.string_edit import alphanumeric_lower
from gsrest.util.checks import LABEL_PREFIX_LENGTH


def get_label(label):
    label_norm = alphanumeric_lower(label)
    label_norm_prefix = label_norm[:LABEL_PREFIX_LENGTH]

    session = get_session(currency=None, keyspace_type='tagpacks')
    query = "SELECT label_norm, label_norm_prefix, label, COUNT(address) as " \
            "address_count FROM tag_by_label WHERE label_norm_prefix = %s " \
            "and label_norm = %s GROUP BY label_norm_prefix, label_norm"
    result = session.execute(query, [label_norm_prefix, label_norm])
    if result:
        return Label.from_row(result[0]).to_dict()
    abort(404, "Label not found")


def list_tags(label, currency=None):
    label_norm = alphanumeric_lower(label)
    label_norm_prefix = label_norm[:LABEL_PREFIX_LENGTH]

    session = get_session(currency=None, keyspace_type='tagpacks')
    query = "SELECT * FROM tag_by_label WHERE label_norm_prefix = %s and " \
            "label_norm = %s"
    rows = session.execute(query, [label_norm_prefix, label_norm])
    if rows:
        if currency:
            return [Tag.from_address_row(row, row.currency).to_dict()
                    for row in rows if row.currency.lower() == currency]
        return [Tag.from_address_row(row, row.currency).to_dict()
                for row in rows]
    abort(404, "Label not found")


def list_labels(currency, expression):
    # Normalize label
    expression_norm = alphanumeric_lower(expression)
    expression_norm_prefix = expression_norm[:LABEL_PREFIX_LENGTH]

    session = get_session(currency=None, keyspace_type='tagpacks')
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
