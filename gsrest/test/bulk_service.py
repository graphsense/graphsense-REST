from gsrest.test.blocks_service import block, block2

error_bodies = [{'x': 'x'}, {}]
path = '/{currency}/bulk.{form}/get_block?num_pages=1'
headers = {
    'Accept': 'application/json',
    'Authorization': 'x'
}


async def bulk_csv(test_case):
    body = {'height': [1, 2]}
    response = await test_case.client.request(
        path=path.format(form="csv", currency="btc"),
        method='POST',
        json=body,
        headers=headers)
    result = (await response.read()).decode('utf-8')
    expected = ('_request_height,block_hash,height,no_txs,timestamp\r\n'
        '1,00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048,1,1,1231469665\r\n' # noqa
        '2,000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd,2,1,1231469744\r\n') # noqa
    test_case.assertEqual(sorted(expected.split('\r\n')),
                          sorted(result.split('\r\n')))

    # no data
    body = {'height': [100, 200]}
    response = await test_case.client.request(
        path=path.format(form="csv", currency="btc"),
        method='POST',
        json=body,
        headers=headers)
    result = (await response.read()).decode('utf-8')
    expected = ('_request_height,_info\r\n'
        '100,no data\r\n' # noqa
        '200,no data\r\n') # noqa

    test_case.assertEqual(sorted(expected.split('\r\n')),
                          sorted(result.split('\r\n')))
    # error bodies:
    for body in error_bodies:
        response = await test_case.client.request(
            path=path.format(form="csv", currency="btc"),
            method='POST',
            json=body,
            headers=headers)
        content = (await response.read()).decode('utf-8')
        test_case.assertEqual(400, response.status, "response is " + content)


async def bulk_json(test_case):
    body = {'height': [1, 2]}
    result = await test_case.requestWithCodeAndBody(
                        path.format(form="json", currency="btc"), 200, body,
                        currency="btc",
                        form='json')

    def s(b):
        return b['block_hash']

    result = sorted(result, key=s)
    expected = [block.to_dict(), block2.to_dict()]
    for b in expected:
        b['_request_height'] = b['height']
    blocks = sorted(expected, key=s)
    test_case.assertEqual(blocks, result)
