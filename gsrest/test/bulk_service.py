from gsrest.test.blocks_service import block, block2

error_bodies = [{'x': 'x'}, {}]
block_path = '/{currency}/bulk.{form}/get_block?num_pages=1'
headers = {
    'Accept': 'application/json',
    'Authorization': 'x'
}


async def bulk_csv(test_case):
    body = {'height': [1, 2]}
    response = await test_case.client.request(
        path=block_path.format(form="csv", currency="btc"),
        method='POST',
        json=body,
        headers=headers)
    result = (await response.read()).decode('utf-8')
    expected = ('_request_height,block_hash,height,no_txs,timestamp\r\n'
        '1,00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048,1,1,1231469665\r\n' # noqa
        '2,000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd,2,1,1231469744\r\n') # noqa
    test_case.assertEqual(sorted(expected.split('\r\n')),
                          sorted(result.split('\r\n')))

    # get_address

    path = '/{currency}/bulk.{form}/get_address?num_pages=1'
    body = {'address': ['a123456', '2']}
    response = await test_case.client.request(
        path=path.format(form="csv", currency="btc"),
        method='POST',
        json=body,
        headers=headers)
    result = (await response.read()).decode('utf-8')
    expected = ('_request_address,address,balance_eur,balance_usd,balance_value,entity,first_tx_height,first_tx_timestamp,first_tx_tx_hash,in_degree,last_tx_height,last_tx_timestamp,last_tx_tx_hash,no_incoming_txs,no_outgoing_txs,out_degree,tags,total_received_eur,total_received_usd,total_received_value,total_spent_eur,total_spent_usd,total_spent_value,_error\r\n' # noqa
                '2,,,,,,,,,,,,,,,,,,,,,,,Not found\r\n'
                'a123456,a123456,1.15,2.31,115422577,123,1,1361497172,04d92601677d62a985310b61a301e74870fa942c8be0648e16b1db23b996a8cd,5013,1,1361497172,bd01b57a50bdee0fb34ce77f5c62a664cea5b94b304d438a8225850f05b45ae5,3981,267,284,,2130676.5,2543214.5,40412296129,2118309.0,2541183.0,40296873552,\r\n') # noqa
    test_case.assertEqual(sorted(expected.split('\r\n')),
                          sorted(result.split('\r\n')))

    # no data
    body = {'height': [100, 200]}
    response = await test_case.client.request(
        path=block_path.format(form="csv", currency="btc"),
        method='POST',
        json=body,
        headers=headers)
    result = (await response.read()).decode('utf-8')
    expected = ('_error,_request_height\r\n'
        'Not found,100\r\n' # noqa
        'Not found,200\r\n') # noqa

    test_case.assertEqual(sorted(expected.split('\r\n')),
                          sorted(result.split('\r\n')))
    # error bodies:
    for body in error_bodies:
        response = await test_case.client.request(
            path=block_path.format(form="csv", currency="btc"),
            method='POST',
            json=body,
            headers=headers)
        content = (await response.read()).decode('utf-8')
        test_case.assertEqual(400, response.status, "response is " + content)


async def bulk_json(test_case):
    body = {'height': [1, 2]}
    result = await test_case.requestWithCodeAndBody(
                        block_path.format(form="json", currency="btc"),
                        200, body,
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
