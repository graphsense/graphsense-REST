from tagstore.db import TagstoreDbAsync

from openapi_server.models.currency_stats import CurrencyStats


async def get_currency_statistics(request, currency):
    db = request.app["db"]

    tsdb = TagstoreDbAsync(request.app["gs-tagstore"])

    tag_stats = await tsdb.get_network_statistics_cached()

    result = await db.get_currency_statistics(currency)
    if result is None:
        raise SystemError("statistics for currency {} not found".format(currency))

    network_stats = tag_stats.by_network[currency.upper()]
    no_labels = network_stats.nr_labels
    no_tagged_addresses = network_stats.nr_identifiers_implicit

    return CurrencyStats(
        name=currency,
        no_blocks=result["no_blocks"],
        no_address_relations=result["no_address_relations"],
        no_addresses=result["no_addresses"],
        no_entities=result["no_clusters"],
        no_txs=result["no_transactions"],
        no_labels=int(no_labels),
        no_tagged_addresses=int(no_tagged_addresses),
        timestamp=result["timestamp"],
    )


async def get_no_blocks(request, currency):
    db = request.app["db"]
    result = await db.get_currency_statistics(currency)
    if result is None:
        raise SystemError("statistics for currency {} not found".format(currency))
    return result["no_blocks"]
