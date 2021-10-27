import time
import asyncio
from aiohttp import web
from openapi_server.models.stats import Stats
from openapi_server.models.stats_version import StatsVersion
from openapi_server.models.stats_tool import StatsTool
from openapi_server.models.stats_tags_source import StatsTagsSource
from openapi_server.models.stats_note import StatsNote
from openapi_server.models.search_result import SearchResult
from openapi_server.models.search_result_by_currency \
    import SearchResultByCurrency
from gsrest.service.stats_service import get_currency_statistics
from gsrest.service.txs_service import list_matching_txs
from gsrest.service.tags_service import list_labels
from gsrest.service.addresses_service import list_matching_addresses

import yaml

note1 = ('Please **note** that the clustering dataset is built with'
         ' multi input address clustering to avoid false clustering '
         'results due to coinjoins (see TITANIUM glossary '
         'http://titanium-project.eu/glossary/#coinjoin), we exclude'
         ' coinjoins prior to clustering. This does not eliminate '
         'the risk of false results, since coinjoin detection is also'
         ' heuristic in nature, but it should decrease the potential '
         'for wrong cluster merges.')


note2 = ('Our tags are all manually crawled or from credible sources,'
         ' we do not use tags that where automatically extracted '
         'without human interaction. Origins of the tags have been '
         'saved for reproducibility please contact the GraphSense '
         'team (contact@graphsense.info) for more insight.')


def execute_async(session, q):
    response_future = session.execute_async(q)
    loop = asyncio.get_event_loop()
    future = loop.create_future()

    def on_done(result):
        loop.call_soon_threadsafe(future.set_result, result)

    def on_err(result):
        loop.call_soon_threadsafe(future.set_exception, result)

    response_future.add_callbacks(on_done, on_err)
    return future


async def get_statistics_old(request):
    print(f'run start {time.time()}')
    title = "bla"
    version = '0.5'
    currency_stats = await get_currency_statistics(request, 'btc', version)
    print(f'scheduled {time.time()}')
    return Stats(
            currencies=currency_stats,
            version=StatsVersion(
                nr=version,
                hash=None,
                timestamp=time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.gmtime()),
                file=version),
            tools=[StatsTool(
                visible_name=title,
                version=version,
                id='ait:graphsense',
                titanium_replayable=False,
                responsible_for=[]
                )],
            tags_source=StatsTagsSource(
                visible_name="GraphSense attribution tags",
                version=version,
                id="graphsense_tags",
                report_uuid="graphsense_tags"),
            notes=[StatsNote(note=note1),
                   StatsNote(note=note2)])


async def get_statistics(request):
    """
    Returns summary statistics on all available currencies
    """
    version = request.app['openapi']['info']['version']
    title = request.app['openapi']['info']['title']
    currency_stats = list()
    db = request.app['db']
    aws = [get_currency_statistics(request, currency, version)
           for currency in db.get_supported_currencies()]
    currency_stats = await asyncio.gather(*aws)

    return Stats(
            currencies=currency_stats,
            version=StatsVersion(
                nr=version,
                hash=None,
                timestamp=time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.gmtime()),
                file=version),
            tools=[StatsTool(
                visible_name=title,
                version=version,
                id='ait:graphsense',
                titanium_replayable=False,
                responsible_for=[]
                )],
            tags_source=StatsTagsSource(
                visible_name="GraphSense attribution tags",
                version=version,
                id="graphsense_tags",
                report_uuid="graphsense_tags"),
            notes=[StatsNote(note=note1),
                   StatsNote(note=note2)])


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

    return result
