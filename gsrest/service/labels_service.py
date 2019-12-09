from gsrest.db.cassandra import get_session
from gsrest.model.tags import Label, Tag
from gsrest.util.checks import alphanumeric_lower

LABEL_PREFIX_LENGTH = 3


def get_label(label):
    # TODO: allow user to filter by currency
    label_norm = alphanumeric_lower(label)
    label_norm_prefix = label_norm[:LABEL_PREFIX_LENGTH]

    session = get_session(currency=None, keyspace_type='tagpacks')
    query = "SELECT label_norm, label_norm_prefix, label, COUNT(address) as " \
            "address_count FROM tag_by_label WHERE label_norm_prefix = %s " \
            "and label_norm = %s GROUP BY label_norm_prefix, label_norm"
    result = session.execute(query, [label_norm_prefix, label_norm])
    return Label.from_row(result[0]).to_dict() if result else None


def list_tags(label):
    # TODO: allow user to filter by currency
    label_norm = alphanumeric_lower(label)
    label_norm_prefix = label_norm[:LABEL_PREFIX_LENGTH]

    session = get_session(currency=None, keyspace_type='tagpacks')
    query = "SELECT * FROM tag_by_label WHERE label_norm_prefix = %s and " \
            "label_norm = %s"
    rows = session.execute(query, [label_norm_prefix, label_norm])
    return [Tag.from_address_row(row, row.currency).to_dict() for row in rows]\
        if rows else None
