import gsrest.service.batch_service as service
from tests.util.util import yamldump
from openapi_server.models.get_tx import GetTx
from openapi_server.models.get_tx_parameters import GetTxParameters
from openapi_server.models.get_tx_io import GetTxIo
from openapi_server.models.get_tx_io_parameters import GetTxIoParameters
from openapi_server.models.io import Io


async def batch(test_case):
    return
    p = GetTxIoParameters(io=Io('inputs'), tx_hash='ab1880')
    response = await service.batch(currency='btc',
                                 batch_operation=GetTxIo(parameters=[
                                    p,
                                    GetTxIoParameters(io=Io('inputs'),tx_hash='ab188013'),
                                    GetTxIoParameters(io=Io('inputs'),tx_hash='00ab188013')
                                    ]))

    print(response.data.decode('utf-8'))
    test_case.assertTrue(False)
    #test_case.assertEqual(tx1, result)
