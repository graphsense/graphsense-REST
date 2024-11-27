import asyncio
from datetime import datetime
from openapi_server.models.stats import Stats
from openapi_server.models.search_result import SearchResult
from openapi_server.models.labeled_item_ref import LabeledItemRef
from openapi_server.models.search_result_by_currency \
    import SearchResultByCurrency
from gsrest.service.stats_service import get_currency_statistics
from gsrest.service.tags_service import get_tagstore_access_groups
from gsrest.util.string_edit import alphanumeric_lower
from tagstore.db import TagstoreDbAsync


async def get_statistics(request):
    """
    Returns summary statistics on all available currencies
    """
    version = request.app['openapi']['info']['version']
    currency_stats = list()
    db = request.app['db']
    aws = [
        get_currency_statistics(request, currency)
        for currency in db.get_supported_currencies()
    ]
    currency_stats = await asyncio.gather(*aws)

    tstamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return Stats(currencies=currency_stats,
                 version=version,
                 request_timestamp=tstamp)


async def search_by_currency(request, currency, q, limit=10):
    db = request.app['db']

    r = SearchResultByCurrency(currency=currency, addresses=[], txs=[])

    if len(q) >= 3:
        [txs, addresses] = await asyncio.gather(
            db.list_matching_txs(currency, q, limit),
            db.list_matching_addresses(currency, q, limit),
        )
    else:
        txs = []
        addresses = []

    r.txs = txs
    r.addresses = addresses

    return r


async def search(request, q, currency=None, limit=10):
    db = request.app['db']
    currencies = db.get_supported_currencies()
    tsdb = TagstoreDbAsync(request.app["gs-tagstore"])

    q = q.strip()
    result = SearchResult(currencies=[], labels=[])

    currs = [
        curr for curr in currencies
        if currency is None or currency.lower() == curr.lower()
    ]

    expression_norm = alphanumeric_lower(q)

    tagstore_search = tsdb.search_labels(
        expression_norm, limit, groups=get_tagstore_access_groups(request))

    aws1 = [search_by_currency(request, curr, q) for curr in currs]
    aw1 = asyncio.gather(*aws1)

    [r1, r2] = await asyncio.gather(aw1, tagstore_search)

    result.labels = [x.label for x in r2.tag_labels]

    result.actors = [
        LabeledItemRef(id=x.id, label=x.label) for x in r2.actor_labels
    ]

    return result
