from openapi_server.models.rates import Rates
import gsrest.service.rates_service as service

rate = Rates(
   height=1,
   rates=[{'code': 'eur', 'value': 0.0}, {'code': 'usd', 'value': 0.0}]
)


def get_exchange_rates(test_case):
    result = service.get_exchange_rates(currency='btc', height=1)
    test_case.assertEqual(rate, result)
