import gsrest.service.blocks_service
from gsrest.model.blocks import Block

TEST_BLOCKS = {
    1: Block(1, "1sdf2", 2, 3),
    2: Block(2, "4adb43", 4, 5)
}


def test_block_by_height(client, auth, monkeypatch):

    # define a monkeypatch method
    def mock_get_block(*args, **kwargs):
        return TEST_BLOCKS.get(args[1])

    # apply the monkeypatch method for blocks_service.get_block
    monkeypatch.setattr(gsrest.service.blocks_service, "get_block",
                        mock_get_block)

    auth.login()

    # request existing block
    response = client.get('/btc/blocks/1')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['blockHash'] == TEST_BLOCKS.get(1).blockHash
    assert json_data['height'] == TEST_BLOCKS.get(1).height
    assert json_data['noTransactions'] == TEST_BLOCKS.get(1).noTransactions
    assert json_data['timestamp'] == TEST_BLOCKS.get(1).timestamp

    # request non-existing block
    response = client.get('/btc/blocks/3')
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Block height 3 not found in currency btc.' in json_data['message']

    # request block of non-existing currency
    response = client.get('/abc/blocks/3')
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Block height 3 not found in currency abc.' in json_data['message']


def test_block_list(client, auth, monkeypatch):

    # define a monkeypatch method without paging
    def mock_list_blocks(*args, **kwargs):
        return (None, [block.__dict__ for block in TEST_BLOCKS.values()])

    # apply the monkeypatch method for blocks_service.get_block
    monkeypatch.setattr(gsrest.service.blocks_service, "list_blocks",
                        mock_list_blocks)

    auth.login()

    # request list of blocks
    response = client.get('/btc/blocks/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data['blocks']) == 2
    assert json_data['nextPage'] is None

    # define a monkeypatch method with paging
    def mock_list_blocks_paging(*args, **kwargs):
        return (bytes('example token', 'utf-8'),
                [block.__dict__ for block in TEST_BLOCKS.values()])

    # apply the monkeypatch method for blocks_service.get_block
    monkeypatch.setattr(gsrest.service.blocks_service, "list_blocks",
                        mock_list_blocks_paging)

    # request list of blocks
    response = client.get('/btc/blocks/')
    assert response.status_code == 200
    json_data = response.get_json()

    assert json_data['nextPage'] == bytes('example token', 'utf-8').hex()
