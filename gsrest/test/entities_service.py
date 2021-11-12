from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.address_tx_utxo import AddressTxUtxo
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.address import Address
from openapi_server.models.entity_addresses import EntityAddresses
from openapi_server.models.entity import Entity
from openapi_server.models.search_result_level1 import SearchResultLevel1
from openapi_server.models.entity_tag import EntityTag
from openapi_server.models.links import Links
from openapi_server.models.link_utxo import LinkUtxo
from openapi_server.models.tags import Tags
from gsrest.util.values import make_values
from gsrest.test.addresses_service import addressD, addressE, eth_address, \
        eth_addressWithTagsOutNeighbors, atag1, atag2, eth_tag, eth_tag2
from gsrest.test.txs_service import tx1_eth, tx2_eth, tx22_eth, tx4_eth
from gsrest.service.rates_service import list_rates
from gsrest.util.values import convert_value
import copy

tag = EntityTag(
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

tag2 = EntityTag(
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
       entity_tags=[tag2, tag],
       address_tags=[atag2, atag1],
       tag_coherence=0.5)
)

eth_entity = Entity(
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
   balance=eth_address.balance
)

eth_entityWithTags = Entity(**eth_entity.to_dict())
eth_entityWithTags.tags = Tags(address_tags=[eth_tag, eth_tag2],
                               entity_tags=[])

eth_neighbors = []
for n in eth_addressWithTagsOutNeighbors.neighbors:
    nn = Neighbor(**n.to_dict())
    nn.node_type = 'entity'
    eth_neighbors.append(nn)

eth_neighbors[0].id = '107925000'
eth_neighbors[1].id = '107925001'

eth_entityWithTagsOutNeighbors = Neighbors(
        next_page=None,
        neighbors=eth_neighbors)

entityWithTagsOutNeighbors = Neighbors(
    next_page=None,
    neighbors=[
        Neighbor(
          received=make_values(
             usd=2583655.0,
             eur=2162085.5,
             value=139057689444
          ),
          value=make_values(
             eur=2411.06,
             usd=3074.92,
             value=48610000000
          ),
          id='2818641',
          node_type='entity',
          labels=['labelX', 'labelY'],
          no_txs=1,
          balance=make_values(
             value=115422577,
             usd=2.31,
             eur=1.15,
          )
        ),
        Neighbor(
          received=make_values(
             usd=2583655.0,
             eur=2162085.5,
             value=139057689444
          ),
          value=make_values(
             eur=1078.04,
             usd=1397.54,
             value=3375700000
          ),
          id='8361735',
          node_type='entity',
          labels=[],
          no_txs=3,
          balance=make_values(
             value=115422577,
             usd=2.31,
             eur=1.15,
          )
        )])

entityWithTagsInNeighbors = Neighbors(
    next_page=None,
    neighbors=[
        Neighbor(
          received=make_values(
             usd=200.0,
             eur=100.0,
             value=10
          ),
          value=make_values(
             usd=0.96,
             eur=0.72,
             value=190000
          ),
          id='67065',
          node_type='entity',
          labels=[],
          no_txs=10,
          balance=make_values(
             eur=0.0,
             usd=0.0,
             value=5
          )
        ),
        Neighbor(
          received=make_values(
             usd=13.41,
             eur=9.87,
             value=5000000000
          ),
          value=make_values(
             eur=295.7,
             usd=404.02,
             value=50000000
          ),
          id='144534',
          node_type='entity',
          labels=[],
          no_txs=1,
          balance=make_values(
             eur=0.0,
             usd=0.0,
             value=0
          )
        )])


entityWithTagsAddresses = EntityAddresses(
        next_page=None,
        addresses=[addressD, addressE]
        )


async def get_entity(test_case):
    path = '/{currency}/entities/{entity}'\
           '?include_tags={include_tags}&tag_coherence={tag_coherence}'
    result = await test_case.request(path,
                                     currency='btc',
                                     entity=entityWithTags.entity,
                                     include_tags=True,
                                     tag_coherence=True)

    # tag_coherence tested by tests/util/test_tag_coherence.py so hardcode here
    test_case.assertIsNot(result['tags']['tag_coherence'], None)
    result['tags']['tag_coherence'] = 0.5
    test_case.assertEqual(entityWithTags.to_dict(), result)

    result = await test_case.request(path,
                                     currency='eth',
                                     entity=eth_entity.entity,
                                     include_tags=True,
                                     tag_coherence=False)

    test_case.assertEqual(eth_entityWithTags.to_dict(), result)


async def list_tags_by_entity(test_case):
    path = '/{currency}/entities/{entity}/tags'
    result = await test_case.request(path,
                                     currency='btc',
                                     entity=entityWithTags.entity,
                                     tag_coherence=False)
    result['tag_coherence'] = 0.5
    test_case.assertEqual(entityWithTags.tags.to_dict(), result)
    result = await test_case.request(path,
                                     currency='eth',
                                     entity=eth_entityWithTags.entity,
                                     tag_coherence=False)
    test_case.assertEqual(eth_entityWithTags.tags.to_dict(),
                          result)


async def list_entity_neighbors(test_case):
    basepath = '/{currency}/entities/{entity}/neighbors'\
               '?direction={direction}'
    path = basepath + '&include_labels={include_labels}'
    result = await test_case.request(
        path,
        currency='btc',
        entity=entityWithTags.entity,
        include_labels=True,
        direction='out')
    test_case.assertEqual(entityWithTagsOutNeighbors.to_dict(), result)

    result = await test_case.request(
        path,
        currency='btc',
        entity=entityWithTags.entity,
        include_labels=True,
        direction='in')
    test_case.assertEqual(entityWithTagsInNeighbors.to_dict(), result)

    result = await test_case.request(
        path,
        currency='eth',
        entity=eth_entityWithTags.entity,
        include_labels=True,
        direction='out')
    test_case.assertEqual(eth_entityWithTagsOutNeighbors.to_dict(), result)

    path = basepath + '&only_ids={only_ids}'
    result = await test_case.request(
        path,
        currency="btc",
        entity="17642138",
        direction='in',
        only_ids='67065,144534'
        )

    test_case.assertEqual(
        [n.id for n in entityWithTagsInNeighbors.neighbors],
        [n['id'] for n in result['neighbors']]
    )

    result = await test_case.request(
        path,
        currency="btc",
        entity="17642138",
        direction='in',
        only_ids='144534'
        )

    test_case.assertEqual(
        [entityWithTagsInNeighbors.neighbors[1].id],
        [n['id'] for n in result['neighbors']]
    )

    result = await test_case.request(
        path,
        currency="eth",
        entity=eth_entityWithTags.entity,
        direction='out',
        only_ids=eth_entityWithTagsOutNeighbors.neighbors[0].id
        )

    test_case.assertEqual(
        [eth_entityWithTagsOutNeighbors.neighbors[0].id],
        [n['id'] for n in result['neighbors']]
    )


async def list_entity_addresses(test_case):
    path = '/{currency}/entities/{entity}/addresses'
    result = await test_case.request(path,
                                     currency='btc',
                                     entity=entityWithTags.entity)
    test_case.assertEqual(entityWithTagsAddresses.to_dict(), result)

    result = await test_case.request(path,
                                     currency='eth',
                                     entity=eth_entityWithTags.entity)
    expected = Address(
            address=eth_address.address,
            entity=eth_entityWithTags.entity,
            first_tx=eth_address.first_tx,
            last_tx=eth_address.last_tx,
            no_incoming_txs=eth_address.no_incoming_txs,
            no_outgoing_txs=eth_address.no_outgoing_txs,
            total_received=eth_address.total_received,
            total_spent=eth_address.total_spent,
            in_degree=eth_address.in_degree,
            out_degree=eth_address.out_degree,
            balance=eth_address.balance
            )

    test_case.assertEqual(EntityAddresses(
        next_page=None,
        addresses=[expected]).to_dict(), result)


async def search_entity_neighbors(test_case):

    # Test category matching

    path = '/{currency}/entities/{entity}/search'\
           '?direction={direction}'\
           '&key={key}'\
           '&value={value}'\
           '&depth={depth}'\
           '&breadth={breadth}'

    category = 'MyCategory'
    result = await test_case.request(
                    path,
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='category',
                    value=','.join([category])
                    )
    test_case.assertEqual(2818641, result['paths'][0]['node']['entity'])
    test_case.assertEqual(123,
                          result['paths'][0]['paths'][0]['node']['entity'])
    test_case.assertEqual(
        category,
        result['paths'][0]['paths'][0]['node']['tags']['entity_tags'][0]
              ['category'])

    category = 'MyCategory'
    result = await test_case.request(
                    path,
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='in',
                    depth=2,
                    breadth=10,
                    key='category',
                    value=','.join([category])
                    )
    test_case.assertEqual(67065, result['paths'][0]['node']['entity'])
    test_case.assertEqual(123,
                          result['paths'][0]['paths'][0]['node']['entity'])
    test_case.assertEqual(category,
                          result['paths'][0]['paths'][0]['node']['tags']
                                ['entity_tags'][0]['category'])

    # Test addresses matching

    addresses = ['abcdefg', 'xyz1278']
    result = await test_case.request(
                    path,
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='addresses',
                    value=','.join(addresses)
                    )
    test_case.assertEqual(2818641, result['paths'][0]['node']['entity'])
    test_case.assertEqual(456,
                          result['paths'][0]['paths'][0]['node']['entity'])
    test_case.assertEqual(addresses,
                          [a['address'] for a in result['paths'][0]['paths'][0]
                                                       ['matching_addresses']])

    result = await test_case.request(
                    path,
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='entities',
                    value=','.join(['123'])
                    )
    test_case.assertEqual(2818641, result['paths'][0]['node']['entity'])
    test_case.assertEqual(123,
                          result['paths'][0]['paths'][0]['node']['entity'])

    addresses = ['abcdefg']
    result = await test_case.request(
                    path,
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='addresses',
                    value=','.join(addresses)
                    )
    test_case.assertEqual(2818641,
                          result['paths'][0]['node']['entity'])
    test_case.assertEqual(456,
                          result['paths'][0]['paths'][0]['node']['entity'])
    test_case.assertEqual(addresses,
                          [a['address'] for a in result['paths'][0]['paths'][0]
                                                       ['matching_addresses']])

    addresses = ['0x234567']
    result = await test_case.request(
                    path,
                    currency='eth',
                    entity=eth_entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='addresses',
                    value=','.join(addresses)
                    )
    test_case.assertEqual(107925001, result['paths'][0]['node']['entity'])
    test_case.assertEqual(107925002,
                          result['paths'][0]['paths'][0]['node']['entity'])
    test_case.assertEqual(addresses,
                          [a['address'] for a in result['paths'][0]['paths'][0]
                                                       ['matching_addresses']])

    # Test value matching

    result = await test_case.request(
                    path,
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='total_received',
                    value=','.join(['value', '5', '150'])
                    )
    test_case.assertEqual(2818641, result['paths'][0]['node']['entity'])
    test_case.assertEqual(789,
                          result['paths'][0]['paths'][0]['node']['entity'])
    test_case.assertEqual(10,
                          result['paths'][0]['paths'][0]['node']
                                ['total_received']['value'])

    # Test value matching

    result = await test_case.request(
                    path,
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='total_received',
                    value=','.join(['value', '5', '8'])
                    )
    test_case.assertEqual(SearchResultLevel1(paths=[]).to_dict(), result)
    #
    # Test value matching

    result = await test_case.request(
                    path,
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='total_received',
                    value=','.join(['eur', '50', '100'])
                    )
    test_case.assertEqual(2818641, result['paths'][0]['node']['entity'])
    test_case.assertEqual(789,
                          result['paths'][0]['paths'][0]['node']['entity'])
    test_case.assertEqual(100.0, result['paths'][0]['paths'][0]
                                       ['node']['total_received']
                                       ['fiat_values'][0]['value'])

    addresses = ['abcdefg', 'xyz1278']
    result = await test_case.request(
                    path,
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=7,
                    breadth=10,
                    key='addresses',
                    value=','.join(addresses)
                    )
    test_case.assertEqual(2818641, result['paths'][0]['node']['entity'])
    test_case.assertEqual(456,
                          result['paths'][0]['paths'][0]['node']['entity'])
    test_case.assertEqual(addresses,
                          [a['address'] for a in result['paths'][0]['paths'][0]
                                                       ['matching_addresses']])


async def list_entity_txs(test_case):
    """Test case for list_entity_txs

    Get all transactions an entity has been involved in
    """
    path = '/{currency}/entities/{entity}/txs'
    rates = await list_rates(test_case, currency='btc', heights=[2])
    entity_txs = AddressTxs(
                    next_page=None,
                    address_txs=[
                        AddressTxUtxo(
                            tx_hash="123456",
                            value=convert_value('btc', 1260000, rates[2]),
                            coinbase=False,
                            height=2,
                            timestamp=1510347493),
                        AddressTxUtxo(
                            tx_hash="abcdef",
                            value=convert_value('btc', -1260000, rates[2]),
                            coinbase=False,
                            height=2,
                            timestamp=1511153263),
                        AddressTxUtxo(
                            tx_hash="4567",
                            value=convert_value('btc', -1, rates[2]),
                            coinbase=False,
                            height=2,
                            timestamp=1510347492)
                        ]
                    )
    result = await test_case.request(path, currency='btc', entity=144534)
    test_case.assertEqual(entity_txs.to_dict(), result)

    def reverse(tx):
        tx_r = TxAccount.from_dict(copy.deepcopy(tx.to_dict()))
        tx_r.value.value = -tx_r.value.value
        for v in tx_r.value.fiat_values:
            v.value = -v.value
        return tx_r
    tx2_eth_r = reverse(tx2_eth)
    tx22_eth_r = reverse(tx22_eth)
    txs = AddressTxs(address_txs=[tx1_eth, tx4_eth, tx2_eth_r, tx22_eth_r])
    result = await test_case.request(path, currency='eth', entity=107925000)
    test_case.assertEqual(txs.to_dict(), result)


async def list_entity_links(test_case):
    path = '/{currency}/entities/{entity}/links?neighbor={neighbor}'
    result = await test_case.request(path,
                                     currency='btc',
                                     entity=144534,
                                     neighbor=10102718)
    link = Links(links=[LinkUtxo(tx_hash='abcdef',
                                 input_value=make_values(
                                     eur=-0.01, usd=-0.03, value=-1260000),
                                 output_value=make_values(
                                     eur=0.01, usd=0.03, value=1260000),
                                 timestamp=1511153263,
                                 height=2)])
    test_case.assertEqual(link.to_dict(), result)

    result = await test_case.request(path,
                                     currency='btc',
                                     entity=10102718,
                                     neighbor=144534)
    link = Links(links=[LinkUtxo(tx_hash='123456',
                                 input_value=make_values(
                                     eur=-0.01, usd=-0.03, value=-1260000),
                                 output_value=make_values(
                                     eur=0.01, usd=0.03, value=1260000),
                                 timestamp=1510347493,
                                 height=2)])
    test_case.assertEqual(link.to_dict(), result)

    result = await test_case.request(path,
                                     currency='eth',
                                     entity=107925000,
                                     neighbor=107925001)
    txs = Links(links=[tx2_eth, tx22_eth])
    test_case.assertEqual(txs.to_dict(), result)
