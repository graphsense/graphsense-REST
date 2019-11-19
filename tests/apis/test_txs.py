import gsrest.service.txs_service
from gsrest.model.txs import Tx
from collections import namedtuple
from gsrest.util.checks import crypto_in_config

tx1 = 'ab188013f626405ddebf1a7b2e0af34253d09e80f9ef7f981ec1ec59d6200c1f'
in1_d = {"address": ["1H8omroLCN2578Mj6sDrWa8YueqWEckNKY"], "value": 10000000}
out1_d = {"address": ["138cWsiAGpW9yqfjMVCCsFcnaiSHyoWMnJ"], "value": 1}
out2_d = {"address": ["1CRqaDkksF1zp6wLunY7ygSafXsiftH9FN"], "value": 9949999}
input1 = namedtuple('input1', in1_d.keys())(*in1_d.values())
output1 = namedtuple('output1', out1_d.keys())(*out1_d.values())
output2 = namedtuple('output2', out2_d.keys())(*out2_d.values())

TEST_TXS = {
    tx1: Tx(bytearray.fromhex(tx1),
            False,
            245426,
            [input1],
            [output1, output2],
            1373266967,
            10000000,
            9950000)
}

non_existing_tx = '999999'
non_existing_currency = 'abc'


def test_tx(client, auth, monkeypatch):

    # define a monkeypatch method
    def mock_get_tx(*args, **kwargs):
        if crypto_in_config(args[0]):
            return TEST_TXS.get(args[1])
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for txs_service.get_tx
    monkeypatch.setattr(gsrest.service.txs_service, "get_tx", mock_get_tx)

    auth.login()

    # request existing tx
    response = client.get('btc/txs/' + tx1)
    assert response.status_code == 200
    json_data = response.get_json()

    assert json_data['txHash'] == TEST_TXS.get(tx1).txHash
    assert json_data['coinbase'] == TEST_TXS.get(tx1).coinbase
    assert json_data['height'] == TEST_TXS.get(tx1).height
    assert json_data['inputs'] == TEST_TXS.get(tx1).inputs
    assert json_data['outputs'] == TEST_TXS.get(tx1).outputs
    assert json_data['timestamp'] == TEST_TXS.get(tx1).timestamp
    assert json_data['totalInput'] == TEST_TXS.get(tx1).totalInput
    assert json_data['totalOutput'] == TEST_TXS.get(tx1).totalOutput

    # request non-existing tx
    response = client.get('/btc/txs/{}'.format(non_existing_tx))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Transaction {} not found in currency btc'.format(non_existing_tx) \
           in json_data['message']

    # request tx of non-existing currency
    response = client.get('/{}/txs/{}'.format(non_existing_currency,
                                              TEST_TXS.get(tx1).txHash))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Unknown currency in config: {}'.format(non_existing_currency) in \
           json_data['message']


def test_tx_list(client, auth, monkeypatch):

    # define a monkeypatch method without paging
    def mock_list_txs(*args, **kwargs):
        if crypto_in_config(args[0]):
            return None, [tx.__dict__ for tx in TEST_TXS.values()]
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for txs_service.get_tx
    monkeypatch.setattr(gsrest.service.txs_service, "list_txs", mock_list_txs)

    auth.login()

    # request list of txs
    response = client.get('/btc/txs/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data['txs']) == 1
    assert json_data['nextPage'] is None

    # request list of non-existing-currency txs
    response = client.get('/{}/txs/'.format(non_existing_currency))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Unknown currency in config: {}'.format(non_existing_currency) in \
           json_data['message']

    # define a monkeypatch method with paging
    def mock_list_txs_paging(*args, **kwargs):
        if crypto_in_config(args[0]):
            return (bytes('example token', 'utf-8'),
                    [tx.__dict__ for tx in TEST_TXS.values()])
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for txs_service.list_txs
    monkeypatch.setattr(gsrest.service.txs_service, "list_txs",
                        mock_list_txs_paging)

    # request list of txs
    response = client.get('/btc/txs/')
    assert response.status_code == 200
    json_data = response.get_json()

    assert json_data['nextPage'] == bytes('example token', 'utf-8').hex()
