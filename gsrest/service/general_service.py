from flask import current_app
from gsrest.db.cassandra import get_session
from openapi_server.models.stats import Stats
from openapi_server.models.currency_stats import CurrencyStats


def get_statistics():
    """
    Returns summary statistics on all available currencies
    """
    currency_stats = list()
    for currency in current_app.config['MAPPING']:
        if currency == "tagpacks":
            continue
        session = get_session(currency, 'transformed')
        query = "SELECT * FROM summary_statistics LIMIT 1"
        result = session.execute(query)
        if not result:
            continue
        print('result {}'.format(result[0]), flush=True)
        currency_stats.append(
            CurrencyStats(
                currency,
                result[0].no_blocks,
                result[0].no_address_relations,
                result[0].no_addresses,
                result[0].no_clusters,
                result[0].no_transactions,
                result[0].no_tags,
                result[0].timestamp
            )
        )
    return Stats(currency_stats)
