from openapi_server.models.currency_stats import CurrencyStats


async def get_currency_statistics(request, currency, version=None):
    db = request.app['db']
    result = await db.get_currency_statistics(currency)
    if result is None:
        raise ValueError('statistics for currency {} not found'
                         .format(currency))
    return CurrencyStats(
            name=currency,
            no_blocks=result['no_blocks'],
            no_address_relations=result['no_address_relations'],
            no_addresses=result['no_addresses'],
            no_entities=result['no_clusters'],
            no_txs=result['no_transactions'],
            no_labels=0,
            timestamp=result['timestamp']
        )
