

def test_blocks(client, auth):
    auth.login()
    response = client.get('/btc/blocks/')
    assert response.status_code == 200
    assert b'NOT YET IMPLEMENTED' in response.data


def test_block_by_height(client, auth):
    auth.login()
    response = client.get('/btc/blocks/1')
    assert response.status_code == 200
    assert b'Requested currency' in response.data


def test_block_txs_by_height(client, auth):
    auth.login()
    response = client.get('/btc/blocks/1/transactions')
    assert response.status_code == 200
    assert b'NOT YET IMPLEMENTED' in response.data
