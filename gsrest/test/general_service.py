from gsrest.test.assertion import assertEqual
import gsrest.service.general_service as service
from openapi_server.models.stats import Stats
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
            no_address_relations=1230),
        CurrencyStats(
            name='ltc',
            no_entities=789,
            no_addresses=456,
            no_blocks=3,
            timestamp=42,
            no_txs=11,
            no_labels=47,
            no_address_relations=123)])


def get_statistics(test_case):
    result = service.get_statistics()
    result.currencies = sorted(result.currencies, key=lambda c: c.name)
    assertEqual(stats, result)


def search(test_case):
    expected = SearchResult(
                    currencies=[
                        SearchResultByCurrency(
                            currency='btc',
                            addresses=['xyz1234', 'xyz1278'],
                            txs=[]),
                        SearchResultByCurrency(
                            currency='ltc',
                            addresses=[],
                            txs=[])],
                    labels=[])

    result = service.search(q='xyz12')
    result.currencies = sorted(result.currencies, key=lambda c: c.currency)
    assertEqual(expected, result)

    expected = SearchResult(
                    currencies=[
                        SearchResultByCurrency(
                            currency='btc',
                            addresses=['xyz1278'],
                            txs=[]),
                        SearchResultByCurrency(
                            currency='ltc',
                            addresses=[],
                            txs=[])],
                    labels=[])

    result = service.search(q='xyz127')
    result.currencies = sorted(result.currencies, key=lambda c: c.currency)
    assertEqual(expected, result)

    expected = SearchResult(
                    currencies=[
                        SearchResultByCurrency(
                            currency='ltc',
                            addresses=[],
                            txs=[]),
                        SearchResultByCurrency(
                            currency='btc',
                            txs=['ab1880', 'ab188013'],
                            addresses=[])],
                    labels=[])

    result = service.search(q='ab188')
    result.currencies = sorted(result.currencies, key=lambda c: c.currency)

    expected = SearchResult(
                    currencies=[
                        SearchResultByCurrency(
                            currency='ltc',
                            addresses=[],
                            txs=[]),
                        SearchResultByCurrency(
                            currency='btc',
                            txs=['ab188013'],
                            addresses=[])],
                    labels=[])

    result = service.search(q='ab18801')
    result.currencies = sorted(result.currencies, key=lambda c: c.currency)

    expected = SearchResult(
                    currencies=[
                        SearchResultByCurrency(
                            currency='ltc',
                            addresses=[],
                            txs=[]),
                        SearchResultByCurrency(
                            currency='btc',
                            txs=['00ab1880'],
                            addresses=[])],
                    labels=[])

    result = service.search(q='00ab1')
    result.currencies = sorted(result.currencies, key=lambda c: c.currency)

    expected = SearchResult(
                    currencies=[
                        SearchResultByCurrency(
                            currency='ltc',
                            addresses=[],
                            txs=[]),
                        SearchResultByCurrency(
                            currency='btc',
                            txs=[],
                            addresses=[])],
                    labels=['isolinks'])

    result = service.search(q='iso')
    result.currencies = sorted(result.currencies, key=lambda c: c.currency)
