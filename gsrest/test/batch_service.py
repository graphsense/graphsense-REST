import gsrest.service.batch_service as service
from tests.util.util import yamldump
from openapi_server.models.get_tx import GetTx
from openapi_server.models.get_tx_parameters import GetTxParameters


async def batch(test_case):
    response = await service.batch(currency='btc',
                                 batch_operation=GetTx(parameters=[
                                    GetTxParameters(tx_hash='ab1880'),
                                    GetTxParameters(tx_hash='ab188013'),
                                    GetTxParameters(tx_hash='00ab188013')
                                    ]))

    print(response.data.decode('utf-8'))
    test_case.assertTrue(False)
    #test_case.assertEqual(tx1, result)
