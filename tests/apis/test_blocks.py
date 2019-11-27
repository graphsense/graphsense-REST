import gsrest.service.blocks_service
from gsrest.model.blocks import Block, BlockTxs, BlockTxSummary
from gsrest.util.checks import crypto_in_config

non_existing_block = 999999
non_existing_currency = 'abc'
existing_block1 = 302602
existing_block2 = 531141

TEST_BLOCKS = {
    existing_block1: Block(existing_block1, "00000000000000000a4d72c6f0c714e8b0f4e847a9599110acc133cec97900d4", 101, 1401047125).to_dict(),
    existing_block2: Block(existing_block2, "0000000000000000000fc3ab40914d4e72ff42d7f9730647cee43d2178607a31", 1342, 1531116874).to_dict(),
}


TEST_BLOCK_TXS = {
    0: BlockTxs(0, [BlockTxSummary('4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b', 0, 1, {'value': 0, 'eur': 0, 'usd': 0}, {'value': 5000000000, 'eur': 25, 'usd': 25}).to_dict()]).to_dict()
}


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
    response = client.get('/btc/blocks/{}'.format(existing_block1))
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == len(TEST_BLOCKS[existing_block1])
    for k in TEST_BLOCKS[existing_block1]:
        assert json_data[k] == TEST_BLOCKS[existing_block1][k]

    # request non-existing block
    response = client.get('/btc/blocks/{}'.format(non_existing_block))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Block {} not found in currency btc.'.format(non_existing_block) \
           in json_data['message']

    # request block of non-existing currency
    response = client.get('/{}/blocks/{}'.format(
        non_existing_currency, TEST_BLOCKS[existing_block1]['height']))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Unknown currency in config: {}'.format(non_existing_currency) in \
           json_data['message']


def test_block_list(client, auth, monkeypatch):

    # define a monkeypatch method without paging
    def mock_list_blocks(*args, **kwargs):
        if crypto_in_config(args[0]):
            return None, [block for block in TEST_BLOCKS.values()]
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for blocks_service.get_block
    monkeypatch.setattr(gsrest.service.blocks_service, "list_blocks",
                        mock_list_blocks)
    
    auth.login()

    # request list of blocks
    response = client.get('/btc/blocks/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data['blocks']) == 2
    assert json_data['next_page'] is None

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
                    [block for block in TEST_BLOCKS.values()])
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for blocks_service.list_blocks
    monkeypatch.setattr(gsrest.service.blocks_service, "list_blocks",
                        mock_list_blocks_paging)

    # request list of blocks
    response = client.get('/btc/blocks/')
    assert response.status_code == 200
    json_data = response.get_json()

    assert json_data['next_page'] == bytes('example token', 'utf-8').hex()


def test_block_txs_list(client, auth, monkeypatch):
    # define a monkeypatch method without paging
    def mock_list_block_txs(*args, **kwargs):
        if crypto_in_config(args[0]):
            return TEST_BLOCK_TXS[args[1]]
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for blocks_service.list_block_txs
    monkeypatch.setattr(gsrest.service.blocks_service, "list_block_txs",
                        mock_list_block_txs)

    auth.login()

    # request list of block transactions
    block_height_test = 0
    response = client.get('/btc/blocks/{}/txs'.format(block_height_test))
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['height'] == TEST_BLOCK_TXS[block_height_test]['height']
    assert json_data['txs'] == TEST_BLOCK_TXS[block_height_test]['txs']
