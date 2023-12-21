from openapi_server.models.rates import Rates
from gsrest.service.stats_service import get_no_blocks
from gsrest.util.values import map_rates_for_peged_tokens
from gsrest.errors import BlockNotFoundException

RATES_TABLE = 'exchange_rates'


async def get_exchange_rates(request, currency, height):
    rates = await get_rates(request, currency, height)
    return Rates(height=height, rates=rates['rates'])


async def get_rates(request, currency, height=None):
    if height is None:
        height = (await get_no_blocks(request, currency)) - 1

    db = request.app['db']
    if ":" in currency:
        network, currency, *rest = currency.split(":")
    else:
        network, currency = (currency, currency)

    token_config = db.get_token_configuration(network)
    if token_config is not None and currency.upper() in token_config:
        # create pseudo rates for eth stable coin tokens.
        r = await db.get_rates(network, height)
        # this avoids changing original rates if cached
        # otherwise results are wrong.
        r = r.copy()
        r["rates"] = map_rates_for_peged_tokens(r['rates'],
                                                token_config[currency.upper()])
    else:
        r = await db.get_rates(currency, height)

    if r is None:
        raise BlockNotFoundException(currency, height)
    return r


async def list_rates(request, currency, heights):
    db = request.app['db']
    rates = await db.list_rates(currency, heights)

    height_rates = dict()  # key: height, value: {'eur': 0, 'usd':0}
    for rate in rates:
        height_rates[rate['block_id']] = rate['rates']
    return height_rates
