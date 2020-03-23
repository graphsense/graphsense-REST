from gsrest.db.cassandra import get_session
from gsrest.model.general import Statistics, Category, Abuse


def get_statistics(currency):
    session = get_session(currency, 'transformed')
    query = "SELECT * FROM summary_statistics LIMIT 1"
    result = session.execute(query)
    if result:
        return Statistics.from_row(result[0], currency).to_dict()
    return None


def list_categories():
    session = get_session(currency=None, keyspace_type='tagpacks')
    query = session.prepare("SELECT * FROM categories")
    rows = session.execute(query)
    return [Category.from_row(row).to_dict() for row in rows]


def list_abuses():
    session = get_session(currency=None, keyspace_type='tagpacks')
    query = session.prepare("SELECT * FROM abuses")
    rows = session.execute(query)
    return [Abuse.from_row(row).to_dict() for row in rows]
