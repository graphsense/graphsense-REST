from gsrest.db import get_connection
from openapi_server.models.rates import Rates
from openapi_server.models.rates_rates import RatesRates
from gsrest.service.stats_service import get_currency_statistics


RATES_TABLE = 'exchange_rates'


def get_exchange_rates(currency, height):
    rates = get_rates(currency, height)
    return Rates(height=height,
                 rates=RatesRates(
                    eur=rates['rates']['eur'],
                    usd=rates['rates']['usd']))


def get_rates(currency, height=None):
    if height is None:
        height = get_currency_statistics(currency).no_blocks - 1

    db = get_connection()
    r = db.get_rates(currency, height)

    if r is None:
        raise ValueError("Cannot find height {} in currency {}"
                         .format(height, currency))
    return {'height': r['height'],
            'rates': {k: v for k, v in r.items() if k != 'height'}}


def list_rates(currency, heights):
    db = get_connection()
    rates = db.list_rates(currency, heights)
    print(f'raw rates {rates}')

    height_rates = dict()  # key: height, value: {'eur': 0, 'usd':0}
    for rate in rates:
        height_rates[rate['height']] = {k: v for k, v in rate.items()
                                        if k != 'height'}
    return height_rates
