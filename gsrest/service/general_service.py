import time
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
from gsrest.db import get_connection

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


async def get_statistics():
    """
    Returns summary statistics on all available currencies
    """
    with open('./openapi_server/openapi/openapi.yaml', 'r') as input_file:
        input = yaml.safe_load(input_file)
        version = input['info']['version']
        title = input['info']['title']
        currency_stats = list()
        db = get_connection()
        for currency in db.get_supported_currencies():
            currency_stats.append(
                await get_currency_statistics(currency, version))
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


def search(q, currency=None, limit=None):
    db = get_connection()
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

        # Look for addresses and transactions
        txs = list_matching_txs(curr, q)
        element.txs = txs[:limit]

        addresses = list_matching_addresses(curr, q)
        element.addresses = addresses[:limit]

        result.currencies.append(element)

        labels = list_labels(curr, q)[:limit]
        if labels:
            result.labels += labels

    return result
