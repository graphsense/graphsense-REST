from flask import current_app
from openapi_server.models.stats import Stats
from openapi_server.models.search_result import SearchResult
from openapi_server.models.search_result_by_currency \
    import SearchResultByCurrency
from gsrest.service.stats_service import get_currency_statistics
from gsrest.service.txs_service import TX_PREFIX_LENGTH, list_matching_txs
from gsrest.service.tags_service import LABEL_PREFIX_LENGTH, list_labels
from gsrest.service.addresses_service import ADDRESS_PREFIX_LENGTH, \
        list_matching_addresses


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


def search(q, currency=None, limit=None):
    currencies = \
        [currency] if currency else \
        [c for c in current_app.config['MAPPING']
         if c != 'tagpacks']
    leading_zeros = 0
    pos = 0
    # leading zeros will be lost when casting to int
    while q[pos] == "0":
        pos += 1
        leading_zeros += 1

    q = q.strip()
    result = SearchResult(currencies=[], labels=[])

    for currency in currencies:
        element = SearchResultByCurrency(
                    currency=currency,
                    addresses=[],
                    txs=[]
                    )

        # Look for addresses and transactions
        if len(q) >= TX_PREFIX_LENGTH:
            txs = list_matching_txs(currency, q, leading_zeros)
            element.txs = txs[:limit]

        if len(q) >= ADDRESS_PREFIX_LENGTH:
            addresses = list_matching_addresses(currency, q)
            element.addresses = addresses[:limit]

        result.currencies.append(element)

        if len(q) >= LABEL_PREFIX_LENGTH:
            labels = list_labels(currency, q)[:limit]
            if labels:
                result.labels += labels

    return result
