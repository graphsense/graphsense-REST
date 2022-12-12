import asyncio
from datetime import datetime
from openapi_server.models.stats import Stats
from openapi_server.models.search_result import SearchResult
from openapi_server.models.search_result_by_currency \
    import SearchResultByCurrency
from gsrest.service.stats_service import get_currency_statistics
from gsrest.util.string_edit import alphanumeric_lower
from gsrest.db.util import tagstores
from fuzzy_match import algorithims


async def get_statistics(request):
    """
    Returns summary statistics on all available currencies
    """
    version = request.app['openapi']['info']['version']
    currency_stats = list()
    db = request.app['db']
    aws = [get_currency_statistics(request, currency)
           for currency in db.get_supported_currencies()]
    currency_stats = await asyncio.gather(*aws)

    tstamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return Stats(currencies=currency_stats,
                 version=version,
                 request_timestamp=tstamp)


async def search_by_currency(request, currency, q, limit=10):
    db = request.app['db']

    r = SearchResultByCurrency(currency=currency,
                               addresses=[],
                               txs=[])

    [txs, addresses] = await asyncio.gather(
        db.list_matching_txs(currency, q, limit),
        db.list_matching_addresses(currency, q, limit),
    )

    r.txs = txs
    r.addresses = addresses

    return r


async def search(request, q, currency=None, limit=10):
    db = request.app['db']
    currencies = db.get_supported_currencies()

    q = q.strip()
    result = SearchResult(currencies=[], labels=[])

    currs = [curr for curr in currencies
             if currency is None or currency.lower() == curr.lower()]

    expression_norm = alphanumeric_lower(q)

    def ts(curr=None):
        return tagstores(
                    request.app['tagstores'],
                    lambda row: row['label'],
                    'list_matching_labels',
                    curr, expression_norm, limit,
                    request.app['show_private_tags'])

    aws1 = [search_by_currency(request, curr, q) for curr in currs]
    if currency:
        aws2 = [ts(curr) for curr in currs]
    else:
        aws2 = [ts()]

    aw3 = tagstores(
        request.app['tagstores'],
        lambda row: row['label'],
        'list_matching_actors',
        expression_norm, limit,
        request.app['show_private_tags'])

    aw1 = asyncio.gather(*aws1)
    aw2 = asyncio.gather(*aws2)

    [r1, r2, r3] = await asyncio.gather(aw1, aw2, aw3)

    result.currencies = r1
    for labels in r2:
        if labels:
            result.labels += labels

    result.labels = sorted(list(set(result.labels)),
                           key=lambda x: -algorithims.trigram(x.lower(),
                                                              expression_norm))

    result.actors = r3

    return result
