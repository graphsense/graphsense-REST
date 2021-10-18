from gsrest.db import get_connection
from openapi_server.models.rates import Rates
from gsrest.service.stats_service import get_currency_statistics


RATES_TABLE = 'exchange_rates'


async def get_exchange_rates(currency, height):
    rates = await get_rates(currency, height)
    return Rates(height=height,
                 rates=rates['rates'])


async def get_rates(currency, height=None):
    if height is None:
        height = (await get_currency_statistics(currency)).no_blocks - 1

    db = get_connection()
    r = await db.get_rates(currency, height)

    if r is None:
        raise ValueError("Cannot find height {} in currency {}"
                         .format(height, currency))
    return r


async def list_rates(currency, heights):
    db = get_connection()
    rates = await db.list_rates(currency, heights)

    height_rates = dict()  # key: height, value: {'eur': 0, 'usd':0}
    for rate in rates:
        height_rates[rate['block_id']] = rate['rates']
    return height_rates
