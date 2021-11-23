import asyncio
from datetime import datetime
from openapi_server.models.stats import Stats
from openapi_server.models.search_result import SearchResult
from openapi_server.models.search_result_by_currency \
    import SearchResultByCurrency
from gsrest.service.stats_service import get_currency_statistics
from gsrest.util.string_edit import alphanumeric_lower


async def get_statistics(request):
    """
    Returns summary statistics on all available currencies
    """
    version = request.app['openapi']['info']['version']
    currency_stats = list()
    db = request.app['db']
    aws = [get_currency_statistics(request, currency, version)
           for currency in db.get_supported_currencies()]
    currency_stats = await asyncio.gather(*aws)

    tstamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return Stats(currencies=currency_stats,
                 version=version,
                 request_timestamp=tstamp)


async def search(request, q, currency=None, limit=10):
    db = request.app['db']
    currencies = db.get_supported_currencies()

    q = q.strip()
    result = SearchResult(currencies=[], labels=[])

    for curr in currencies:
        if currency is not None and currency.lower() != curr.lower():
            continue
        element = SearchResultByCurrency(
                    currency=curr,
                    addresses=[],
                    txs=[]
                    )

        expression_norm = alphanumeric_lower(q)

        [txs, addresses, labels] = await asyncio.gather(
            db.list_matching_txs(curr, q, limit),
            db.list_matching_addresses(curr, q, limit),
            db.list_labels(curr, expression_norm, limit)
        )

        # TODO improve by letting db limit the result during query
        element.txs = txs[:limit]
        element.addresses = addresses

        result.currencies.append(element)

        if labels:
            result.labels += labels
        result.labels = list(set(result.labels))

    return result
