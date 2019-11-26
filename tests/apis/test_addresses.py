import gsrest.service.addresses_service
from gsrest.model.addresses import Address, AddressTx
from gsrest.model.txs import TxSummary
from gsrest.util.checks import crypto_in_config

non_existing_address = 'zzzzz'
non_existing_currency = 'abc'
address1 = 'bc1q2jhyw77crz3xqjml30jpw8zf66dr366kec68a9'
first_tx = TxSummary(577281, 1558549477, bytearray.fromhex('39435696ea53d580f15f85fcae5f084ff9c3ba6b5f1b84d4e1e41d8fceb5d0ba'))
last_tx = TxSummary(585637, 1563268350, bytearray.fromhex('e11c9764f94f5bc8ea2b59ebe6d1e49a69a820d5b46eb9861e0f581be911071a'))
tx1 = 'ab188013f626405ddebf1a7b2e0af34253d09e80f9ef7f981ec1ec59d6200c1f'

TEST_ADDRESSES = {
    address1: Address(address1, first_tx, last_tx, 1, 1,
                      {'value': 649456, 'eur': 44.39, 'usd': 49.51},
                      {'value': 649456, 'eur': 54.59, 'usd': 61.19},
                      1, 2, {'eur': 0.5, 'usd': 0.5})
}

TEST_ADDRESSES_TXS = {
    address1: [
        AddressTx(address1, first_tx.height, first_tx.timestamp, first_tx.tx_hash, 649456, {'eur': 0.5, 'usd': 0.5}),
        AddressTx(address1, last_tx.height, last_tx.timestamp, last_tx.tx_hash, -649456, {'eur': 0.5, 'usd': 0.5})
    ]
}


def test_address(client, auth, monkeypatch):

    # define a monkeypatch method
    def mock_get_address(*args, **kwargs):
        if crypto_in_config(args[0]):
            return TEST_ADDRESSES.get(args[1])
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for addresses_service
    monkeypatch.setattr(gsrest.service.addresses_service, "get_address",
                        mock_get_address)

    auth.login()

    # request existing address
    response = client.get('btc/addresses/{}'.format(address1))
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'address' in json_data
    assert json_data['out_degree'] == TEST_ADDRESSES[address1].out_degree
    assert json_data['in_degree'] == TEST_ADDRESSES[address1].in_degree
    assert json_data['no_incoming_txs'] == TEST_ADDRESSES[address1].no_incoming_txs
    assert json_data['no_outgoing_txs'] == TEST_ADDRESSES[address1].no_outgoing_txs
    # TODO: test values once exchange rates are available
    assert json_data['balance'] == TEST_ADDRESSES[address1].balance
    assert json_data['first_tx'] == TEST_ADDRESSES[address1].first_tx
    assert json_data['last_tx'] == TEST_ADDRESSES[address1].last_tx
    assert json_data['total_received'] == TEST_ADDRESSES[address1].total_received
    assert json_data['total_spent'] == TEST_ADDRESSES[address1].total_spent

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
