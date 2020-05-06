from gsrest.db.cassandra import get_session
from gsrest.model.general import Statistics, Concept


def get_statistics(currency):
    session = get_session(currency, 'transformed')
    query = "SELECT * FROM summary_statistics LIMIT 1"
    result = session.execute(query)
    if result:
        return Statistics.from_row(result[0], currency).to_dict()
    return None


def list_concepts(taxonomy):
    session = get_session(currency=None, keyspace_type='tagpacks')

    query = "SELECT * FROM concept_by_taxonomy_id WHERE taxonomy = %s"
    rows = session.execute(query, [taxonomy])
    return [Concept.from_row(row).to_dict() for row in rows]
