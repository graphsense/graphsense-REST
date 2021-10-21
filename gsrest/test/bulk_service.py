import gsrest.service.bulk_service as service
from gsrest.test.blocks_service import block, block2
import json


async def bulk(test_case):
    body = {'height': [1, 2]}
    result = await service.bulk("btc", "blocks", "get_block", body=body)
    result = result.data.decode('utf-8')
    expected = ('block_hash,height,no_txs,timestamp\r\n'
        '00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048,1,1,1231469665\r\n' # noqa
        '000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd,2,1,1231469744\r\n') # noqa
    test_case.assertEqual(sorted(expected.split('\r\n')),
                          sorted(result.split('\r\n')))

    result = await service.bulk("btc", "blocks", "get_block", body=body,
                                form='json')

    def s(b):
        return b['block_hash']

    result = sorted(json.loads(result.data.decode('utf-8')), key=s)
    blocks = sorted([block.to_dict(), block2.to_dict()], key=s)
    test_case.assertEqual(blocks, result)
