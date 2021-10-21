from gsrest.test.assertion import assertEqual
import gsrest.service.general_service as service
from openapi_server.models.stats import Stats
from openapi_server.models.stats_ledger import StatsLedger
from openapi_server.models.stats_ledger_version import StatsLedgerVersion
from openapi_server.models.search_result import SearchResult
from openapi_server.models.search_result_by_currency \
        import SearchResultByCurrency
from openapi_server.models.currency_stats import CurrencyStats

stats = Stats(
    currencies=[
        CurrencyStats(
            name='btc',
            no_entities=7890,
            no_addresses=4560,
            no_blocks=3,
            timestamp=420,
            no_txs=110,
            no_labels=470,
            no_address_relations=1230,
            notes=[],
            tools=[],
            data_sources=[StatsLedger(
                id='btc_ledger',
                report_uuid='btc_ledger',
                visible_name='BTC Blockchain',
                version=StatsLedgerVersion(
                    nr='3', timestamp='1970-01-01 00:07:00'),
                )]
            ),
        CurrencyStats(
            name='eth',
            no_entities=0,
            no_addresses=1,
            no_blocks=3,
            timestamp=16,
            no_txs=10,
            no_labels=7,
            no_address_relations=2,
            notes=[],
            tools=[],
            data_sources=[StatsLedger(
                id='eth_ledger',
                report_uuid='eth_ledger',
                visible_name='ETH Blockchain',
                version=StatsLedgerVersion(
                    nr='3', timestamp='1970-01-01 00:00:16'),
                )]
            ),
        CurrencyStats(
            name='ltc',
            no_entities=789,
            no_addresses=456,
            no_blocks=3,
            timestamp=42,
            no_txs=11,
            no_labels=47,
            no_address_relations=123,
            notes=[],
            tools=[],
            data_sources=[StatsLedger(
                id='ltc_ledger',
                report_uuid='ltc_ledger',
                visible_name='LTC Blockchain',
                version=StatsLedgerVersion(
                    nr='3', timestamp='1970-01-01 00:00:42'),
                )]
            )])


async def get_statistics(test_case):
    result = await service.get_statistics()
    result.currencies = sorted(result.currencies, key=lambda c: c.name)
    assertEqual(stats.currencies, result.currencies)


async def search(test_case):
    def base_search_results():
        return SearchResult(
                currencies=[
                    SearchResultByCurrency(
                        currency='btc',
                        addresses=[],
                        txs=[]),
                    SearchResultByCurrency(
                        currency='ltc',
                        addresses=[],
                        txs=[]),
                    SearchResultByCurrency(
                        currency='eth',
                        addresses=[],
                        txs=[])],
                labels=[])

    expected = base_search_results()
    expected.currencies[0] = \
        SearchResultByCurrency(
            currency='btc',
            addresses=['xyz1234', 'xyz1278'],
            txs=[])

    result = await service.search(q='xyz12')
    test_case.assertEqual(expected, result)

    expected.currencies[0] = \
        SearchResultByCurrency(
            currency='btc',
            addresses=['xyz1278'],
            txs=[])

    result = await service.search(q='xyz127')
    test_case.assertEqual(expected, result)

    expected.currencies[0] = \
        SearchResultByCurrency(
            currency='btc',
            txs=['ab1880', 'ab188013'],
            addresses=[])

    result = await service.search(q='ab188')
    test_case.assertEqual(expected, result)

    expected.currencies[0] = \
        SearchResultByCurrency(
            currency='btc',
            txs=['ab188013'],
            addresses=[])

    result = await service.search(q='ab18801')
    test_case.assertEqual(expected, result)

    expected.currencies[0] = \
        SearchResultByCurrency(
            currency='btc',
            txs=['00ab188013'],
            addresses=[])

    result = await service.search(q='00ab1')
    test_case.assertEqual(expected, result)

    expected = base_search_results()
    expected.labels = ['isolinks']

    result = await service.search(q='iso')
    test_case.assertEqual(expected, result)

    expected = base_search_results()
    expected.currencies[2] = \
        SearchResultByCurrency(
            currency='eth',
            txs=['af6e0000', 'af6e0003'],
            addresses=[])

    result = await service.search(q='af6e')
    test_case.assertEqual(expected, result)

    expected = base_search_results()
    expected.currencies[2] = \
        SearchResultByCurrency(
            currency='eth',
            txs=[],
            addresses=['0xabcdef'])

    result = await service.search(q='0xabcde')
    test_case.assertEqual(expected, result)
