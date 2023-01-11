from openapi_server.models.rates import Rates

rate = Rates(height=1,
             rates=[{
                 'code': 'eur',
                 'value': 0.0
             }, {
                 'code': 'usd',
                 'value': 0.0
             }])


async def get_exchange_rates(test_case):
    result = await test_case.request('/btc/rates/1')
    test_case.assertEqual(rate.to_dict(), result)
