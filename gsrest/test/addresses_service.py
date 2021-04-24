from openapi_server.models.address_with_tags import AddressWithTags
from openapi_server.models.values import Values
from openapi_server.models.tag import Tag
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.entity_with_tags import EntityWithTags
from openapi_server.models.link import Link
import gsrest.service.addresses_service as service
from gsrest.test.assertion import assertEqual
from openapi_server.models.address_tx import AddressTx
from openapi_server.models.address_txs import AddressTxs
from gsrest.util.values import convert_value
from gsrest.service.rates_service import list_rates
import base64


tag = Tag(
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

tag2 = Tag(
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

eth_tag = Tag(
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

eth_tag2 = Tag(
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

addressWithTags = AddressWithTags(
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
   tags=[tag]
   )

addressWithoutTags = AddressWithTags(
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
   tags=[],
   balance=Values(eur=0.0, usd=0.0, value=0)
)

addressBech32 = AddressWithTags(
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
   tags=[],
   balance=Values(eur=0.0, usd=0.0, value=0)
)

addressWithTotalSpent0 = AddressWithTags(
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
   balance=Values(eur=0.0, usd=0.0, value=18099),
   tags=[]
   )

addressWithTagsOutNeighbors = Neighbors(
        next_page=None,
        neighbors=[
            Neighbor(
                id="17DfZja1713S3JRWA9jaebCKFM5anUh7GG",
                node_type='address',
                labels=[],
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
                labels=[],
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
                labels=[],
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
                labels=[],
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


entityWithTagsOfAddressWithTags = EntityWithTags(
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
   tags=[tag2, tag],
   tag_coherence=0
)

eth_addressWithTags = AddressWithTags(
   first_tx=TxSummary(
      tx_hash="abcdef",
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
      tx_hash="123456",
      height=1,
      timestamp=12
   ),
   address="abcdef",
   in_degree=5,
   balance=Values(eur=111.0, usd=222.0, value=11100000000),
   tags=[eth_tag, eth_tag2]
   )


def get_address_with_tags(test_case):
    """Test case for get_address_with_tags
    """
    result = service.get_address_with_tags(
            currency='btc', address=addressWithoutTags.address)
    assertEqual(addressWithoutTags, result)
    result = service.get_address_with_tags(
            currency='btc', address=addressWithTags.address)
    assertEqual(addressWithTags, result)
    result = service.get_address_with_tags(
                currency='btc', address=addressBech32.address)
    assertEqual(addressBech32, result)
    result = service.get_address_with_tags(
                currency='btc', address=addressWithTotalSpent0.address)
    assertEqual(addressWithTotalSpent0, result)

    # ETH
    result = service.get_address_with_tags(
            currency='eth', address=eth_addressWithTags.address)
    assertEqual(eth_addressWithTags, result)


def list_address_txs(test_case):
    """Test case for list_address_txs

    Get all transactions an address has been involved in
    """
    rates = list_rates(currency='btc', heights=[2])

    address_txs = AddressTxs(
                    next_page=None,
                    address_txs=[
                        AddressTx(
                            tx_hash="123456",
                            value=convert_value(1260000, rates[2]),
                            height=2,
                            address=addressWithoutTags.address,
                            timestamp=1510347493),
                        AddressTx(
                            tx_hash="abcdef",
                            value=convert_value(-1260000, rates[2]),
                            height=2,
                            address=addressWithoutTags.address,
                            timestamp=1511153263)
                        ]
                    )

    result = service.list_address_txs('btc', addressWithoutTags.address)
    assertEqual(address_txs, result)


def list_address_txs_csv(test_case):
    # result = service.list_address_txs_csv('btc', addressWithoutTags.address)
    # assertEqual('', result.data.decode('utf-8'))
    pass


def list_address_tags(test_case):
    result = service.list_address_tags('btc', addressWithTags.address)
    assertEqual(addressWithTags.tags, result)

    result = service.list_address_tags('eth', eth_addressWithTags.address)
    assertEqual(eth_addressWithTags.tags, result)


def list_address_tags_csv(test_case):
    csv = ("abuse,active,address,category,currency,label,lastmod,"
           "source,tagpack_uri\r\n,True,1Archive1n2C579dMsAu3iC6"
           "tWzuQJz8dN,organization,btc,\"Internet, Archive\",1560290400"
           ",https://archive.org/donate/cryptocurrency,http://tagpack_uri\r\n")
    csv = base64.b64encode(csv.encode("utf-8"))
    result = service.list_address_tags_csv(
                        "btc",
                        addressWithTags.address).data.decode('utf-8')
    result = base64.b64encode(result.encode("utf-8"))
    assertEqual(csv, result)


def list_address_neighbors(test_case):
    result = service.list_address_neighbors(
        currency='btc',
        address=addressWithTags.address,
        direction='out')
    assertEqual(addressWithTagsOutNeighbors, result)

    result = service.list_address_neighbors(
        currency='btc',
        address=addressWithTags.address,
        direction='in')
    assertEqual(addressWithTagsInNeighbors, result)


def list_address_neighbors_csv(test_case):
    csv = ("balance_eur,balance_usd,balance_value,estimated_value_eur,"
           "estimated_value_usd,estimated_value_value,id,labels,no_txs,"
           "node_type,received_eur,received_usd,received_value\r\n0.0,0.0,"
           "0,72.08,87.24,27789282,17DfZja1713S3JRWA9jaebCKFM5anUh7GG,[]"
           ",1,address,114.86,142.18,87789282\r\n0.0,0.0,0,72.08,87.24,"
           "27789282,1LpXFVskUaE2cs5xkQE5bDDaX8hff4L2Ej,[],1,address,98.72,"
           "121.46,67789282\r\n")
    result = service.list_address_neighbors_csv(
        currency='btc',
        address=addressWithTags.address,
        direction='out')
    assertEqual(csv, result.data.decode('utf-8'))


def get_address_entity(test_case):
    result = service.get_address_entity(
                currency='btc',
                address=addressWithTags.address)
    result.tags = sorted(result.tags, key=lambda t: t.label)
    result.tag_coherence = 0
    assertEqual(entityWithTagsOfAddressWithTags, result)


def list_address_links(test_case):
    result = service.list_address_links(
                currency='btc',
                address=addressWithTags.address,
                neighbor='17DfZja1713S3JRWA9jaebCKFM5anUh7GG')
    link = [Link(tx_hash='123456',
                 input_value=Values(eur=-0.1, usd=-0.2, value=-10000000),
                 output_value=Values(eur=-0.1, usd=-0.2, value=-10000000),
                 timestamp=1361497172,
                 height=2)]

    assertEqual(link, result)


def list_address_links_csv(test_case):
    '''
    result = service.list_address_links_csv(
                currency='btc',
                address=addressWithTags.address,
                neighbor='17DfZja1713S3JRWA9jaebCKFM5anUh7GG')

    assertEqual("", result.data.decode('utf-8'))
    '''
    pass
