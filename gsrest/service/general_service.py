import asyncio
from datetime import datetime
from openapi_server.models.stats import Stats
from openapi_server.models.search_result import SearchResult
from openapi_server.models.search_result_by_currency \
    import SearchResultByCurrency
from gsrest.service.stats_service import get_currency_statistics
from gsrest.service.txs_service import list_matching_txs
from gsrest.service.tags_service import list_labels
from gsrest.service.addresses_service import list_matching_addresses


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


async def search(request, q, currency=None, limit=None):
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

        [txs, addresses, labels] = await asyncio.gather(
            list_matching_txs(request, curr, q),
            list_matching_addresses(request, curr, q),
            list_labels(request, curr, q)
        )

        # TODO improve by letting db limit the result during query
        element.txs = txs[:limit]
        element.addresses = addresses[:limit]

        result.currencies.append(element)

        if labels:
            result.labels += labels
        result.labels = list(set(result.labels))

    return result
