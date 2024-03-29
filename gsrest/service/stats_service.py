from openapi_server.models.currency_stats import CurrencyStats
from gsrest.db.util import tagstores


async def get_currency_statistics(request, currency):
    db = request.app['db']
    result = await db.get_currency_statistics(currency)
    if result is None:
        raise SystemError(
            'statistics for currency {} not found'.format(currency))
    counts = await tagstores(
        request.app['tagstores'], lambda row: row, 'count', currency,
        request.app['request_config']['show_private_tags'])
    no_labels = 0
    no_tagged_addresses = 0
    for c in counts:
        no_labels += c['no_labels']
        no_tagged_addresses += c['no_tagged_addresses']
    return CurrencyStats(name=currency,
                         no_blocks=result['no_blocks'],
                         no_address_relations=result['no_address_relations'],
                         no_addresses=result['no_addresses'],
                         no_entities=result['no_clusters'],
                         no_txs=result['no_transactions'],
                         no_labels=int(no_labels),
                         no_tagged_addresses=int(no_tagged_addresses),
                         timestamp=result['timestamp'])


async def get_no_blocks(request, currency):
    db = request.app['db']
    result = await db.get_currency_statistics(currency)
    if result is None:
        raise SystemError(
            'statistics for currency {} not found'.format(currency))
    return result['no_blocks']
