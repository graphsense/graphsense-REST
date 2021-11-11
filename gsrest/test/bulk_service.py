from gsrest.test.blocks_service import block, block2


async def bulk_csv(test_case):
    body = {'height': [1, 2]}
    path = '/{currency}/bulk.csv/blocks/get_block'
    headers = {
        'Accept': 'application/json',
    }
    response = await test_case.client.request(
        path=path.format(form="csv", currency="btc"),
        method='POST',
        json=body,
        headers=headers)
    result = (await response.read()).decode('utf-8')
    expected = ('block_hash,height,no_txs,timestamp\r\n'
        '00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048,1,1,1231469665\r\n' # noqa
        '000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd,2,1,1231469744\r\n') # noqa
    test_case.assertEqual(sorted(expected.split('\r\n')),
                          sorted(result.split('\r\n')))


async def bulk_json(test_case):
    body = {'height': [1, 2]}
    path = '/{currency}/bulk.json/blocks/get_block'
    result = await test_case.requestWithCodeAndBody(
                        path, 200, body,
                        currency="btc",
                        form='json')

    def s(b):
        return b['block_hash']

    result = sorted(result, key=s)
    blocks = sorted([block.to_dict(), block2.to_dict()], key=s)
    test_case.assertEqual(blocks, result)
