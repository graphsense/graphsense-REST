from cassandra.query import dict_factory
from cassandra.concurrent import execute_concurrent

from gsrest.db.cassandra import get_session
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
    """ Returns the exchange rate for a given block height """

    if height is None:
        height = get_currency_statistics(currency).no_blocks - 1

    session = get_session(currency, 'transformed')
    session.row_factory = dict_factory
    query = "SELECT * FROM exchange_rates WHERE height = %s"
    result = session.execute(query, [height])
    if result.current_rows:
        r = result.current_rows[0]
        return {'height': r['height'],
                'rates': {k: v for k, v in r.items() if k != 'height'}}
    raise ValueError("Cannot find height {} in currency {}"
                     .format(height, currency))


def list_rates(currency, heights=-1):
    """ Returns the exchange rates for a list of block heights """
    session = get_session(currency, 'transformed')
    session.row_factory = dict_factory

    if heights == -1:
        heights = [get_currency_statistics(currency).no_blocks - 1]

    concurrent_query = "SELECT * FROM exchange_rates WHERE height = %s"
    statements_and_params = []
    for h in heights:
        statements_and_params.append((concurrent_query, [h]))
    rates = execute_concurrent(session, statements_and_params,
                               raise_on_first_error=False)
    height_rates = dict()  # key: height, value: {'eur': 0, 'usd':0}
    for (success, rate) in rates:
        if not success:
            pass
        else:
            d = rate.one()
            height_rates[d['height']] = {k: v for k, v in d.items()
                                         if k != 'height'}
    return height_rates
