from openapi_server.models.rates import Rates
from gsrest.service.stats_service import get_no_blocks
from gsrest.util.values import map_rates_for_peged_tokens

RATES_TABLE = 'exchange_rates'


async def get_exchange_rates(request, currency, height):
    rates = await get_rates(request, currency, height)
    return Rates(height=height, rates=rates['rates'])


async def get_rates(request, currency, height=None):
    if height is None:
        height = (await get_no_blocks(request, currency)) - 1

    db = request.app['db']

    eth_token_config = db.get_token_configuration("eth")
    if currency.upper() in eth_token_config:
        # create pseudo rates for eth stable coin tokens.
        r = await db.get_rates("eth", height)
        r["rates"] = map_rates_for_peged_tokens(
            r['rates'], eth_token_config[currency.upper()])
    else:
        r = await db.get_rates(currency, height)

    if r is None:
        raise ValueError("Cannot find height {} in currency {}".format(
            height, currency))
    return r


async def list_rates(request, currency, heights):
    db = request.app['db']
    rates = await db.list_rates(currency, heights)

    height_rates = dict()  # key: height, value: {'eur': 0, 'usd':0}
    for rate in rates:
        height_rates[rate['block_id']] = rate['rates']
    return height_rates
