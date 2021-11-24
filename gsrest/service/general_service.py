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

    currs = [curr for curr in currencies
             if currency is None or currency.lower() == curr.lower()]

    expression_norm = alphanumeric_lower(q)

    async def s(curr):
        r = SearchResultByCurrency(currency=curr,
                                   addresses=[],
                                   txs=[])

        [txs, addresses] = await asyncio.gather(
            db.list_matching_txs(curr, q, limit),
            db.list_matching_addresses(curr, q, limit),
        )

        r.txs = txs
        r.addresses = addresses
        return r

    aws1 = [s(curr) for curr in currs]
    aws2 = [db.list_matching_labels(curr, expression_norm, limit)
            for curr in currs]

    aw1 = asyncio.gather(*aws1)
    aw2 = asyncio.gather(*aws2)

    [r1, r2] = await asyncio.gather(aw1, aw2)

    result.currencies = r1
    for labels in r2:
        if labels:
            result.labels += labels

    result.labels = sorted(list(set(result.labels)), key=lambda x: x.lower())

    return result
