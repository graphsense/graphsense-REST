from collections import namedtuple

from gsrest.model.addresses import Address, AddressTx
from gsrest.model.txs import TxSummary
from gsrest.model.tags import Tag
import gsrest.service.addresses_service
import gsrest.service.common_service
from gsrest.util.checks import check_inputs

non_existing_address = 'zzzzz'
non_existing_currency = 'abc'
address1 = 'bc1q2jhyw77crz3xqjml30jpw8zf66dr366kec68a9'  # no more txs
address2 = '3Aa7BnDG7XeuSZwL7Hzo3p87eiqoaAG3s3'  # txs were easy to fetch
address3 = '1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s'  # binance
address4 = '1A8pUXyXzqWQzqR6q2djwrXuG4nfici4KY'  # random
address5 = '1N4RJ9fRGzk1HCWfqZs3jYdSJZprC4D76Y'  # tags error
address6 = '112AmFATxzhuSpvtz1hfpa3Zrw3BG276pc'  # locky
address7 = '1NFnCeW8MBpqNJf9pdT7Qk8fpUgYJAZ1bh'  # sextortion talos
first_tx = TxSummary(577281, 1558549477, bytearray.fromhex(
    '39435696ea53d580f15f85fcae5f084ff9c3ba6b5f1b84d4e1e41d8fceb5d0ba'))
last_tx = TxSummary(585637, 1563268350, bytearray.fromhex(
    'e11c9764f94f5bc8ea2b59ebe6d1e49a69a820d5b46eb9861e0f581be911071a'))
tx1 = 'ab188013f626405ddebf1a7b2e0af34253d09e80f9ef7f981ec1ec59d6200c1f'

total_received1 = {'value': 649456, 'eur': 44.39, 'usd': 49.51}
total_spent1 = {'value': 649456, 'eur': 54.59, 'usd': 61.19}

received1 = namedtuple('input1',
                       total_received1.keys())(*total_received1.values())
spent1 = namedtuple('input1', total_spent1.keys())(*total_spent1.values())

TEST_ADDRESSES = {
    address1: Address(address1, first_tx, last_tx, 1, 1,
                      received1, spent1,
                      1, 2, {'eur': 0.5, 'usd': 0.5}).to_dict()
}

TEST_ADDRESSES_TXS = {
    address1: [
        AddressTx(address1, first_tx.height, first_tx.timestamp,
                  first_tx.tx_hash.hex(), 649456, {'eur': 0.5, 'usd': 0.5})
        .to_dict(),
        AddressTx(address1, last_tx.height, last_tx.timestamp,
                  last_tx.tx_hash.hex(), -649456, {'eur': 0.5, 'usd': 0.5})
        .to_dict()
    ]
}

TEST_ADDRESSES_TAGS = {
    address2: [Tag(
        address2,
        "Shapeshift",
        "exchange",
        None,
        "https://git-service.ait.ac.at/dil-graphsense/"
        "graphsense-tagpacks-private/tree/master/packs/shapeshift.yaml",
        "https://arxiv.org/abs/1810.12786",
        1565128800,
        True,
        'btc',
    ).to_dict()]
}


def test_address(client, auth, monkeypatch):

    def mock_get_address(*args):
        check_inputs(currency=args[0])
        return TEST_ADDRESSES.get(args[1])
    monkeypatch.setattr(gsrest.service.common_service, "get_address",
                        mock_get_address)

    def mock_list_address_tags(*args):
        check_inputs(currency=args[0])
        return []
    monkeypatch.setattr(gsrest.service.common_service, "list_address_tags",
                        mock_list_address_tags)

    auth.login()

    response = client.get('btc/addresses/{}'.format(address1))
    assert response.status_code == 200
    json_data = response.get_json()

    assert set(TEST_ADDRESSES[address1].keys()) == set(json_data.keys())
    for k, v in json_data.items():
        if k == 'tags':
            assert isinstance(type(v), type(list))
        else:
            assert v == TEST_ADDRESSES[address1][k]

    response = client.get('{}/addresses/{}'.format(non_existing_currency,
                                                   address1))
    assert response.status_code == 404
    json_data = response.get_json()
    assert 'Unknown currency in config: {}'.format(non_existing_currency) in \
           json_data['message']


def test_address_txs(client, auth, monkeypatch):

    def mock_list_address_txs(*args):
        check_inputs(currency=args[0])
        return None, TEST_ADDRESSES_TXS.get(args[1])

    monkeypatch.setattr(gsrest.service.addresses_service, "list_address_txs",
                        mock_list_address_txs)

    auth.login()

    response = client.get('btc/addresses/{}/txs'.format(address1))
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'address_txs' in json_data
    assert len(json_data['address_txs']) == len(TEST_ADDRESSES_TXS[address1])
    for i, tx in enumerate(json_data['address_txs']):
        for k in TEST_ADDRESSES_TXS[address1][i]:
            assert json_data['address_txs'][i][k] == \
                   TEST_ADDRESSES_TXS[address1][i][k]


def test_address_tags(client, auth, monkeypatch):

    def mock_list_address_tags(*args):
        check_inputs(currency=args[0])
        return TEST_ADDRESSES_TAGS.get(args[1])

    monkeypatch.setattr(gsrest.service.common_service, "list_address_tags",
                        mock_list_address_tags)

    auth.login()

    response = client.get('btc/addresses/{}/tags'.format(address2))
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == len(TEST_ADDRESSES_TAGS[address2])
    for i in range(len(json_data)):
        for k in TEST_ADDRESSES_TAGS[address2][i]:
            assert json_data[i][k] == TEST_ADDRESSES_TAGS[address2][i][k]


def test_address_tags_csv(client, auth, monkeypatch):

    def mock_list_address_tags(*args):
        check_inputs(currency=args[0])
        return TEST_ADDRESSES_TAGS.get(args[1])

    monkeypatch.setattr(gsrest.service.common_service, "list_address_tags",
                        mock_list_address_tags)

    auth.login()

    response = client.get('btc/addresses/{}/tags'.format(address2))
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == len(TEST_ADDRESSES_TAGS[address2])


# def test_address_neighbors(client, auth, monkeypatch):
#
#     def mock_list_address_neighbors(*args):
#         check_inputs(currency=args[0])
#         paging_state = None
#         return paging_state
#
#     def mock_list_address_tags(*args):
#         check_inputs(currency=args[0])
#         return None
#
#     monkeypatch.setattr(gsrest.service.addresses_service,
#                         "list_address_incoming_relations",
#                         mock_list_address_neighbors)
#
#     monkeypatch.setattr(gsrest.service.addresses_service,
#                         "list_address_outgoing_relations",
#                         mock_list_address_neighbors)
#
#     monkeypatch.setattr(gsrest.service.common_service,
#                         "list_address_tags",
#                         mock_list_address_tags)
#
#     auth.login()
#
