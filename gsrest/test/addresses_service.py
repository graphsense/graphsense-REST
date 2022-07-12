from openapi_server.models.address import Address
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.neighbor_addresses import NeighborAddresses
from openapi_server.models.neighbor_address import NeighborAddress
from openapi_server.models.entity import Entity
from openapi_server.models.link_utxo import LinkUtxo
from openapi_server.models.links import Links
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.address_tx_utxo import AddressTxUtxo
from openapi_server.models.address_txs import AddressTxs
from gsrest.util.values import convert_value
from gsrest.service.rates_service import list_rates
from gsrest.test.txs_service import tx1_eth, tx2_eth, tx22_eth, tx4_eth
from gsrest.util.values import make_values
import gsrest.test.tags_service as ts
import copy


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
addressWithTags.tags = [ts.tag1, ts.tag2, ts.tag3]


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

addressF = Address(
   address="addressF",
   entity=10164852,
   last_tx=TxSummary(
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea"
      "5b94b304d438a8225850f05b45ae5",
      height=1,
      timestamp=1361497172
   ),
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
   in_degree=5013,
   balance=make_values(eur=1.15, usd=2.31, value=115422577),
)

addressB = Address(
   address="addressB",
   entity=67065,
   first_tx=TxSummary(
      tx_hash="04d92601677d62a985310b61a301e74870fa942c"
      "8be0648e16b1db23b996a8cd",
      height=1,
      timestamp=1361497172
   ),
   last_tx=TxSummary(
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea"
      "5b94b304d438a8225850f05b45ae5",
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
   in_degree=5013,
   balance=make_values(eur=1.15, usd=2.31, value=115422577),
        )

addressD = Address(
   address="addressD",
   entity=17642138,
   first_tx=TxSummary(
      tx_hash="04d92601677d62a985310b61a301e74870fa942c"
      "8be0648e16b1db23b996a8cd",
      height=1,
      timestamp=1361497172
   ),
   last_tx=TxSummary(
      tx_hash="bd01b57a50bdee0fb34ce77f5c62a664cea"
      "5b94b304d438a8225850f05b45ae5",
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
   in_degree=5013,
   balance=make_values(eur=1.15, usd=2.31, value=115422577),
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

addressWithTagsOutNeighbors = NeighborAddresses(
        next_page=None,
        neighbors=[
            NeighborAddress(
                labels=['labelX', 'labelY'],
                no_txs=10,
                value=make_values(
                    value=27789282,
                    usd=87.24,
                    eur=72.08),
                address=addressE
                ),
            NeighborAddress(
                labels=[],
                no_txs=1,
                value=make_values(
                    value=27789282,
                    usd=87.24,
                    eur=72.08),
                address=addressF
                )])

addressWithTagsInNeighbors = NeighborAddresses(
        next_page=None,
        neighbors=[
            NeighborAddress(
                labels=[],
                no_txs=1,
                value=make_values(
                    value=1091,
                    usd=0.01,
                    eur=0.0),
                address=addressB
                ),
            NeighborAddress(
                labels=[],
                no_txs=1,
                value=make_values(
                    value=50000000,
                    usd=404.02,
                    eur=295.7),
                address=addressD
                )])


entityWithTags = Entity(
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
   root_address="addressA",
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
   best_address_tag=ts.etag1
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
eth_addressWithTags.tags = [ts.eth_tag1, ts.eth_tag2]


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

eth_addressWithTagsOutNeighbors = NeighborAddresses(
        next_page=None,
        neighbors=[
            NeighborAddress(
                labels=['TagA', 'TagB'],
                no_txs=4,
                value=make_values(
                    value=10000000000000000000,
                    usd=20.0,
                    eur=10.0),
                address=eth_address
                ),
            NeighborAddress(
                labels=['LabelX', 'LabelY'],
                no_txs=4,
                value=make_values(
                    value=10000000000000000000,
                    usd=20.0,
                    eur=10.0),
                address=eth_address2
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
   root_address=eth_address.address,
   out_degree=eth_address.out_degree,
   first_tx=eth_address.first_tx,
   balance=eth_address.balance,
   best_address_tag=ts.eth_tag1
)


async def get_address(test_case):
    """Test case for get_address
    """
    basepath = '/{currency}/addresses/{address}'
    path = basepath + '?include_tags={include_tags}'
    result = await test_case.request(path,
                                     currency='btc',
                                     address=addressWithoutTags.address,
                                     include_tags=True)
    test_case.assertEqual(addressWithoutTags.to_dict(), result)

    result = await test_case.request(path,
                                     currency='btc',
                                     address=addressWithTags.address,
                                     include_tags=True)
    awt = addressWithTags.to_dict()
    test_case.assertEqual(awt, result)
    awt_public = Address(**awt)
    awt_public.tags = [ts.tag1, ts.tag3]
    result = await test_case.request(path,
                                     currency='btc',
                                     auth='unauthorized',
                                     address=addressWithTags.address,
                                     include_tags=True)
    test_case.assertEqual(awt_public.to_dict(), result)

    result = await test_case.request(basepath,
                                     currency='btc',
                                     address=addressWithTotalSpent0.address)
    test_case.assertEqual(addressWithTotalSpent0.to_dict(), result)

    # ETH
    result = await test_case.request(basepath,
                                     currency='eth',
                                     address=eth_addressWithTags.address)
    test_case.assertEqual(eth_address.to_dict(), result)


async def list_address_txs(test_case):
    """Test case for list_address_txs

    Get all transactions an address has been involved in
    """
    path = '/{currency}/addresses/{address}/txs'
    rates = await list_rates(test_case, currency='btc', heights=[2])
    address_txs = AddressTxs(
                    next_page=None,
                    address_txs=[
                        AddressTxUtxo(
                            tx_hash="123456",
                            value=convert_value('btc', 1260000, rates[2]),
                            height=2,
                            coinbase=False,
                            timestamp=1510347493),
                        AddressTxUtxo(
                            tx_hash="abcdef",
                            value=convert_value('btc', -1260000, rates[2]),
                            height=2,
                            coinbase=False,
                            timestamp=1511153263),
                        AddressTxUtxo(
                            tx_hash="4567",
                            value=convert_value('btc', -1, rates[2]),
                            height=2,
                            coinbase=False,
                            timestamp=1510347492)
                        ]
                    )
    result = await test_case.request(path,
                                     currency='btc',
                                     address=address2.address)
    test_case.assertEqualWithList(address_txs.to_dict(), result, 'address_txs',
                                  'tx_hash')

    def reverse(tx):
        tx_r = TxAccount.from_dict(copy.deepcopy(tx.to_dict()))
        tx_r.value.value = -tx_r.value.value
        for v in tx_r.value.fiat_values:
            v.value = -v.value
        return tx_r
    tx2_eth_r = reverse(tx2_eth)
    tx22_eth_r = reverse(tx22_eth)
    txs = AddressTxs(address_txs=[tx1_eth, tx4_eth, tx2_eth_r, tx22_eth_r])
    result = await test_case.request(path,
                                     currency='eth',
                                     address=eth_address.address)
    test_case.assertEqualWithList(txs.to_dict(), result, 'address_txs',
                                  'tx_hash')


async def list_tags_by_address(test_case):
    path = '/{currency}/addresses/{address}/tags'
    result = await test_case.request(path,
                                     currency='btc',
                                     address=addressWithTags.address)   
    tags = [tag.to_dict() for tag in addressWithTags.tags]
    test_case.assertEqual(tags, result['address_tags'])

    result = await test_case.request(path,
                                     auth='unauthorized',
                                     currency='btc',
                                     address=addressWithTags.address)
    tags = [tag for tag in tags if tag['tagpack_is_public']]
    test_case.assertEqual(tags, result['address_tags'])

    result = await test_case.request(path,
                                     currency='eth',
                                     address=eth_addressWithTags.address)
    print(result)
    test_case.assertEqual([tag.to_dict()
                           for tag in eth_addressWithTags.tags],
                          result['address_tags'])


async def list_address_neighbors(test_case):
    path = '/{currency}/addresses/{address}/neighbors'\
           '?include_labels={include_labels}&direction={direction}'
    result = await test_case.request(path,
                                     currency='btc',
                                     address=address.address,
                                     include_labels=True,
                                     direction='out')
    awton = addressWithTagsOutNeighbors.to_dict()
    test_case.assertEqual(awton, result)

    result = await test_case.request(path,
                                     currency='btc',
                                     auth='unauthorized',
                                     address=address.address,
                                     include_labels=True,
                                     direction='out')
    awton['neighbors'][0]['labels'] = ['labelX']
    test_case.assertEqual(awton, result)

    result = await test_case.request(path,
                                     currency='btc',
                                     address=address.address,
                                     include_labels=True,
                                     direction='in')
    test_case.assertEqual(addressWithTagsInNeighbors.to_dict(), result)

    result = await test_case.request(path,
                                     currency='eth',
                                     address=eth_address.address,
                                     include_labels=True,
                                     direction='out')
    test_case.assertEqual(eth_addressWithTagsOutNeighbors.to_dict(), result)


async def get_address_entity(test_case):
    path = '/{currency}/addresses/{address}/entity'\
           '?include_tags={include_tags}'
    result = await test_case.request(path,
                                     currency='btc',
                                     address=address.address,
                                     include_tags=True)
    test_case.assertEqual(entityWithTags.to_dict(), result)

    result = await test_case.request(path,
                                     currency='eth',
                                     address=eth_address.address,
                                     include_tags=True)
    test_case.assertEqual(eth_entityWithTags.to_dict(), result)


async def list_address_links(test_case):
    path = '/{currency}/addresses/{address}/links'\
           '?neighbor={neighbor}'
    result = await test_case.request(path,
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

    test_case.assertEqualWithList(link.to_dict(), result, 'links', 'tx_hash')

    txs = Links(links=[tx2_eth, tx22_eth])
    result = await test_case.request(path,
                                     currency='eth',
                                     address=eth_address.address,
                                     neighbor='0x123456')

    # remember here in which order eth links are stored in db (might change
    # from ingest to ingest:
    first = result['links'][0]
    second = result['links'][1]
    test_case.assertEqualWithList(txs.to_dict(), result, 'links', 'tx_hash')

    path += '&pagesize={pagesize}'
    result = await test_case.request(path,
                                     currency='eth',
                                     address=eth_address.address,
                                     neighbor='0x123456',
                                     pagesize=1)
    txs = Links(links=[tx2_eth if first['tx_hash'] == tx2_eth.tx_hash else
                       tx22_eth])
    test_case.assertEqual([li.to_dict() for li in txs.links], result['links'])
    test_case.assertNotEqual(None, result.get('next_page', None))

    path += '&page={page}'
    result = await test_case.request(path,
                                     currency='eth',
                                     address=eth_address.address,
                                     neighbor='0x123456',
                                     page=result['next_page'],
                                     pagesize=1)
    txs = Links(links=[tx22_eth if second['tx_hash'] == tx22_eth.tx_hash else
                       tx2_eth])
    test_case.assertEqual([li.to_dict() for li in txs.links], result['links'])
    test_case.assertNotEqual(None, result.get('next_page', None))

    result = await test_case.request(path,
                                     currency='eth',
                                     address=eth_address.address,
                                     neighbor='0x123456',
                                     page=result['next_page'],
                                     pagesize=1)
    test_case.assertEqual(Links(links=[]).to_dict(), result)
