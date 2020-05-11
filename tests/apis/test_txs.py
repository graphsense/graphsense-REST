from collections import namedtuple

from gsrest.model.txs import Tx
import gsrest.service.txs_service
from gsrest.util.checks import check_inputs

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
            9950000,
            {'eur': 0.5, 'usd': 0.5}).to_dict()
}

non_existing_tx = '999999'
non_existing_currency = 'abc'


def test_tx(client, auth, monkeypatch):

    # define a monkeypatch method
    def mock_get_tx(*args, **kwargs):
        check_inputs(currency=args[0])  # abort if fails
        return TEST_TXS.get(args[1])

    # apply the monkeypatch method for txs_service.get_tx
    monkeypatch.setattr(gsrest.service.txs_service, "get_tx", mock_get_tx)

    auth.login()

    # request existing tx
    response = client.get('btc/txs/{}'.format(tx1))
    assert response.status_code == 200
    json_data = response.get_json()
    for k in TEST_TXS[tx1]:
        assert json_data[k] == TEST_TXS[tx1][k]

    # request tx of non-existing currency
    response = client.get('/{}/txs/{}'.format(non_existing_currency,
                                              TEST_TXS[tx1]['tx_hash']))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Unknown currency in config: {}'.format(non_existing_currency) in \
           json_data['message']


def test_tx_list(client, auth, monkeypatch):

    # define a monkeypatch method without paging
    def mock_list_txs(*args, **kwargs):
        check_inputs(currency=args[0])  # abort if fails
        return None, [tx for tx in TEST_TXS.values()]

    # apply the monkeypatch method for txs_service.get_tx
    monkeypatch.setattr(gsrest.service.txs_service, "list_txs", mock_list_txs)

    auth.login()

    # request list of txs
    response = client.get('/btc/txs/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data['txs']) == 1
    assert json_data['next_page'] is None

    # request list of non-existing-currency txs
    response = client.get('/{}/txs/'.format(non_existing_currency))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Unknown currency in config: {}'.format(non_existing_currency) in \
           json_data['message']

    # define a monkeypatch method with paging
    def mock_list_txs_paging(*args, **kwargs):
        check_inputs(currency=args[0])  # abort if fails
        return bytes('example token', 'utf-8'), \
            [tx for tx in TEST_TXS.values()]

    # apply the monkeypatch method for txs_service.list_txs
    monkeypatch.setattr(gsrest.service.txs_service, "list_txs",
                        mock_list_txs_paging)

    # request list of txs
    response = client.get('/btc/txs/')
    assert response.status_code == 200
    json_data = response.get_json()

    assert json_data['next_page'] == bytes('example token', 'utf-8').hex()
