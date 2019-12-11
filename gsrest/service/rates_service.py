from flask import current_app
from cassandra.query import SimpleStatement, dict_factory

from gsrest.db.cassandra import (get_session, get_keyspace_mapping,
                                 get_supported_currencies)

from gsrest.model.rates import ExchangeRate


CACHED_EXCHANGE_RATES = {}


def init_app(app):
    # do not load in development mode
    if not app.config.get('DUMMY_EXCHANGE_RATES'):
        app.before_first_request(load_all_exchange_rates)


def load_all_exchange_rates():
    """ Load and cache exchange rates for all known currencies """

    currencies = get_supported_currencies()
    for currency in currencies:
        CACHED_EXCHANGE_RATES[currency] = {}
        load_exchange_rates(currency)


def load_supported_fiat_currencies(currency):
    """ Load supported fiat currencies from exchange_rates table schema """

    current_app.logger.info("Querying supported fiat currencies")

    keyspace = get_keyspace_mapping(currency, 'transformed')

    session = get_session(currency, 'transformed')
    session.row_factory = dict_factory

    query = "SELECT column_name FROM system_schema.columns \
             WHERE keyspace_name = '{}' \
             AND table_name = 'exchange_rates'".format(keyspace)

    results = session.execute(query)
    currencies = []
    for row in results:
        if row['column_name'] != 'height':
            currencies.append(row['column_name'])
    return currencies


def load_exchange_rates(currency):
    """ Load and cache exchange rates for a given currency """

    current_app.logger.info("Loading all exchange rates for {}..."
                            .format(currency))

    supported_fiat_currencies = load_supported_fiat_currencies(currency)

    session = get_session(currency, 'transformed')
    session.row_factory = dict_factory

    query = "SELECT * FROM exchange_rates"
    statement = SimpleStatement(query, fetch_size=10000)
    counter = 0
    for row in session.execute(statement):
        exchange_rates = {}
        for fiat_currency in supported_fiat_currencies:
            exchange_rates[fiat_currency] = row[fiat_currency]
        height = row['height']
        CACHED_EXCHANGE_RATES[currency][height] = ExchangeRate(height,
                                                               exchange_rates)
        counter = counter + 1

    current_app.logger.info("Finished loading {} exchange rates for {}."
                            .format(counter, currency))


def get_exchange_rate(currency, height=-1):
    """ Returns the exchange rate for a given block height """
    # TODO: handle default value (-1) as last height

    # used in development mode only
    if current_app.config.get('DUMMY_EXCHANGE_RATES'):
        return ExchangeRate(height, {'eur': 0.5, 'usd': 0.5}).to_dict()

    currency_rates = CACHED_EXCHANGE_RATES.get(currency)
    if not currency_rates:
        raise ValueError("Cannot load exchange rates. Unknown currency: {}"
                         .format(currency))

    height_rates = currency_rates.get(height)
    if not height_rates:
        raise ValueError("Cannot find height {} in currency {}"
                         .format(height, currency))

    return height_rates.to_dict()
