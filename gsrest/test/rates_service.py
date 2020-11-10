from openapi_server.models.rates import Rates
from openapi_server.models.rates_rates import RatesRates
from gsrest.test.assertion import assertEqual
import gsrest.service.rates_service as service

rate = Rates(
   height=1,
   rates=RatesRates(eur=0.0, usd=0.0)
)


def get_exchange_rates(test_case):
    result = service.get_exchange_rates(currency='btc', height=1)
    assertEqual(rate, result)
