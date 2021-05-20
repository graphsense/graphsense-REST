from openapi_server.models.address import Address
from openapi_server.models.addresses import Addresses
from openapi_server.models.values import Values
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.entity_tag import EntityTag
from openapi_server.models.tags_by_entity import TagsByEntity
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.entity import Entity
from openapi_server.models.link_utxo import LinkUtxo
import gsrest.service.addresses_service as service
from gsrest.test.assertion import assertEqual
from openapi_server.models.address_tx_utxo import AddressTxUtxo
from openapi_server.models.address_txs import AddressTxs
from gsrest.util.values import convert_value
from gsrest.service.rates_service import list_rates
from gsrest.test.txs_service import tx1_eth, tx2_eth
import base64


tag = AddressTag(
           category="organization",
           label="Internet, Archive",
           abuse=None,
           lastmod=1560290400,
           source="https://archive.org/donate/cryptocurrency",
           address="1Archive1n2C579dMsAu3iC6tWzuQJz8dN",
           tagpack_uri="http://tagpack_uri",
           active=True,
           currency='btc'
        )

tag2 = AddressTag(
           category="organization",
           label="Internet Archive 2",
           abuse=None,
           lastmod=1560290400,
           source="https://archive.org/donate/cryptocurrency",
           address="1Archive1n2C579dMsAu3iC6tWzuQJz8dN",
           tagpack_uri="http://tagpack_uri",
           active=True,
           currency='btc'
        )

eth_tag = AddressTag(
           category=None,
           label="TagA",
           abuse=None,
           lastmod=1,
           source="sourceX",
           address="abcdef",
           tagpack_uri="uriX",
           active=True,
           currency='eth'
        )

eth_tag2 = AddressTag(
           category=None,
           label="TagB",
           abuse=None,
           lastmod=1,
           source="sourceY",
           address="abcdef",
           tagpack_uri="uriY",
           active=True,
           currency='eth'
        )

etag = EntityTag(
           category="organization",
           label="Internet, Archive",
           abuse=None,
           lastmod=1560290400,
           source="https://archive.org/donate/cryptocurrency",
           entity=17642138,
           tagpack_uri="http://tagpack_uri",
           active=True,
           currency='btc'
        )

etag2 = EntityTag(
           category="organization",
           label="Internet Archive 2",
           abuse=None,
           lastmod=1560290400,
           source="https://archive.org/donate/cryptocurrency",
           entity=17642138,
           tagpack_uri="http://tagpack_uri",
           active=True,
           currency='btc'
        )

atag1 = AddressTag(
    abuse=None,
    active=True,
    address='17gN64BPHtxi4mEM3qWrxdwhieUvRq8R2r',
    category='organization',
    currency='btc',
    label='addressTag1',
    lastmod=1,
    source='https://archive.org/donate/cryptocurrency',
    tagpack_uri='http://tagpack_uri'
)

atag2 = AddressTag(
    abuse=None,
    active=True,
    address='1KeDrQdATuXaZFW4CL9tfe2zpQ5SrmBFWc',
    category='organization',
    currency='btc',
    label='addressTag2',
    lastmod=2,
    source='https://archive.org/donate/cryptocurrency',
    tagpack_uri='http://tagpack_uri'
)


address = Address(
   first_tx=TxSummary(
      tx_hash="04d92601677d62a985310b61a301e74870fa942c"
      "8be0648e16b1db23b996a8cd",
      height=1,
      timestamp=1378415426
   ),
   total_spent=Values(
      usd=2541183.0,
      value=40296873552,
      eur=2118309.0
   ),
   out_degree=284,
   no_incoming_txs=3981,
   no_outgoing_txs=267,
   total_received=Values(
      usd=2543214.5,
      value=40412296129,
      eur=2130676.5
   ),
   last_tx=TxSummary(
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea"
      "5b94b304d438a8225850f05b45ae5",
      height=2,
      timestamp=1602006938
   ),
   address="1Archive1n2C579dMsAu3iC6tWzuQJz8dN",
   in_degree=5013,
   balance=Values(eur=1.15, usd=2.31, value=115422577),
        )

addressWithTags = Address(
   **address.to_dict()
   )
addressWithTags.tags = [tag]


address2 = Address(
   out_degree=1,
   no_incoming_txs=1,
   total_spent=Values(
      value=1260000,
      usd=103.8,
      eur=88.46
   ),
   last_tx=TxSummary(
      timestamp=1511153263,
      tx_hash="a8826f8b164ddf6d173b335051896570cee818e62d793423620fd"
      "16b836ba52e",
      height=2
   ),
   total_received=Values(
      eur=70.96,
      usd=82.79,
      value=1260000
   ),
   in_degree=1,
   first_tx=TxSummary(
      tx_hash="6e7456a7a0e4cc2c4ade617e4e950ece015c00add338be345ce2b"
      "544e5a86322",
      timestamp=1510347493,
      height=1
   ),
   address="3Hrnn1UN78uXgLNvtqVXMjHwB41PmX66X4",
   no_outgoing_txs=1,
   balance=Values(eur=0.0, usd=0.0, value=0)
   )

addressWithoutTags = Address(
   **address2.to_dict()
)
addressWithoutTags.tags = []

address3 = Address(
   first_tx=TxSummary(
      timestamp=1540073277,
      tx_hash="8b3f09b110628cf596fa67d470db46d1f65"
              "2fe6ae01b6fb95ebf4b5b7d767df5",
      height=1
   ),
   out_degree=1,
   total_received=Values(
      usd=0.45,
      eur=0.39,
      value=6896
   ),
   address="3Hrnn2xbNUBDfqgLQh6CwfutAm9dfVq67u",
   no_incoming_txs=1,
   in_degree=1,
   no_outgoing_txs=1,
   total_spent=Values(
      value=6896,
      usd=0.45,
      eur=0.39
   ),
   last_tx=TxSummary(
      tx_hash="e87135937ff07e6cf35ecae8224345d1cf"
              "07363d62a0316b9add6137010b022c",
      timestamp=1540074500,
      height=2
   ),
   balance=Values(eur=0.0, usd=0.0, value=0)
)

addressBech32 = Address(
   out_degree=0,
   no_incoming_txs=0,
   total_spent=Values(
      value=0,
      usd=0,
      eur=0
   ),
   last_tx=TxSummary(
      timestamp=0,
      tx_hash="abcd",
      height=0
   ),
   total_received=Values(
      eur=0,
      usd=0,
      value=0
   ),
   in_degree=0,
   first_tx=TxSummary(
      tx_hash="abcd",
      timestamp=0,
      height=0
   ),
   address="bc1xyz123456789",
   no_outgoing_txs=0,
   balance=Values(eur=0.0, usd=0.0, value=0)
)

addressWithTotalSpent0 = Address(
   first_tx=TxSummary(
      tx_hash="04d92601677d62a985310b61a301e74870fa942c"
      "8be0648e16b1db23b996a8cd",
      height=1,
      timestamp=1378415426
   ),
   total_spent=Values(
      usd=0.0,
      value=0,
      eur=0.0
   ),
   out_degree=284,
   no_incoming_txs=3981,
   no_outgoing_txs=267,
   total_received=Values(
      usd=0.11,
      value=18099,
      eur=0.1
   ),
   last_tx=TxSummary(
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea"
      "5b94b304d438a8225850f05b45ae5",
      height=2,
      timestamp=1602006938
   ),
   address="13k8QzZMyce7hF4rT18CHVozE3ooNiFgfF",
   in_degree=5013,
   balance=Values(eur=0.0, usd=0.0, value=18099)
   )

addressWithTagsOutNeighbors = Neighbors(
        next_page=None,
        neighbors=[
            Neighbor(
                id="17DfZja1713S3JRWA9jaebCKFM5anUh7GG",
                node_type='address',
                has_labels=False,
                received=Values(
                        value=87789282,
                        usd=142.18,
                        eur=114.86),
                balance=Values(
                        value=0,
                        usd=0.0,
                        eur=0.0),
                no_txs=1,
                estimated_value=Values(
                    value=27789282,
                    usd=87.24,
                    eur=72.08)
                ),
            Neighbor(
                id="1LpXFVskUaE2cs5xkQE5bDDaX8hff4L2Ej",
                node_type='address',
                has_labels=False,
                received=Values(
                        value=67789282,
                        usd=121.46,
                        eur=98.72),
                balance=Values(
                        value=0,
                        usd=0.0,
                        eur=0.0),
                no_txs=1,
                estimated_value=Values(
                    value=27789282,
                    usd=87.24,
                    eur=72.08)
                )])

addressWithTagsInNeighbors = Neighbors(
        next_page=None,
        neighbors=[
            Neighbor(
                id="1BLCmwzV5KXdd4zuonoxaBC9YobJfrkxFg",
                node_type='address',
                has_labels=False,
                received=Values(
                        value=59308362491,
                        usd=17221.5,
                        eur=12887.89),
                balance=Values(
                        value=606,
                        usd=0.0,
                        eur=0.0),
                no_txs=1,
                estimated_value=Values(
                    value=1091,
                    usd=0.01,
                    eur=0.0)
                ),
            Neighbor(
                id="1KzsFAeH9rL6nVXDEt9mnFHR3sekBjpNSt",
                node_type='address',
                has_labels=False,
                received=Values(
                        value=5000000000,
                        usd=13.41,
                        eur=9.87),
                balance=Values(
                        value=0,
                        usd=0.0,
                        eur=0.0),
                no_txs=1,
                estimated_value=Values(
                    value=50000000,
                    usd=404.02,
                    eur=295.7)
                )])


entityWithTagsOfAddressWithTags = Entity(
   no_outgoing_txs=280,
   last_tx=TxSummary(
      height=651545,
      tx_hash="5678",
      timestamp=1602006938
   ),
   total_spent=Values(
      eur=2291256.5,
      value=138942266867,
      usd=2762256.25
   ),
   in_degree=4358,
   no_addresses=110,
   total_received=Values(
      usd=2583655.0,
      eur=2162085.5,
      value=139057689444
   ),
   no_incoming_txs=4859,
   entity=17642138,
   out_degree=176,
   first_tx=TxSummary(
      timestamp=1323298692,
      height=156529,
      tx_hash="4567"
   ),
   balance=Values(
            value=115422577,
            usd=2.31,
            eur=1.15),
   tags=TagsByEntity(
       entity_tags=[etag2, etag],
       address_tags=[atag1, atag2],
       tag_coherence=None)
)

eth_address = Address(
   first_tx=TxSummary(
      tx_hash="af6e0000",
      height=1,
      timestamp=11
   ),
   total_spent=Values(
      eur=30.33,
      value=12300000000,
      usd=40.44
   ),
   out_degree=6,
   no_incoming_txs=5,
   no_outgoing_txs=10,
   total_received=Values(
      eur=10.11,
      value=23400000000,
      usd=20.22
   ),
   last_tx=TxSummary(
      tx_hash="af6e0003",
      height=1,
      timestamp=12
   ),
   address="abcdef",
   in_degree=5,
   balance=Values(eur=111.0, usd=222.0, value=11100000000))


eth_addressWithTags = Address(
   **eth_address.to_dict()
   )
eth_addressWithTags.tags = [eth_tag, eth_tag2]


eth_address2 = Address(
   last_tx=TxSummary(
      tx_hash="af6e0003",
      height=2,
      timestamp=22
   ),
   in_degree=1,
   no_incoming_txs=1,
   out_degree=2,
   total_received=Values(
            value=45600000000,
            eur=40.44,
            usd=50.56),
   balance=Values(
            value=11100000000,
            usd=222.0,
            eur=111.0),
   no_outgoing_txs=2,
   total_spent=Values(
            value=34500000000,
            eur=50.56,
            usd=60.67),
   first_tx=TxSummary(
      timestamp=21,
      tx_hash="af6e0000",
      height=1
   ),
   address="123456"
)

eth_addressWithTagsOutNeighbors = Neighbors(
        next_page=None,
        neighbors=[
            Neighbor(
                id="abcdef",
                node_type='address',
                has_labels=False,
                received=Values(
                        value=12300000000,
                        eur=22.22,
                        usd=33.33),
                balance=Values(
                        value=2300000000,
                        usd=46.0,
                        eur=23.0),
                no_txs=4,
                estimated_value=Values(
                    value=1000000000,
                    usd=20.0,
                    eur=10.0)
                ),
            Neighbor(
                id="123456",
                node_type='address',
                has_labels=False,
                received=Values(
                        value=12300000000,
                        eur=22.22,
                        usd=33.33),
                balance=Values(
                        value=2300000000,
                        usd=46.0,
                        eur=23.0),
                no_txs=4,
                estimated_value=Values(
                    value=1000000000,
                    usd=20.0,
                    eur=10.0)
                )])

eth_entityWithTags = Entity(
   no_outgoing_txs=eth_address.no_outgoing_txs,
   last_tx=eth_address.last_tx,
   total_spent=eth_address.total_spent,
   in_degree=eth_address.in_degree,
   no_addresses=1,
   total_received=eth_address.total_received,
   no_incoming_txs=eth_address.no_incoming_txs,
   entity=eth_address.address + '_',
   out_degree=eth_address.out_degree,
   first_tx=eth_address.first_tx,
   balance=eth_address.balance,
   tags=TagsByEntity(address_tags=[], entity_tags=[], tag_coherence=None)
)


def get_address(test_case):
    """Test case for get_address
    """
    result = service.get_address(
            'btc', addressWithoutTags.address, True)
    test_case.assertEqual(addressWithoutTags, result)
    result = service.get_address(
            'btc', addressWithTags.address, True)
    assertEqual(addressWithTags, result)
    result = service.get_address(
                'btc', addressBech32.address, False)
    test_case.assertEqual(addressBech32, result)
    result = service.get_address(
                currency='btc', address=addressWithTotalSpent0.address)
    test_case.assertEqual(addressWithTotalSpent0, result)

    # ETH
    result = service.get_address(
            'eth', eth_addressWithTags.address)
    test_case.assertEqual(eth_address, result)


def list_address_txs(test_case):
    """Test case for list_address_txs

    Get all transactions an address has been involved in
    """
    rates = list_rates(currency='btc', heights=[2])
    address_txs = AddressTxs(
                    next_page=None,
                    address_txs=[
                        AddressTxUtxo(
                            tx_hash="123456",
                            value=convert_value(1260000, rates[2]),
                            height=2,
                            timestamp=1510347493),
                        AddressTxUtxo(
                            tx_hash="abcdef",
                            value=convert_value(-1260000, rates[2]),
                            height=2,
                            timestamp=1511153263)
                        ]
                    )
    result = service.list_address_txs('btc', address2.address)
    test_case.assertEqual(address_txs, result)

    txs = AddressTxs(address_txs=[tx1_eth, tx2_eth])
    result = service.list_address_txs('eth', eth_address.address)
    test_case.assertEqual(txs, result)


def list_address_txs_csv(test_case):
    result = service.list_address_txs_csv('btc', address2.address)
    test_case.assertEqual(
        'currency_type,height,timestamp,tx_hash,value_eur,value_usd,'
        'value_value\r\n'
        'utxo,2,1510347493,123456,0.01,0.03,'
        '1260000\r\n'
        'utxo,2,1511153263,abcdef,-0.01,-0.03,'
        '-1260000\r\n', result.data.decode('utf-8'))

    result = service.list_address_txs_csv('eth', eth_address.address)
    test_case.assertEqual(
        'currency_type,height,timestamp,tx_hash,values_eur,values_usd,'
        'values_value\r\n'
        'account,1,15,af6e0000,123.0,246.0,12300000000\r\n'
        'account,1,16,af6e0003,234.0,468.0,23400000000\r\n',
        result.data.decode('utf-8'))


def list_tags_by_address(test_case):
    result = service.list_tags_by_address('btc', addressWithTags.address)
    assertEqual(addressWithTags.tags, result)

    result = service.list_tags_by_address('eth', eth_addressWithTags.address)
    assertEqual(eth_addressWithTags.tags, result)


def list_tags_by_address_csv(test_case):
    csv = ("abuse,active,address,category,currency,label,lastmod,"
           "source,tagpack_uri\r\n,True,1Archive1n2C579dMsAu3iC6"
           "tWzuQJz8dN,organization,btc,\"Internet, Archive\",1560290400"
           ",https://archive.org/donate/cryptocurrency,http://tagpack_uri\r\n")
    csv = base64.b64encode(csv.encode("utf-8"))
    result = service.list_tags_by_address_csv(
                        "btc",
                        address.address).data.decode('utf-8')
    result = base64.b64encode(result.encode("utf-8"))
    assertEqual(csv, result)


def list_address_neighbors(test_case):
    result = service.list_address_neighbors(
        currency='btc',
        address=address.address,
        direction='out')
    test_case.assertEqual(addressWithTagsOutNeighbors, result)

    result = service.list_address_neighbors(
        currency='btc',
        address=address.address,
        direction='in')
    test_case.assertEqual(addressWithTagsInNeighbors, result)

    result = service.list_address_neighbors(
        currency='eth',
        address=eth_address.address,
        direction='out')
    test_case.assertEqual(eth_addressWithTagsOutNeighbors, result)


def list_address_neighbors_csv(test_case):
    csv = ("balance_eur,balance_usd,balance_value,estimated_value_eur,"
           "estimated_value_usd,estimated_value_value,has_labels,id,no_txs,"
           "node_type,received_eur,received_usd,received_value\r\n0.0,0.0,"
           "0,72.08,87.24,27789282,False,17DfZja1713S3JRWA9jaebCKFM5anUh7GG"
           ",1,address,114.86,142.18,87789282\r\n0.0,0.0,0,72.08,87.24,"
           "27789282,False,1LpXFVskUaE2cs5xkQE5bDDaX8hff4L2Ej,1,address,98.72,"
           "121.46,67789282\r\n")
    result = service.list_address_neighbors_csv(
        currency='btc',
        address=address.address,
        direction='out')
    assertEqual(csv, result.data.decode('utf-8'))


def get_address_entity(test_case):
    result = service.get_address_entity(
                currency='btc',
                address=address.address,
                include_tags=True)
    result.tags.tag_coherence = None
    test_case.assertEqual(entityWithTagsOfAddressWithTags, result)

    result = service.get_address_entity(
                currency='eth',
                address=eth_address.address,
                include_tags=True)
    result.tags.tag_coherence = None
    test_case.assertEqual(eth_entityWithTags, result)


def list_address_links(test_case):
    result = service.list_address_links(
                currency='btc',
                address=address.address,
                neighbor='17DfZja1713S3JRWA9jaebCKFM5anUh7GG')
    link = [LinkUtxo(tx_hash='123456',
                     input_value=Values(eur=-0.1, usd=-0.2, value=-10000000),
                     output_value=Values(eur=-0.1, usd=-0.2, value=-10000000),
                     timestamp=1361497172,
                     height=2)]

    test_case.assertEqual(link, result)

    result = service.list_address_links(
                currency='eth',
                address=eth_address.address,
                neighbor='123456')
    txs = [tx1_eth, tx2_eth]
    test_case.assertEqual(txs, result)


def list_address_links_csv(test_case):
    result = service.list_address_links_csv(
                currency='btc',
                address=address.address,
                neighbor='17DfZja1713S3JRWA9jaebCKFM5anUh7GG')

    csv = ('currency_type,height,input_value_eur,input_value_usd,'
           'input_value_value,output_value_eur,output_value_usd,'
           'output_value_value,timestamp,tx_hash\r\n'
           'utxo,2,-0.1,-0.2,-10000000,-0.1,-0.2,-10000000,'
           '1361497172,123456\r\n')

    test_case.assertEqual(csv, result.data.decode('utf-8'))

    result = service.list_address_links_csv(
                currency='eth',
                address=eth_address.address,
                neighbor='123456')

    csv = ('currency_type,height,timestamp,tx_hash,values_eur,'
           'values_usd,values_value\r\n'
           'account,1,15,af6e0000,123.0,246.0,12300000000\r\n'
           'account,1,16,af6e0003,234.0,468.0,23400000000\r\n')
    test_case.assertEqual(csv, result.data.decode('utf-8'))


def list_addresses(test_case):
    result = service.list_addresses('btc', pagesize=2)
    test_case.assertEqual([address2, address3],
                          result.addresses)
    test_case.assertIsNot(result.next_page, None)

    ids = [address.address,
           address3.address,
           'doesnotexist']
    result = service.list_addresses('btc', ids=ids)

    test_case.assertEqual(Addresses(
                            next_page=None,
                            addresses=[address, address3]),
                          result)

    result = service.list_addresses('eth')
    assertEqual([eth_address, eth_address2], result.addresses)
    test_case.assertIs(result.next_page, None)

    ids = [eth_address2.address, 'aaaa']

    result = service.list_addresses('eth', ids=ids)
    assertEqual([eth_address2], result.addresses)
    test_case.assertIs(result.next_page, None)


def list_addresses_csv(test_case):
    result = service.list_addresses_csv(
                "btc", [address.address]).data.decode('utf-8')
    assertEqual(3, len(result.split("\r\n")))
    result = service.list_addresses_csv(
                "eth", [eth_address.address]).data.decode('utf-8')
    assertEqual(3, len(result.split("\r\n")))
