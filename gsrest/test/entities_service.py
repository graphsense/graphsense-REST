from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.address_tx_utxo import AddressTxUtxo
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.neighbor_entities import NeighborEntities
from openapi_server.models.neighbor_entity import NeighborEntity
from openapi_server.models.entity_addresses import EntityAddresses
from openapi_server.models.entity import Entity
from openapi_server.models.links import Links
from openapi_server.models.link_utxo import LinkUtxo
from gsrest.util.values import make_values
from gsrest.test.addresses_service import addressD, addressE, eth_address, \
        eth_address2, entityWithTags, entity2, entity3, entity4, entity5, \
        eth_addressWithTagsOutNeighbors
import gsrest.test.tags_service as ts
from gsrest.test.txs_service import tx1_eth, tx2_eth, tx22_eth, tx4_eth
from gsrest.service.rates_service import list_rates
from gsrest.util.values import convert_value
import copy

eth_entity = Entity(
   currency="eth",
   no_outgoing_txs=eth_address.no_outgoing_txs,
   last_tx=eth_address.last_tx,
   total_spent=eth_address.total_spent,
   in_degree=eth_address.in_degree,
   no_addresses=1,
   no_address_tags=2,
   total_received=eth_address.total_received,
   no_incoming_txs=eth_address.no_incoming_txs,
   entity=107925000,
   root_address=eth_address.address,
   out_degree=eth_address.out_degree,
   first_tx=eth_address.first_tx,
   balance=eth_address.balance,
   best_address_tag=ts.eth_tag1
)

eth_entity2 = Entity(
   currency="eth",
   no_outgoing_txs=eth_address2.no_outgoing_txs,
   last_tx=eth_address2.last_tx,
   total_spent=eth_address2.total_spent,
   in_degree=eth_address2.in_degree,
   no_addresses=1,
   no_address_tags=2,
   total_received=eth_address2.total_received,
   no_incoming_txs=eth_address2.no_incoming_txs,
   entity=107925001,
   root_address=eth_address2.address,
   out_degree=eth_address2.out_degree,
   first_tx=eth_address2.first_tx,
   balance=eth_address2.balance
)

eth_neighbors = []
for n in eth_addressWithTagsOutNeighbors.neighbors:
    d = n.to_dict()
    d.pop('address')
    nn = NeighborEntity(**d)
    nn.labels = []
    eth_neighbors.append(nn)

eth_neighbors[0].entity = eth_entity
eth_neighbors[0].labels = [ts.eth_etag1.label]
eth_neighbors[1].entity = eth_entity2

eth_entityWithTagsOutNeighbors = NeighborEntities(
        next_page=None,
        neighbors=eth_neighbors)

entityWithTagsOutNeighbors = NeighborEntities(
    next_page=None,
    neighbors=[
        NeighborEntity(
          entity=entity2,
          value=make_values(
             eur=2411.06,
             usd=3074.92,
             value=48610000000
          ),
          labels=['labelX', 'labelY'],
          no_txs=1,
        ),
        NeighborEntity(
          entity=entity3,
          value=make_values(
             eur=1078.04,
             usd=1397.54,
             value=3375700000
          ),
          labels=[],
          no_txs=3,
        )])

entityWithTagsInNeighbors = NeighborEntities(
    next_page=None,
    neighbors=[
        NeighborEntity(
          entity=entity4,
          value=make_values(
             usd=0.96,
             eur=0.72,
             value=190000
          ),
          labels=[],
          no_txs=10,
        ),
        NeighborEntity(
          entity=entity5,
          value=make_values(
             eur=295.7,
             usd=404.02,
             value=50000000
          ),
          labels=[],
          no_txs=1,
        )])


entityWithTagsAddresses = EntityAddresses(
        next_page=None,
        addresses=[addressD, addressE]
        )


tag_entityA = Entity(
   currency='btc',
   no_address_tags=2,
   no_outgoing_txs=0,
   last_tx=TxSummary(
      timestamp=1434554207,
      height=1,
      tx_hash="4567"
   ),
   total_spent=make_values(
      usd=0.0,
      value=0,
      eur=0.0
   ),
   in_degree=0,
   no_addresses=2,
   total_received=make_values(
      usd=0.0,
      value=0,
      eur=0.0
   ),
   no_incoming_txs=0,
   entity=12,
   root_address="tag_addressA",
   out_degree=0,
   first_tx=TxSummary(
      timestamp=1434554207,
      height=1,
      tx_hash="4567"
   ),
   balance=make_values(eur=0.0, usd=0.0, value=0),
   best_address_tag=None
)


tag_entityB = Entity(
   currency='btc',
   no_address_tags=2,
   no_outgoing_txs=0,
   last_tx=TxSummary(
      timestamp=1434554207,
      height=1,
      tx_hash="4567"
   ),
   total_spent=make_values(
      usd=0.0,
      value=0,
      eur=0.0
   ),
   in_degree=0,
   no_addresses=2,
   total_received=make_values(
      usd=0.0,
      value=0,
      eur=0.0
   ),
   no_incoming_txs=0,
   entity=14,
   root_address="tag_addressC",
   out_degree=0,
   first_tx=TxSummary(
      timestamp=1434554207,
      height=1,
      tx_hash="4567"
   ),
   balance=make_values(eur=0.0, usd=0.0, value=0),
   best_address_tag=AddressTag(
        category=None,
        label="x",
        abuse=None,
        lastmod=2,
        source="Unspecified",
        address="tag_addressC",
        currency='BTC',
        tagpack_is_public=True,
        is_cluster_definer=True,
        confidence='ownership',
        confidence_level=100,
        tagpack_creator='x',
        tagpack_title='',
        tagpack_uri='https://tagpack_uri',
        entity=14
    )
)

tag_entityC = Entity(
   currency='btc',
   no_address_tags=3,
   no_outgoing_txs=0,
   last_tx=TxSummary(
      timestamp=1434554207,
      height=1,
      tx_hash="4567"
   ),
   total_spent=make_values(
      usd=0.0,
      value=0,
      eur=0.0
   ),
   in_degree=0,
   no_addresses=3,
   total_received=make_values(
      usd=0.0,
      value=0,
      eur=0.0
   ),
   no_incoming_txs=0,
   entity=16,
   root_address="tag_addressE",
   out_degree=0,
   first_tx=TxSummary(
      timestamp=1434554207,
      height=1,
      tx_hash="4567"
   ),
   balance=make_values(eur=0.0, usd=0.0, value=0),
   best_address_tag=AddressTag(
        category=None,
        label="x",
        abuse=None,
        lastmod=2,
        source="Unspecified",
        address="tag_addressE",
        currency='BTC',
        tagpack_is_public=True,
        is_cluster_definer=True,
        confidence='ownership',
        confidence_level=100,
        tagpack_creator='x',
        tagpack_title='',
        tagpack_uri='https://tagpack_uri',
        entity=16
    )
)

tag_entityD = Entity(
   currency='btc',
   no_address_tags=1,
   no_outgoing_txs=0,
   last_tx=TxSummary(
      timestamp=1434554207,
      height=1,
      tx_hash="4567"
   ),
   total_spent=make_values(
      usd=0.0,
      value=0,
      eur=0.0
   ),
   in_degree=0,
   no_addresses=1,
   total_received=make_values(
      usd=0.0,
      value=0,
      eur=0.0
   ),
   no_incoming_txs=0,
   entity=19,
   root_address="tag_addressH",
   out_degree=0,
   first_tx=TxSummary(
      timestamp=1434554207,
      height=1,
      tx_hash="4567"
   ),
   balance=make_values(eur=0.0, usd=0.0, value=0),
   best_address_tag=AddressTag(
        category=None,
        label="x",
        abuse=None,
        lastmod=2,
        source="Unspecified",
        address="tag_addressH",
        currency='BTC',
        tagpack_is_public=True,
        is_cluster_definer=False,
        confidence='ownership',
        confidence_level=100,
        tagpack_creator='x',
        tagpack_title='',
        tagpack_uri='https://tagpack_uri',
        entity=19
    )
)

tag_entityE = Entity(
   currency='btc',
   no_address_tags=3,
   no_outgoing_txs=0,
   last_tx=TxSummary(
      timestamp=1434554207,
      height=1,
      tx_hash="4567"
   ),
   total_spent=make_values(
      usd=0.0,
      value=0,
      eur=0.0
   ),
   in_degree=0,
   no_addresses=1,
   total_received=make_values(
      usd=0.0,
      value=0,
      eur=0.0
   ),
   no_incoming_txs=0,
   entity=20,
   root_address="tag_addressI",
   out_degree=0,
   first_tx=TxSummary(
      timestamp=1434554207,
      height=1,
      tx_hash="4567"
   ),
   balance=make_values(eur=0.0, usd=0.0, value=0),
   best_address_tag=AddressTag(
        category=None,
        label="x",
        abuse=None,
        lastmod=2,
        source="Unspecified",
        address="tag_addressI",
        currency='BTC',
        tagpack_is_public=True,
        is_cluster_definer=False,
        confidence='ownership',
        confidence_level=100,
        tagpack_creator='x',
        tagpack_title='',
        tagpack_uri='https://tagpack_uri',
        entity=20
    )
)


async def get_entity(test_case):
    path = '/{currency}/entities/{entity}'
    result = await test_case.request(path,
                                     currency='btc',
                                     entity=entityWithTags.entity)
    ewt = entityWithTags.to_dict()
    test_case.assertEqual(ewt, result)

    result = await test_case.request(path,
                                     auth='unauthorized',
                                     currency='btc',
                                     entity=entityWithTags.entity)
    ewt['no_address_tags'] = 3
    test_case.assertEqual(ewt, result)

    result = await test_case.request(path,
                                     currency='eth',
                                     entity=eth_entity.entity)

    test_case.assertEqual(eth_entity.to_dict(), result)

    # test best_address_tag:

    # a cluster with multiple addresses, none cluster definer
    #   -> no best address tag

    result = await test_case.request(path,
                                     currency='btc',
                                     entity=tag_entityA.entity)

    test_case.assertEqual(tag_entityA.to_dict(), result)

    # a cluster with multiple addresses, one cluster definer
    #   -> this one tag is best address tag

    result = await test_case.request(path,
                                     currency='btc',
                                     entity=tag_entityB.entity)

    test_case.assertEqual(tag_entityB.to_dict(), result)

    # a cluster with multiple addresses, multiple cluster definers
    #   -> the one with highest confidence

    result = await test_case.request(path,
                                     currency='btc',
                                     entity=tag_entityC.entity)

    test_case.assertEqual(tag_entityC.to_dict(), result)

    # If cluster size = 1 and there is an address tag on that single address
    #   -> the one tag is best address tag

    result = await test_case.request(path,
                                     currency='btc',
                                     entity=tag_entityD.entity)

    test_case.assertEqual(tag_entityD.to_dict(), result)

    # If cluster size = 1 and there are several address tags on that address
    #   -> the one with highest confidence

    result = await test_case.request(path,
                                     currency='btc',
                                     entity=tag_entityE.entity)

    test_case.assertEqual(tag_entityE.to_dict(), result)


async def list_address_tags_by_entity(test_case):
    path = '/{currency}/entities/{entity}/tags'
    result = await test_case.request(path,
                                     currency='btc',
                                     entity=entityWithTags.entity)
    expected = [ts.tag1, ts.tag4, ts.tag2, ts.tag3]
    test_case.assertEqual([e.to_dict() for e in expected],
                          result['address_tags'])

    result = await test_case.request(path,
                                     currency='eth',
                                     entity=eth_entity.entity)
    expected = [ts.eth_tag1, ts.eth_tag2]
    test_case.assertEqual([e.to_dict() for e in expected],
                          result['address_tags'])

    result = await test_case.request(path,
                                     auth='unauthorized',
                                     currency='eth',
                                     entity=eth_entity.entity,
                                     level='address')
    public_address_tags = [tag.to_dict() for tag in expected
                           if tag.tagpack_is_public]
    test_case.assertEqual(public_address_tags,
                          result['address_tags'])


async def list_entity_neighbors(test_case):
    basepath = '/{currency}/entities/{entity}/neighbors'\
               '?direction={direction}'
    path = basepath + '&include_labels={include_labels}'
    '''
    ewton = entityWithTagsOutNeighbors.to_dict()
    result = await test_case.request(
        path,
        currency='btc',
        entity=entityWithTags.entity,
        include_labels=True,
        direction='out')
    test_case.assertEqual(ewton, result)

    result = await test_case.request(
        path,
        auth='unauthorized',
        currency='btc',
        entity=entityWithTags.entity,
        include_labels=True,
        direction='out')
    ewton['neighbors'][0]['labels'] = ['labelX']
    ewton['neighbors'][0]['entity']['no_address_tags'] = 1
    test_case.assertEqual(ewton, result)

    result = await test_case.request(
        path,
        currency='btc',
        entity=entityWithTags.entity,
        include_labels=True,
        direction='in')
    test_case.assertEqual(entityWithTagsInNeighbors.to_dict(), result)

    '''
    result = await test_case.request(
        path,
        currency='eth',
        entity=eth_entity.entity,
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
        [n.entity.entity for n in entityWithTagsInNeighbors.neighbors],
        [n['entity']['entity'] for n in result['neighbors']]
    )

    result = await test_case.request(
        path,
        currency="btc",
        entity="17642138",
        direction='in',
        only_ids='144534'
        )

    test_case.assertEqual(
        [entityWithTagsInNeighbors.neighbors[1].entity.entity],
        [n['entity']['entity'] for n in result['neighbors']]
    )

    result = await test_case.request(
        path,
        currency="eth",
        entity=eth_entity.entity,
        direction='out',
        only_ids=eth_entityWithTagsOutNeighbors.neighbors[0].entity.entity
        )

    test_case.assertEqual(
        [eth_entityWithTagsOutNeighbors.neighbors[0].entity.entity],
        [n['entity']['entity'] for n in result['neighbors']]
    )


async def list_entity_addresses(test_case):
    path = '/{currency}/entities/{entity}/addresses'
    result = await test_case.request(path,
                                     currency='btc',
                                     entity=entityWithTags.entity)
    test_case.assertEqual(entityWithTagsAddresses.to_dict(), result)

    result = await test_case.request(path,
                                     currency='eth',
                                     entity=eth_entity.entity)

    test_case.assertEqual(EntityAddresses(
        next_page=None,
        addresses=[eth_address]).to_dict(), result)


async def search_entity_neighbors(test_case):

    # Test category matching

    path = '/{currency}/entities/{entity}/search'\
           '?direction={direction}'\
           '&key={key}'\
           '&value={value}'\
           '&depth={depth}'\
           '&breadth={breadth}'

    category = 'exchange'
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
    test_case.assertEqual(
        2818641,
        result[0]['neighbor']['entity']['entity'])
    test_case.assertEqual(
        123,
        result[0]['paths'][0]['neighbor']['entity']['entity'])
    test_case.assertEqual(
        category,
        result[0]['paths'][0]['neighbor']['entity']['best_address_tag']['category']) # noqa

    category = 'exchange'
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
    test_case.assertEqual(67065, result[0]['neighbor']['entity']['entity'])
    test_case.assertEqual(
        123,
        result[0]['paths'][0]['neighbor']['entity']['entity'])
    test_case.assertEqual(
        category,
        result[0]['paths'][0]['neighbor']['entity']['best_address_tag']['category']) # noqa

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
    test_case.assertEqual(2818641, result[0]['neighbor']['entity']['entity'])
    test_case.assertEqual(
        456,
        result[0]['paths'][0]['neighbor']['entity']['entity'])
    test_case.assertEqual(addresses,
                          [a['address'] for a in result[0]['paths'][0]
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
    test_case.assertEqual(2818641, result[0]['neighbor']['entity']['entity'])
    test_case.assertEqual(
        123,
        result[0]['paths'][0]['neighbor']['entity']['entity'])

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
    test_case.assertEqual(
        2818641,
        result[0]['neighbor']['entity']['entity'])
    test_case.assertEqual(
        456,
        result[0]['paths'][0]['neighbor']['entity']['entity'])
    test_case.assertEqual(addresses,
                          [a['address'] for a in result[0]['paths'][0]
                                                       ['matching_addresses']])

    addresses = ['0x234567']
    result = await test_case.request(
                    path,
                    currency='eth',
                    entity=eth_entity.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='addresses',
                    value=','.join(addresses)
                    )
    test_case.assertEqual(107925001, result[0]['neighbor']['entity']['entity'])
    test_case.assertEqual(
        107925002,
        result[0]['paths'][0]['neighbor']['entity']['entity'])
    test_case.assertEqual(addresses,
                          [a['address'] for a in result[0]['paths'][0]
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
    test_case.assertEqual(2818641, result[0]['neighbor']['entity']['entity'])
    test_case.assertEqual(
        789,
        result[0]['paths'][0]['neighbor']['entity']['entity'])
    test_case.assertEqual(10,
                          result[0]['paths'][0]['neighbor']
                                ['entity']['total_received']['value'])

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
    test_case.assertEqual([], result)
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
    test_case.assertEqual(2818641, result[0]['neighbor']['entity']['entity'])
    test_case.assertEqual(
        789,
        result[0]['paths'][0]['neighbor']['entity']['entity'])
    test_case.assertEqual(100.0, result[0]['paths'][0]
                                       ['neighbor']['entity']['total_received']
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
    test_case.assertEqual(2818641, result[0]['neighbor']['entity']['entity'])
    test_case.assertEqual(
        456,
        result[0]['paths'][0]['neighbor']['entity']['entity'])
    test_case.assertEqual(addresses,
                          [a['address'] for a in result[0]['paths'][0]
                                                       ['matching_addresses']])


async def list_entity_txs(test_case):
    """Test case for list_entity_txs

    Get all transactions an entity has been involved in
    """
    path = '/{currency}/entities/{entity}/txs'
    rates = await list_rates(test_case, currency='btc', heights=[2])
    txs = [AddressTxUtxo(
                tx_hash="123456",
                currency="btc",
                value=convert_value('btc', 1260000, rates[2]),
                coinbase=False,
                height=2,
                timestamp=1510347493),
           AddressTxUtxo(
                tx_hash="4567",
                currency="btc",
                value=convert_value('btc', -1, rates[2]),
                coinbase=False,
                height=2,
                timestamp=1510347492),
           AddressTxUtxo(
                tx_hash="abcdef",
                currency="btc",
                value=convert_value('btc', -1260000, rates[2]),
                coinbase=False,
                height=2,
                timestamp=1511153263)]
    entity_txs = AddressTxs(
                    next_page=None,
                    address_txs=txs
                    )
    result = await test_case.request(path, currency='btc', entity=144534)
    test_case.assertEqualWithList(entity_txs.to_dict(), result, 'address_txs',
                                  'tx_hash')

    path_with_direction =\
        '/{currency}/entities/{entity}/txs?direction={direction}'
    result = await test_case.request(path_with_direction,
                                     currency='btc',
                                     entity=144534,
                                     direction='out')
    entity_txs.address_txs = txs[1:]
    test_case.assertEqualWithList(entity_txs.to_dict(), result, 'address_txs',
                                  'tx_hash')

    result = await test_case.request(path_with_direction,
                                     currency='btc',
                                     entity=144534,
                                     direction='in')
    entity_txs.address_txs = txs[0:1]
    test_case.assertEqualWithList(entity_txs.to_dict(), result, 'address_txs',
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
    txs.address_txs = sorted(txs.address_txs, key=lambda t: t.tx_hash)
    result = await test_case.request(path, currency='eth', entity=107925000)
    result['address_txs'] = sorted(result['address_txs'],
                                   key=lambda t: t['tx_hash'])
    test_case.assertEqual(txs.to_dict(), result)


async def list_entity_links(test_case):
    path = '/{currency}/entities/{entity}/links?neighbor={neighbor}'
    result = await test_case.request(path,
                                     currency='btc',
                                     entity=144534,
                                     neighbor=10102718)
    link = Links(links=[LinkUtxo(tx_hash='abcdef',
                                 currency='btc',
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
                                 currency='btc',
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
    test_case.assertEqualWithList(txs.to_dict(), result, 'links', 'tx_hash')
