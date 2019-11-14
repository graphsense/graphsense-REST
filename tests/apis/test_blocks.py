import gsrest.service.blocks_service
from gsrest.model.blocks import Block
from gsrest.util.checks import crypto_in_config

TEST_BLOCKS = {
    302602: Block(302602, "00000000000000000a4d72c6f0c714e8b0f4e847a9599110acc133cec97900d4", 101, 1401047125),
    531141: Block(531141, "0000000000000000000fc3ab40914d4e72ff42d7f9730647cee43d2178607a31", 1342, 1531116874),
}

non_existing_block = '999999'
non_existing_currency = 'abc'


def test_block_by_height(client, auth, monkeypatch):

    # define a monkeypatch method
    def mock_get_block(*args, **kwargs):
        if crypto_in_config(args[0]):
            return TEST_BLOCKS.get(args[1])
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for blocks_service.get_block
    monkeypatch.setattr(gsrest.service.blocks_service, "get_block",
                        mock_get_block)

    auth.login()

    # request existing block
    response = client.get('/btc/blocks/302602')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['blockHash'] == TEST_BLOCKS.get(302602).blockHash
    assert json_data['height'] == TEST_BLOCKS.get(302602).height
    assert json_data['noTxs'] == TEST_BLOCKS.get(302602).noTxs
    assert json_data['timestamp'] == TEST_BLOCKS.get(302602).timestamp

    # request non-existing block
    response = client.get('/btc/blocks/{}'.format(non_existing_block))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Block {} not found in currency btc.'.format(non_existing_block) \
           in json_data['message']

    # request block of non-existing currency
    response = client.get('/{}/blocks/{}'.format(
        non_existing_currency, TEST_BLOCKS.get(302602).height))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Unknown currency in config: {}'.format(non_existing_currency) in \
           json_data['message']


def test_block_list(client, auth, monkeypatch):

    # define a monkeypatch method without paging
    def mock_list_blocks(*args, **kwargs):
        if crypto_in_config(args[0]):
            return None, [block.__dict__ for block in TEST_BLOCKS.values()]
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for blocks_service.get_block
    monkeypatch.setattr(gsrest.service.blocks_service, "list_blocks",
                        mock_list_blocks)
    
    auth.login()

    # request list of blocks
    response = client.get('/btc/blocks/')
    assert response.status_code == 200
    json_data = response.get_json()
    # assert len(json_data['blocks']) == 100
    # assert json_data['nextPage'] is not None
    assert len(json_data['blocks']) == 2
    assert json_data['nextPage'] is None

    # request list of non-existing-currency blocks
    response = client.get('/{}/blocks/'.format(non_existing_currency))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Unknown currency in config: {}'.format(non_existing_currency) in \
           json_data['message']

    # define a monkeypatch method with paging
    def mock_list_blocks_paging(*args, **kwargs):
        if crypto_in_config(args[0]):
            return (bytes('example token', 'utf-8'),
                    [block.__dict__ for block in TEST_BLOCKS.values()])
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for blocks_service.list_blocks
    monkeypatch.setattr(gsrest.service.blocks_service, "list_blocks",
                        mock_list_blocks_paging)

    # request list of blocks
    response = client.get('/btc/blocks/')
    assert response.status_code == 200
    json_data = response.get_json()

    # assert json_data['nextPage'] is not None
    assert json_data['nextPage'] == bytes('example token', 'utf-8').hex()
