from gsrest.db.cassandra import get_session
from gsrest.model.general import Statistics


def get_statistics(currency):
    session = get_session(currency, 'transformed')
    query = "SELECT * FROM summary_statistics LIMIT 1"
    result = session.execute(query)
    if result:
        return Statistics.from_row(result[0], currency).to_dict()
    return None
