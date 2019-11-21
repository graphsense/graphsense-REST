import gsrest.service.addresses_service
from gsrest.model.addresses import Address
from gsrest.model.txs import TxSummary
from gsrest.model.blocks import Value
from gsrest.util.checks import crypto_in_config

non_existing_address = 'zzzzz'
non_existing_currency = 'abc'
address1 = 'bc1q2jhyw77crz3xqjml30jpw8zf66dr366kec68a9'
firstTx = TxSummary(577281, 1558549477, bytearray.fromhex('e11c9764f94f5bc8ea2b59ebe6d1e49a69a820d5b46eb9861e0f581be911071a'))
lastTx = TxSummary(585637, 1563268350, bytearray.fromhex('39435696ea53d580f15f85fcae5f084ff9c3ba6b5f1b84d4e1e41d8fceb5d0ba'))
tx1 = 'ab188013f626405ddebf1a7b2e0af34253d09e80f9ef7f981ec1ec59d6200c1f'

TEST_ADDRESSES = {
    address1: Address(address1, 514179526, firstTx, lastTx, 1, 1, Value(649456, 44.39, 49.51), Value(649456, 54.59, 61.19), 1, 2)
}


def test_address(client, auth, monkeypatch):

    # define a monkeypatch method
    def mock_get_address(*args, **kwargs):
        if crypto_in_config(args[0]):
            return TEST_ADDRESSES.get(args[1])
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for txs_service.addresses_service
    monkeypatch.setattr(gsrest.service.addresses_service, "get_address",
                        mock_get_address)

    auth.login()

    # request existing address
    response = client.get('btc/addresses/{}'.format(address1))
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'address' in json_data
    assert json_data['outDegree'] == TEST_ADDRESSES[address1].outDegree
    assert json_data['inDegree'] == TEST_ADDRESSES[address1].inDegree
    assert json_data['noIncomingTxs'] == TEST_ADDRESSES[address1].noIncomingTxs
    assert json_data['noOutgoingTxs'] == TEST_ADDRESSES[address1].noOutgoingTxs
    # TODO: test values once exchange rates are available
    # assert json_data['balance'] == TEST_ADDRESSES[address1].balance
    # assert json_data['firstTx'] == TEST_ADDRESSES[address1].firstTx
    # assert json_data['lastTx'] == TEST_ADDRESSES[address1].lastTx
    # assert json_data['totalReceived'] == TEST_ADDRESSES[address1].totalReceived
    # assert json_data['totalSpent'] == TEST_ADDRESSES[address1].totalSpent

    # request non-existing address
    response = client.get('/btc/addresses/{}'.format(non_existing_address))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Address {} not found in currency btc'.format(non_existing_address)\
           in json_data['message']
#
    # request tx of non-existing currency
    response = client.get('/{}/addresses/{}'.format(non_existing_currency,
                                                    address1))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Unknown currency in config: {}'.format(non_existing_currency) in \
           json_data['message']
#
#
