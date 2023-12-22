from openapi_server.models.stats import Stats
from openapi_server.models.search_result import SearchResult
from openapi_server.models.search_result_by_currency \
    import SearchResultByCurrency
from openapi_server.models.currency_stats import CurrencyStats

stats = Stats(currencies=[
    CurrencyStats(name='btc',
                  no_entities=7890,
                  no_addresses=4560,
                  no_blocks=3,
                  timestamp=420,
                  no_txs=110,
                  no_labels=13,
                  no_tagged_addresses=79,
                  no_address_relations=1230),
    CurrencyStats(name='eth',
                  no_entities=0,
                  no_addresses=1,
                  no_blocks=3,
                  timestamp=16,
                  no_txs=10,
                  no_labels=4,
                  no_tagged_addresses=90,
                  no_address_relations=2),
    CurrencyStats(name='ltc',
                  no_entities=789,
                  no_addresses=456,
                  no_blocks=3,
                  timestamp=42,
                  no_txs=11,
                  no_labels=2,
                  no_tagged_addresses=20,
                  no_address_relations=123)
])


async def get_statistics(test_case):
    result = await test_case.request('/stats')
    result['currencies'] = \
        sorted(result['currencies'], key=lambda c: c['name'])
    cs = [c.to_dict() for c in stats.currencies]
    test_case.assertEqual(cs, result['currencies'])

    result = await test_case.request('/stats', auth='unauthenticated')
    result['currencies'] = \
        sorted(result['currencies'], key=lambda c: c['name'])

    test_case.assertEqual(cs, result['currencies'])


async def search(test_case):

    def base_search_results():
        return SearchResult(currencies=[
            SearchResultByCurrency(currency='btc', addresses=[], txs=[]),
            SearchResultByCurrency(currency='ltc', addresses=[], txs=[]),
            SearchResultByCurrency(currency='eth', addresses=[], txs=[])
        ],
            labels=[],
            actors=[])

    expected = base_search_results()
    expected.currencies[0] = \
        SearchResultByCurrency(
            currency='btc',
            addresses=['xyz120new', 'xyz1234', 'xyz1278'],
            txs=[])

    path = '/search?q={q}'
    result = await test_case.request(path, q='xyz12')
    test_case.assertEqual(expected.to_dict(), result)

    expected.currencies[0] = \
        SearchResultByCurrency(
            currency='btc',
            addresses=['xyz1278'],
            txs=[])

    result = await test_case.request(path, q='xyz127')
    test_case.assertEqual(expected.to_dict(), result)

    expected.currencies[0] = \
        SearchResultByCurrency(
            currency='btc',
            txs=['ab1880'.rjust(64, "0"), 'ab188013'.rjust(64, "0")],
            addresses=[])

    result = await test_case.request(path, q='ab188')
    test_case.assertEqual(expected.to_dict(), result)

    expected.currencies[0] = \
        SearchResultByCurrency(
            currency='btc',
            txs=['ab188013'.rjust(64, "0")],
            addresses=[])

    result = await test_case.request(path, q='ab18801')
    test_case.assertEqual(expected.to_dict(), result)

    expected.currencies[0] = \
        SearchResultByCurrency(
            currency='btc',
            txs=['00ab188013'.rjust(64, "0")],
            addresses=[])

    result = await test_case.request(path, q='00ab1')
    test_case.assertEqual(expected.to_dict(), result)

    expected = base_search_results()
    expected.labels = sorted(['Internet Archive 2', 'Internet, Archive'])

    result = await test_case.request(path, q='internet')
    result['labels'] = sorted(result['labels'])
    test_case.assertEqual(expected.to_dict(), result)

    result = await test_case.request(path, auth='y', q='internet')
    expected.labels = ['Internet, Archive']
    test_case.assertEqual(expected.to_dict(), result)

    expected = base_search_results()
    expected.actors = [{
        'id': 'actorX',
        'label': 'Actor X'
    }, {
        'id': 'actorY',
        'label': 'Actor Y'
    }, {
        'id': 'anotherActor',
        'label': 'Another Actor Y'
    }]

    result = await test_case.request(path, q='actor')
    result['labels'] = sorted(result['labels'])
    test_case.assertEqual(expected.to_dict(), result)

    result = await test_case.request(path, auth='y', q='actor')
    expected.actors = [{'id': 'actorX', 'label': 'Actor X'}]
    test_case.assertEqual(expected.to_dict(), result)

    expected = base_search_results()
    expected.currencies[2] = \
        SearchResultByCurrency(
            currency='eth',
            txs=['af6e0000'.rjust(64, "0"), 'af6e0003'.rjust(64, "0")],
            addresses=[])

    result = await test_case.request(path, q='af6e')
    test_case.assertEqual(expected.to_dict(), result)

    expected = base_search_results()
    expected.currencies[2] = \
        SearchResultByCurrency(
            currency='eth',
            txs=[],
            addresses=['0xabcdef'])

    result = await test_case.request(path, q='0xabcde')
    test_case.assertEqual(expected.to_dict(), result)
