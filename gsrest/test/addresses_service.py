from openapi_server.models.address_with_tags import AddressWithTags
from openapi_server.models.values import Values
from openapi_server.models.tag import Tag
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
import gsrest.service.addresses_service as service
from gsrest.test.assertion import assertEqual
from openapi_server.models.address_tx import AddressTx
from openapi_server.models.address_txs import AddressTxs
from gsrest.model.common import convert_value
from gsrest.service.rates_service import list_rates

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
   tags=[Tag(
           category="organization",
           label="Internet Archive",
           abuse=None,
           lastmod=1560290400,
           source="https://archive.org/donate/cryptocurrency",
           address="1Archive1n2C579dMsAu3iC6tWzuQJz8dN",
           tagpack_uri="https://github.com/graphsense"
           "/graphsense-tagpacks/blob/develop/packs/demo.yaml",
           active=True,
           currency='btc'
        )]
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


def get_address_with_tags(test_case):
    """Test case for get_address_with_tags
    """
    result = service.get_address_with_tags(
            currency='btc', address=addressWithoutTags.address)
    assertEqual(addressWithoutTags, result)
    result = service.get_address_with_tags(
            currency='btc', address=addressWithTags.address)
    assertEqual(addressWithTags, result)


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


def list_address_tags(test_case):
    result = service.list_address_tags('btc', addressWithTags.address)
    assertEqual(addressWithTags.tags, result)


def list_address_tags_csv(test_case):
    csv = "abuse,active,address,category,currency,label,lastmod,source,tagpack_uri\nNone,True,1Archive1n2C579dMsAu3iC6tWzuQJz8dN,organization,btc,Internet Archive,1560290400,https://archive.org/donate/cryptocurrency,https://github.com/graphsense/graphsense-tagpacks/blob/develop/packs/demo.yaml\n"
    assertEqual(csv, service.list_address_tags_csv(
                        "btc",
                        addressWithTags.address).data.decode('utf-8'))


def list_address_neighbors(test_case):
    result = service.list_address_neighbors(
        currency='btc',
        address=addressWithTags.address,
        direction='out')
    assertEqual(addressWithTagsOutNeighbors, result)
