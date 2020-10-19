from flask import current_app
from gsrest.db.cassandra import get_session
from openapi_server.models.stats import Stats
from openapi_server.models.currency_stats import CurrencyStats
from gsrest.service.problems import notfound


def get_statistics():
    """
    Returns summary statistics on all available currencies
    """
    currency_stats = list()
    for currency in current_app.config['MAPPING']:
        if currency == "tagpacks":
            continue
        currency_stats.append(get_currency_statistics(currency))
    return Stats(currency_stats)


def get_currency_statistics(currency):
    session = get_session(currency, 'transformed')
    query = "SELECT * FROM summary_statistics LIMIT 1"
    result = session.execute(query).one()
    if result is None:
        notfound('statistics for currency {} not found'.format(currency))
    return CurrencyStats(
            name=currency,
            no_blocks=result.no_blocks,
            no_address_relations=result.no_address_relations,
            no_addresses=result.no_addresses,
            no_entities=result.no_clusters,
            no_txs=result.no_transactions,
            no_labels=result.no_tags,
            timestamp=result.timestamp
        )
