from gsrest import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_blocks(client):
    response = client.get('/btc/blocks')
    print(response.data)
