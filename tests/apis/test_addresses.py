import gsrest.service.addresses_service
from gsrest.model.addresses import Address, AddressTx
from gsrest.model.txs import TxSummary
from gsrest.model.tags import Tag
from gsrest.util.checks import crypto_in_config

non_existing_address = 'zzzzz'
non_existing_currency = 'abc'
address1 = 'bc1q2jhyw77crz3xqjml30jpw8zf66dr366kec68a9'
address2 = '3Aa7BnDG7XeuSZwL7Hzo3p87eiqoaAG3s3'
first_tx = TxSummary(577281, 1558549477, bytearray.fromhex('39435696ea53d580f15f85fcae5f084ff9c3ba6b5f1b84d4e1e41d8fceb5d0ba'))
last_tx = TxSummary(585637, 1563268350, bytearray.fromhex('e11c9764f94f5bc8ea2b59ebe6d1e49a69a820d5b46eb9861e0f581be911071a'))
tx1 = 'ab188013f626405ddebf1a7b2e0af34253d09e80f9ef7f981ec1ec59d6200c1f'

TEST_ADDRESSES = {
    address1: Address(address1, first_tx, last_tx, 1, 1,
                      {'value': 649456, 'eur': 44.39, 'usd': 49.51},
                      {'value': 649456, 'eur': 54.59, 'usd': 61.19},
                      1, 2, {'eur': 0.5, 'usd': 0.5}).to_dict()
}

TEST_ADDRESSES_TXS = {
    address1: [
        AddressTx(address1, first_tx.height, first_tx.timestamp, first_tx.tx_hash.hex(), 649456, {'eur': 0.5, 'usd': 0.5}).to_dict(),
        AddressTx(address1, last_tx.height, last_tx.timestamp, last_tx.tx_hash.hex(), -649456, {'eur': 0.5, 'usd': 0.5}).to_dict()
    ]
}

TEST_ADDRESSES_TAGS = {
    address2: [Tag(
        address2,
        "Shapeshift",
        "Other",
        None,
        "https://git-service.ait.ac.at/dil-graphsense/graphsense-tagpacks-private/tree/master/shapeshift.yaml",
        "https://arxiv.org/abs/1810.12786",
        1565128800,
        'btc',
    ).to_dict()]
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
    assert TEST_ADDRESSES[address1].keys() == json_data.keys()
    for k, v in json_data.items():
        assert v == TEST_ADDRESSES[address1][k]

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


def test_address_txs(client, auth, monkeypatch):

    # define a monkeypatch method
    def mock_get_address_txs(*args, **kwargs):
        if crypto_in_config(args[0]):
            return None, TEST_ADDRESSES_TXS.get(args[1])
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for addresses_service
    monkeypatch.setattr(gsrest.service.addresses_service, "list_address_txs",
                        mock_get_address_txs)

    auth.login()

    # request existing address
    response = client.get('btc/addresses/{}/txs'.format(address1))
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'address_txs' in json_data
    assert len(json_data['address_txs']) == len(TEST_ADDRESSES_TXS[address1])
    for i, tx in enumerate(json_data['address_txs']):
        for k in TEST_ADDRESSES_TXS[address1][i]:
            assert json_data['address_txs'][i][k] == TEST_ADDRESSES_TXS[address1][i][k]


def test_address_tags(client, auth, monkeypatch):

    # define a monkeypatch method
    def mock_list_address_tags(*args, **kwargs):
        if crypto_in_config(args[0]):
            return TEST_ADDRESSES_TAGS.get(args[1])
        # else 404 from crypto_in_config()

    # apply the monkeypatch method for addresses_service
    monkeypatch.setattr(gsrest.service.addresses_service, "list_address_tags",
                        mock_list_address_tags)

    auth.login()

    # request existing address
    response = client.get('btc/addresses/{}/tags'.format(address2))
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == len(TEST_ADDRESSES_TAGS[address2])
    for i in range(len(json_data)):
        for k in TEST_ADDRESSES_TAGS[address2][i]:
            assert json_data[i][k] == TEST_ADDRESSES_TAGS[address2][i][k]
