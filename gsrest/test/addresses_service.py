from openapi_server.models.address import Address
from openapi_server.models.addresses import Addresses
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.entity_tag import EntityTag
from openapi_server.models.tags import Tags
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.entity import Entity
from openapi_server.models.link_utxo import LinkUtxo
from openapi_server.models.links import Links
import gsrest.service.addresses_service as service
from gsrest.test.assertion import assertEqual
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.txs import Txs
from gsrest.util.values import convert_value
from gsrest.service.rates_service import list_rates
from gsrest.test.txs_service import tx1_eth, tx2_eth, tx4_eth
from gsrest.util.values import make_values
import copy
from tests.util.util import yamldump


tag = AddressTag(
           category="organization",
           label="Internet, Archive",
           abuse=None,
           lastmod=1560290400,
           source="https://archive.org/donate/cryptocurrency",
           address="addressA",
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
           address="addressA",
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
           address="0xabcdef",
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
           address="0xabcdef",
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
    address='addressA',
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
    address='addressH',
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
      timestamp=1361497172
   ),
   total_spent=make_values(
      usd=2541183.0,
      value=40296873552,
      eur=2118309.0
   ),
   out_degree=284,
   no_incoming_txs=3981,
   no_outgoing_txs=267,
   total_received=make_values(
      usd=2543214.5,
      value=40412296129,
      eur=2130676.5
   ),
   last_tx=TxSummary(
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea"
      "5b94b304d438a8225850f05b45ae5",
      height=1,
      timestamp=1361497172
   ),
   address="addressA",
   entity=17642138,
   in_degree=5013,
   balance=make_values(eur=1.15, usd=2.31, value=115422577),
        )

addressWithTags = Address(
   **address.to_dict()
   )
addressWithTags.tags = [tag]


address2 = Address(
   out_degree=1,
   no_incoming_txs=1,
   total_spent=make_values(
      value=1260000,
      usd=103.8,
      eur=88.46
   ),
   first_tx=TxSummary(
      timestamp=1361497172,
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea5b94b304d438a822585"
      "0f05b45ae5",
      height=1
   ),
   total_received=make_values(
      eur=70.96,
      usd=82.79,
      value=1260000
   ),
   in_degree=1,
   last_tx=TxSummary(
      tx_hash="6e7456a7a0e4cc2c4ade617e4e950ece015c00add338be345ce2b"
      "544e5a86322",
      timestamp=1510347493,
      height=2
   ),
   address="bc1xyz123456789",
   entity=325790641,
   no_outgoing_txs=1,
   balance=make_values(eur=0.0, usd=0.0, value=0)
   )

addressWithoutTags = Address(
   **address2.to_dict()
)
addressWithoutTags.tags = []

address3 = Address(
   first_tx=TxSummary(
      timestamp=1361497172,
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea"
      "5b94b304d438a8225850f05b45ae5",
      height=1
   ),
   out_degree=1,
   total_received=make_values(
      usd=0.45,
      eur=0.39,
      value=6896
   ),
   address="addressJ",
   entity=442606576,
   no_incoming_txs=1,
   in_degree=1,
   no_outgoing_txs=1,
   total_spent=make_values(
      value=6896,
      usd=0.45,
      eur=0.39
   ),
   last_tx=TxSummary(
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea"
      "5b94b304d438a8225850f05b45ae5",
      timestamp=1361497172,
      height=1
   ),
   balance=make_values(eur=0.0, usd=0.0, value=0)
)

addressWithTotalSpent0 = Address(
   first_tx=TxSummary(
      tx_hash="04d92601677d62a985310b61a301e74870fa942c"
      "8be0648e16b1db23b996a8cd",
      height=1,
      timestamp=1361497172
   ),
   total_spent=make_values(
      usd=0.0,
      value=0,
      eur=0.0
   ),
   out_degree=284,
   no_incoming_txs=3981,
   no_outgoing_txs=267,
   total_received=make_values(
      usd=0.11,
      value=18099,
      eur=0.1
   ),
   last_tx=TxSummary(
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea"
      "5b94b304d438a8225850f05b45ae5",
      height=1,
      timestamp=1361497172
   ),
   address="addressC",
   entity=17642139,
   in_degree=5013,
   balance=make_values(eur=0.0, usd=0.0, value=18099)
   )

addressWithTagsOutNeighbors = Neighbors(
        next_page=None,
        neighbors=[
            Neighbor(
                id="addressE",
                node_type='address',
                labels=['labelX', 'labelY'],
                received=make_values(
                        value=87789282,
                        usd=142.18,
                        eur=114.86),
                balance=make_values(
                        value=0,
                        usd=0.0,
                        eur=0.0),
                no_txs=1,
                value=make_values(
                    value=27789282,
                    usd=87.24,
                    eur=72.08)
                ),
            Neighbor(
                id="addressF",
                node_type='address',
                labels=[],
                received=make_values(
                        value=40412296129,
                        usd=2543214.5,
                        eur=2130676.5),
                balance=make_values(
                        value=115422577,
                        usd=2.31,
                        eur=1.15),
                no_txs=1,
                value=make_values(
                    value=27789282,
                    usd=87.24,
                    eur=72.08)
                )])

addressWithTagsInNeighbors = Neighbors(
        next_page=None,
        neighbors=[
            Neighbor(
                id="addressB",
                node_type='address',
                labels=[],
                received=make_values(
                        value=40412296129,
                        usd=2543214.5,
                        eur=2130676.5),
                balance=make_values(
                        value=115422577,
                        usd=2.31,
                        eur=1.15),
                no_txs=1,
                value=make_values(
                    value=1091,
                    usd=0.01,
                    eur=0.0)
                ),
            Neighbor(
                id="addressD",
                node_type='address',
                labels=[],
                received=make_values(
                        value=40412296129,
                        usd=2543214.5,
                        eur=2130676.5),
                balance=make_values(
                        value=115422577,
                        usd=2.31,
                        eur=1.15),
                no_txs=1,
                value=make_values(
                    value=50000000,
                    usd=404.02,
                    eur=295.7)
                )])

addressD = Address(
   first_tx=TxSummary(
      tx_hash="04d92601677d62a985310b61a301e74870fa942c"
      "8be0648e16b1db23b996a8cd",
      height=1,
      timestamp=1361497172
   ),
   total_spent=make_values(
      usd=2541183.0,
      value=40296873552,
      eur=2118309.0
   ),
   out_degree=284,
   no_incoming_txs=3981,
   no_outgoing_txs=267,
   total_received=make_values(
      usd=2543214.5,
      value=40412296129,
      eur=2130676.5
   ),
   last_tx=TxSummary(
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea"
      "5b94b304d438a8225850f05b45ae5",
      height=1,
      timestamp=1361497172
   ),
   address="addressD",
   entity=17642138,
   in_degree=5013,
   balance=make_values(eur=1.15, usd=2.31, value=115422577),
        )

addressE = Address(
   address="addressE",
   entity=17642138,
   last_tx=TxSummary(
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea"
      "5b94b304d438a8225850f05b45ae5",
      height=1,
      timestamp=1361497172,
   ),
   no_outgoing_txs=3,
   balance=make_values(
      value=0,
      eur=0.0,
      usd=0.0
   ),
   out_degree=7,
   first_tx=TxSummary(
      timestamp=1361497172,
      height=1,
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea"
      "5b94b304d438a8225850f05b45ae5"
   ),
   total_received=make_values(
      value=87789282,
      eur=114.86,
      usd=142.18
   ),
   total_spent=make_values(
      value=87789282,
      eur=114.86,
      usd=142.18
   ),
   no_incoming_txs=3,
   in_degree=3
)

entityWithTagsOfAddressWithTags = Entity(
   no_outgoing_txs=280,
   last_tx=TxSummary(
      height=1,
      tx_hash="5678",
      timestamp=1434554207
   ),
   total_spent=make_values(
      eur=2291256.5,
      value=138942266867,
      usd=2762256.25
   ),
   in_degree=4358,
   no_addresses=110,
   total_received=make_values(
      usd=2583655.0,
      eur=2162085.5,
      value=139057689444
   ),
   no_incoming_txs=4859,
   entity=17642138,
   out_degree=176,
   first_tx=TxSummary(
      timestamp=1434554207,
      height=1,
      tx_hash="4567"
   ),
   balance=make_values(
            value=115422577,
            usd=2.31,
            eur=1.15),
   tags=Tags(
       entity_tags=[etag2, etag],
       address_tags=[atag2, atag1],
       tag_coherence=None)
)

eth_address = Address(
   first_tx=TxSummary(
      tx_hash="af6e0000",
      height=1,
      timestamp=15
   ),
   total_spent=make_values(
      eur=30.33,
      value=123000000000000000000,
      usd=40.44
   ),
   out_degree=6,
   no_incoming_txs=5,
   no_outgoing_txs=10,
   total_received=make_values(
      eur=10.11,
      value=234000000000000000000,
      usd=20.22
   ),
   last_tx=TxSummary(
      tx_hash="af6e0003",
      height=1,
      timestamp=16
   ),
   address="0xabcdef",
   entity=107925000,
   in_degree=5,
   balance=make_values(eur=111.0, usd=222.0, value=111000000000000000000))


eth_addressWithTags = Address(
   **eth_address.to_dict()
   )
eth_addressWithTags.tags = [eth_tag, eth_tag2]


eth_address2 = Address(
   last_tx=TxSummary(
      tx_hash="af6e0003",
      height=1,
      timestamp=16
   ),
   in_degree=1,
   no_incoming_txs=1,
   out_degree=2,
   total_received=make_values(
            value=456000000000000000000,
            eur=40.44,
            usd=50.56),
   balance=make_values(
            value=111000000000000000000,
            usd=222.0,
            eur=111.0),
   no_outgoing_txs=2,
   total_spent=make_values(
            value=345000000000000000000,
            eur=50.56,
            usd=60.67),
   first_tx=TxSummary(
      timestamp=15,
      tx_hash="af6e0000",
      height=1
   ),
   address="0x123456",
   entity=107925001
)

eth_address3 = Address(
    **eth_address2.to_dict(),
)
eth_address3.address = "0x234567"
eth_address3.entity = 107925002

eth_addressWithTagsOutNeighbors = Neighbors(
        next_page=None,
        neighbors=[
            Neighbor(
                id="0xabcdef",
                node_type='address',
                labels=[],
                received=make_values(
                        value=234000000000000000000,
                        eur=10.11,
                        usd=20.22),
                balance=make_values(
                        value=111000000000000000000,
                        usd=222.0,
                        eur=111.0),
                no_txs=4,
                value=make_values(
                    value=10000000000000000000,
                    usd=20.0,
                    eur=10.0)
                ),
            Neighbor(
                id="0x123456",
                node_type='address',
                labels=['LabelX', 'LabelY'],
                received=make_values(
                        value=456000000000000000000,
                        eur=40.44,
                        usd=50.56),
                balance=make_values(
                        value=111000000000000000000,
                        usd=222.0,
                        eur=111.0),
                no_txs=4,
                value=make_values(
                    value=10000000000000000000,
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
   entity=107925000,
   out_degree=eth_address.out_degree,
   first_tx=eth_address.first_tx,
   balance=eth_address.balance,
   tags=Tags(address_tags=[eth_tag, eth_tag2], entity_tags=[],
             tag_coherence=None)
)


def get_address(test_case):
    """Test case for get_address
    """
    result = service.get_address(
            'btc', addressWithoutTags.address, True)
    test_case.assertEqual(addressWithoutTags, result)
    result = service.get_address(
            'btc', addressWithTags.address, True)
    test_case.assertEqual(addressWithTags, result)
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
    address_txs = Txs(
                    next_page=None,
                    txs=[
                        TxAccount(
                            tx_hash="123456",
                            value=convert_value('btc', 1260000, rates[2]),
                            height=2,
                            timestamp=1510347493),
                        TxAccount(
                            tx_hash="abcdef",
                            value=convert_value('btc', -1260000, rates[2]),
                            height=2,
                            timestamp=1511153263)
                        ]
                    )
    result = service.list_address_txs('btc', address2.address)
    test_case.assertEqual(address_txs, result)

    tx2_eth_reverse = TxAccount(**copy.deepcopy(tx2_eth.to_dict()))
    tx2_eth_reverse.value.value = -tx2_eth_reverse.value.value
    for v in tx2_eth_reverse.value.fiat_values:
        v.value = -v.value
    txs = Txs(txs=[tx1_eth, tx2_eth_reverse, tx4_eth])
    result = service.list_address_txs('eth', eth_address.address)
    yamldump(result)
    test_case.assertEqual(txs, result)


def list_address_txs_csv(test_case):
    result = service.list_address_txs_csv('btc', address2.address)
    test_case.assertEqual(
        'height,timestamp,tx_hash,tx_type,value_eur,value_usd,'
        'value_value\r\n'
        '2,1510347493,123456,account,0.01,0.03,'
        '1260000\r\n'
        '2,1511153263,abcdef,account,-0.01,-0.03,'
        '-1260000\r\n', result.data.decode('utf-8'))

    result = service.list_address_txs_csv('eth', eth_address.address)
    test_case.assertEqual(
        'height,timestamp,tx_hash,tx_type,value_eur,value_usd,'
        'value_value\r\n'
        '1,15,af6e0000,account,123.0,246.0,123000000000000000000\r\n'
        '1,16,af6e0003,account,-123.0,-246.0,-123000000000000000000\r\n'
        '1,17,123456,account,234.0,468.0,234000000000000000000\r\n',
        result.data.decode('utf-8'))


def list_tags_by_address(test_case):
    result = service.list_tags_by_address('btc', addressWithTags.address)
    assertEqual(addressWithTags.tags, result)

    result = service.list_tags_by_address('eth', eth_addressWithTags.address)
    assertEqual(eth_addressWithTags.tags, result)


def list_tags_by_address_csv(test_case):
    csv = ("abuse,active,address,category,currency,label,lastmod,"
           "source,tagpack_uri\r\n,True,addressA"
           ",organization,btc,\"Internet, Archive\",1560290400"
           ",https://archive.org/donate/cryptocurrency,http://tagpack_uri\r\n")
    csv = csv.encode("utf-8")
    result = service.list_tags_by_address_csv(
                        "btc",
                        address.address).data.decode('utf-8')
    result = result.encode("utf-8")
    test_case.assertEqual(csv, result)


def list_address_neighbors(test_case):
    result = service.list_address_neighbors(
        currency='btc',
        address=address.address,
        include_labels=True,
        direction='out')
    test_case.assertEqual(addressWithTagsOutNeighbors, result)

    result = service.list_address_neighbors(
        currency='btc',
        address=address.address,
        include_labels=True,
        direction='in')
    test_case.assertEqual(addressWithTagsInNeighbors, result)

    result = service.list_address_neighbors(
        currency='eth',
        address=eth_address.address,
        include_labels=True,
        direction='out')
    test_case.assertEqual(eth_addressWithTagsOutNeighbors, result)


def list_address_neighbors_csv(test_case):
    csv = ("balance_eur,balance_usd,balance_value,id,labels,no_txs,"
           "node_type,received_eur,received_usd,received_value,"
           "value_eur,value_usd,value_value\r\n"
           "0.0,0.0,0,addressE,"
           "\"['labelX', 'labelY']\""
           ",1,address,114.86,142.18,87789282,72.08,87.24,27789282\r\n"
           "1.15,2.31,115422577,addressF,[],1,address,2130676.5,2543214.5,"
           "40412296129,72.08,87.24,27789282\r\n")
    result = service.list_address_neighbors_csv(
        currency='btc',
        address=address.address,
        direction='out',
        include_labels=True
        )
    test_case.assertEqual(csv, result.data.decode('utf-8'))


def get_address_entity(test_case):
    result = service.get_address_entity(
                currency='btc',
                address=address.address,
                include_tags=True,
                tag_coherence=False)
    result.tags.tag_coherence = None
    test_case.assertEqual(entityWithTagsOfAddressWithTags, result)

    result = service.get_address_entity(
                currency='eth',
                address=eth_address.address,
                include_tags=True,
                tag_coherence=False)
    result.tags.tag_coherence = None
    test_case.assertEqual(eth_entityWithTags, result)


def list_address_links(test_case):
    result = service.list_address_links(
                currency='btc',
                address=address.address,
                neighbor='addressE')
    link = Links(links=[LinkUtxo(tx_hash='123456',
                                 input_value=make_values(
                                     eur=-0.1, usd=-0.2, value=-10000000),
                                 output_value=make_values(
                                     eur=0.1, usd=0.2, value=10000000),
                                 timestamp=1361497172,
                                 height=2)])

    test_case.assertEqual(link, result)

    result = service.list_address_links(
                currency='eth',
                address=eth_address.address,
                neighbor='0x123456')
    txs = Links(links=[tx1_eth, tx2_eth])
    test_case.assertEqual(txs, result)

    result = service.list_address_links(
                currency='eth',
                address=eth_address.address,
                neighbor='0x123456',
                pagesize=1)
    txs = Links(links=[tx1_eth])
    test_case.assertEqual(txs.links, result.links)
    test_case.assertNotEqual(None, result.next_page)

    result = service.list_address_links(
                currency='eth',
                address=eth_address.address,
                neighbor='0x123456',
                page=result.next_page,
                pagesize=1)
    txs = Links(links=[tx2_eth])
    test_case.assertEqual(txs.links, result.links)
    test_case.assertNotEqual(None, result.next_page)

    result = service.list_address_links(
                currency='eth',
                address=eth_address.address,
                neighbor='0x123456',
                page=result.next_page,
                pagesize=1)
    test_case.assertEqual(Links(links=[]), result)


def list_address_links_csv(test_case):
    result = service.list_address_links_csv(
                currency='btc',
                address=address.address,
                neighbor='addressE')

    csv = ('height,input_value_eur,input_value_usd,'
           'input_value_value,output_value_eur,output_value_usd,'
           'output_value_value,timestamp,tx_hash,tx_type\r\n'
           '2,-0.1,-0.2,-10000000,0.1,0.2,10000000,'
           '1361497172,123456,utxo\r\n')

    test_case.assertEqual(csv, result.data.decode('utf-8'))

    result = service.list_address_links_csv(
                currency='eth',
                address=eth_address.address,
                neighbor='0x123456')

    csv = ('height,timestamp,tx_hash,tx_type,value_eur,'
           'value_usd,value_value\r\n'
           '1,15,af6e0000,account,123.0,246.0,123000000000000000000\r\n'
           '1,16,af6e0003,account,123.0,246.0,123000000000000000000\r\n')
    test_case.assertEqual(csv, result.data.decode('utf-8'))


def list_addresses(test_case):
    result = service.list_addresses('btc', pagesize=2)
    test_case.assertEqual([addressD, address],
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
    test_case.assertEqual([eth_address, eth_address2, eth_address3],
                          result.addresses)
    test_case.assertIs(result.next_page, None)

    ids = [eth_address2.address, 'aaaa']

    result = service.list_addresses('eth', ids=ids)
    test_case.assertEqual([eth_address2], result.addresses)
    test_case.assertIs(result.next_page, None)


def list_addresses_csv(test_case):
    result = service.list_addresses_csv(
                "btc", [address.address]).data.decode('utf-8')
    assertEqual(3, len(result.split("\r\n")))
    result = service.list_addresses_csv(
                "eth", [eth_address.address]).data.decode('utf-8')
    assertEqual(3, len(result.split("\r\n")))
