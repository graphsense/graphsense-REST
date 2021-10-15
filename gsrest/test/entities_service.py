from gsrest.test.assertion import assertEqual
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.txs import Txs
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
import json
from gsrest.util.values import make_values
import gsrest.service.entities_service as service
from gsrest.test.addresses_service import addressD, addressE, eth_address, \
        eth_addressWithTagsOutNeighbors, atag1, atag2, eth_tag, eth_tag2
from gsrest.test.txs_service import tx1_eth, tx2_eth, tx4_eth
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


def get_entity(test_case):
    result = service.get_entity(currency='btc',
                                entity=entityWithTags.entity,
                                include_tags=True,
                                tag_coherence=True)

    # tag_coherence tested by tests/util/test_tag_coherence.py so hardcode here
    test_case.assertIsNot(result.tags.tag_coherence, None)
    result.tags.tag_coherence = 0.5
    test_case.assertEqual(entityWithTags, result)

    result = service.get_entity(currency='eth',
                                entity=eth_entity.entity,
                                include_tags=True,
                                tag_coherence=False)

    test_case.assertEqual(eth_entityWithTags, result)


def list_entities(test_case):
    result = service.list_entities(currency='btc')
    ids = [67065, 144534, 10102718, 10164852, 17642138, 2818641,
           8361735, 123, 456, 789]
    test_case.assertEqual(ids.sort(),
                          [row.entity for row in result.entities].sort())

    result = service.list_entities(currency='btc', ids=[67065, 456, 42])
    ids = [67065, 456]
    test_case.assertEqual(sorted(ids),
                          sorted([row.entity for row in result.entities]))

    result = service.list_entities(currency='eth')
    test_case.assertEqual([107925000, 107925001, 107925002],
                          sorted([row.entity for row in result.entities]))

    result = service.list_entities(currency='eth', ids=[107925000])
    test_case.assertEqual([eth_entity],
                          result.entities)

    ids = [144534, 10102718]
    query_string = [('ids', ','.join([str(id) for id in ids]))]
    headers = {
        'Accept': 'application/json',
    }
    response = test_case.client.open(
        '/{currency}/entities'.format(
            currency="btc"),
        method='GET',
        headers=headers,
        query_string=query_string)
    test_case.assert200(response,
                        'Response body is : ' + response.data.decode('utf-8'))

    result = json.loads(response.data.decode('utf-8'))

    assertEqual(
        ids,
        [n['entity'] for n in result['entities']]
    )


def list_entities_csv(test_case):
    result = service.list_entities_csv(
                "btc", [456, 67065]).data.decode('utf-8')
    assertEqual(4, len(result.split("\r\n")))
    result = service.list_entities_csv(
                "eth", [eth_entity.entity]).data.decode('utf-8')
    assertEqual(3, len(result.split("\r\n")))


def list_tags_by_entity(test_case):
    result = service.list_tags_by_entity(currency='btc',
                                         entity=entityWithTags.entity,
                                         tag_coherence=False)
    result.tag_coherence = 0.5
    test_case.assertEqual(entityWithTags.tags, result)
    result = service.list_tags_by_entity(currency='eth',
                                         entity=eth_entityWithTags.entity,
                                         tag_coherence=False)
    test_case.assertEqual(eth_entityWithTags.tags, result)


def list_tags_by_entity_by_level_csv(test_case):
    csv = ("abuse,active,category,currency,entity,label,lastmod,source,"
           "tagpack_uri\r\n"
           ",True,organization,btc,17642138,"
           "Internet Archive 2,1560290400,https://archive.org/donate/crypto"
           "currency,http://tagpack_uri\r\n"
           ",True,"
           "organization,btc,17642138,\"Internet, Archive\",1560290400,"
           "https://archive.org/donate/cryptocurrency,http://tagpack_uri\r\n"
           )
    assertEqual(
        csv,
        service.list_tags_by_entity_by_level_csv(
            "btc", entityWithTags.entity, 'entity')
        .data.decode('utf-8'))


def list_entity_neighbors(test_case):
    result = service.list_entity_neighbors(
        currency='btc',
        entity=entityWithTags.entity,
        include_labels=True,
        direction='out')
    test_case.assertEqual(entityWithTagsOutNeighbors, result)

    result = service.list_entity_neighbors(
        currency='btc',
        entity=entityWithTags.entity,
        include_labels=True,
        direction='in')
    test_case.assertEqual(entityWithTagsInNeighbors, result)

    result = service.list_entity_neighbors(
        currency='eth',
        entity=eth_entityWithTags.entity,
        include_labels=True,
        direction='out')
    test_case.assertEqual(eth_entityWithTagsOutNeighbors, result)

    query_string = [('direction', 'in'), ('ids', '67065,144534')]
    headers = {
        'Accept': 'application/json',
    }
    response = test_case.client.open(
        '/{currency}/entities/{entity}/neighbors'.format(
            currency="btc",
            entity="17642138"),
        method='GET',
        headers=headers,
        query_string=query_string)
    test_case.assert200(response,
                        'Response body is : ' + response.data.decode('utf-8'))

    result = json.loads(response.data.decode('utf-8'))

    assertEqual(
        [n.id for n in entityWithTagsInNeighbors.neighbors],
        [n['id'] for n in result['neighbors']]
    )

    query_string = [('direction', 'in'), ('ids', '144534')]
    headers = {
        'Accept': 'application/json',
    }
    response = test_case.client.open(
        '/{currency}/entities/{entity}/neighbors'.format(
            currency="btc",
            entity="17642138"),
        method='GET',
        headers=headers,
        query_string=query_string)
    test_case.assert200(response,
                        'Response body is : ' + response.data.decode('utf-8'))

    result = json.loads(response.data.decode('utf-8'))

    test_case.assertEqual(
        [entityWithTagsInNeighbors.neighbors[1].id],
        [n['id'] for n in result['neighbors']]
    )

    query_string = [('direction', 'out'),
                    ('ids',
                     eth_entityWithTagsOutNeighbors.neighbors[0].id)]
    headers = {
        'Accept': 'application/json',
    }
    response = test_case.client.open(
        '/{currency}/entities/{entity}/neighbors'.format(
            currency="eth",
            entity=eth_entityWithTags.entity),
        method='GET',
        headers=headers,
        query_string=query_string)
    test_case.assert200(response,
                        'Response body is : ' + response.data.decode('utf-8'))

    result = json.loads(response.data.decode('utf-8'))

    test_case.assertEqual(
        [eth_entityWithTagsOutNeighbors.neighbors[0].id],
        [n['id'] for n in result['neighbors']]
    )


def list_entity_neighbors_csv(test_case):
    csv = ("balance_eur,balance_usd,balance_value,id,labels,no_txs,"
           "node_type,received_eur,received_usd,received_value,"
           "value_eur,value_usd,value_value\r\n"
           "1.15,2.31,115422577,2818641,\"['labelX', 'labelY']\","
           "1,entity,2162085.5,2583655.0,139057689444,2411.06,"
           "3074.92,48610000000\r\n"
           "1.15,2.31,115422577,8361735,[],3,entity,2162085.5,2583655.0,"
           "139057689444,1078.04,1397.54,3375700000\r\n")
    result = service.list_entity_neighbors_csv(
        currency='btc',
        entity=entityWithTags.entity,
        direction='out',
        include_labels=True)
    test_case.assertEqual(csv, result.data.decode('utf-8'))


async def list_entity_addresses(test_case):
    result = await service.list_entity_addresses(
                    currency='btc',
                    entity=entityWithTags.entity)
    test_case.assertEqual(entityWithTagsAddresses, result)

    result = await service.list_entity_addresses(
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
        addresses=[expected]), result)


def list_entity_addresses_csv(test_case):
    result = service.list_entity_addresses_csv(
                    currency='btc',
                    entity=entityWithTags.entity
                    ).data.decode('utf-8')
    test_case.assertEqual(4, len(result.split("\r\n")))

    result = service.list_entity_addresses_csv(
                    currency='eth',
                    entity=eth_address.entity
                    ).data.decode('utf-8')
    test_case.assertEqual(3, len(result.split("\r\n")))


def search_entity_neighbors(test_case):

    # Test category matching

    category = 'MyCategory'
    result = service.search_entity_neighbors(
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='category',
                    value=[category]
                    )
    assertEqual(2818641, result.paths[0].node.entity)
    assertEqual(123, result.paths[0].paths[0].node.entity)
    assertEqual(category,
                result.paths[0].paths[0].node.tags.entity_tags[0].category)

    category = 'MyCategory'
    result = service.search_entity_neighbors(
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='in',
                    depth=2,
                    breadth=10,
                    key='category',
                    value=[category]
                    )
    assertEqual(67065, result.paths[0].node.entity)
    assertEqual(123, result.paths[0].paths[0].node.entity)
    assertEqual(category,
                result.paths[0].paths[0].node.tags.entity_tags[0].category)

    # Test addresses matching

    addresses = ['abcdefg', 'xyz1278']
    result = service.search_entity_neighbors(
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='addresses',
                    value=addresses
                    )
    assertEqual(2818641, result.paths[0].node.entity)
    assertEqual(456, result.paths[0].paths[0].node.entity)
    assertEqual(addresses, [a.address for a
                            in result.paths[0].paths[0].matching_addresses])

    result = service.search_entity_neighbors(
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='entities',
                    value=['123']
                    )
    assertEqual(2818641, result.paths[0].node.entity)
    assertEqual(123, result.paths[0].paths[0].node.entity)

    query_string = [('direction', 'out'),
                    ('key', 'addresses'),
                    ('value', ','.join(addresses)),
                    ('depth', '7')]
    headers = {
        'Accept': 'application/json',
    }
    response = test_case.client.open(
        '/{currency}/entities/{entity}/search'
        .format(currency="btc", entity=entityWithTags.entity),
        method='GET',
        headers=headers,
        query_string=query_string)

    result = json.loads(response.data.decode('utf-8'))
    assertEqual(2818641, result['paths'][0]['node']['entity'])
    assertEqual(456, result['paths'][0]['paths'][0]['node']['entity'])
    assertEqual(addresses,
                [a['address'] for a
                 in result['paths'][0]['paths'][0]['matching_addresses']])

    addresses = ['abcdefg']
    result = service.search_entity_neighbors(
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='addresses',
                    value=addresses
                    )
    assertEqual(2818641, result.paths[0].node.entity)
    assertEqual(456, result.paths[0].paths[0].node.entity)
    assertEqual(addresses, [a.address for a
                            in result.paths[0].paths[0].matching_addresses])

    addresses = ['0x234567']
    result = service.search_entity_neighbors(
                    currency='eth',
                    entity=eth_entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='addresses',
                    value=addresses
                    )
    assertEqual(107925001, result.paths[0].node.entity)
    assertEqual(107925002, result.paths[0].paths[0].node.entity)
    assertEqual(addresses, [a.address for a
                            in result.paths[0].paths[0].matching_addresses])

    # Test value matching

    result = service.search_entity_neighbors(
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='total_received',
                    value=['value', 5, 150]
                    )
    assertEqual(2818641, result.paths[0].node.entity)
    assertEqual(789, result.paths[0].paths[0].node.entity)
    assertEqual(10, result.paths[0].paths[0].node.total_received.value)

    # Test value matching

    result = service.search_entity_neighbors(
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='total_received',
                    value=['value', 5, 8]
                    )
    assertEqual(SearchResultLevel1(paths=[]), result)
    #
    # Test value matching

    result = service.search_entity_neighbors(
                    currency='btc',
                    entity=entityWithTags.entity,
                    direction='out',
                    depth=2,
                    breadth=10,
                    key='total_received',
                    value=['eur', 50, 100]
                    )
    assertEqual(2818641, result.paths[0].node.entity)
    assertEqual(789, result.paths[0].paths[0].node.entity)
    assertEqual(100.0,
                result.paths[0].paths[0].node.total_received.
                fiat_values[0].value)


def list_entity_txs(test_case):
    """Test case for list_entity_txs

    Get all transactions an entity has been involved in
    """
    rates = list_rates(currency='btc', heights=[2])
    entity_txs = Txs(
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
                            timestamp=1511153263),
                        TxAccount(
                            tx_hash="4567",
                            value=convert_value('btc', -1, rates[2]),
                            height=2,
                            timestamp=1510347492)
                        ]
                    )
    result = service.list_entity_txs('btc', 144534)
    test_case.assertEqual(entity_txs, result)

    tx2_eth_reverse = TxAccount(**copy.deepcopy(tx2_eth.to_dict()))
    tx2_eth_reverse.value.value = -tx2_eth_reverse.value.value
    for v in tx2_eth_reverse.value.fiat_values:
        v.value = -v.value
    txs = Txs(txs=[tx1_eth, tx2_eth_reverse, tx4_eth])
    result = service.list_entity_txs('eth', 107925000)
    test_case.assertEqual(txs, result)


def list_entity_txs_csv(test_case):
    result = service.list_entity_txs_csv('btc', 144534)
    test_case.assertEqual(
        'height,timestamp,tx_hash,tx_type,value_eur,value_usd,'
        'value_value\r\n'
        '2,1510347493,123456,account,0.01,0.03,'
        '1260000\r\n'
        '2,1511153263,abcdef,account,-0.01,-0.03,'
        '-1260000\r\n'
        '2,1510347492,4567,account,-0.0,-0.0,'
        '-1\r\n', result.data.decode('utf-8'))

    result = service.list_entity_txs_csv('eth', 107925000)
    test_case.assertEqual(
        'height,timestamp,tx_hash,tx_type,value_eur,value_usd,'
        'value_value\r\n'
        '1,15,af6e0000,account,123.0,246.0,123000000000000000000\r\n'
        '1,16,af6e0003,account,-123.0,-246.0,-123000000000000000000\r\n'
        '1,17,123456,account,234.0,468.0,234000000000000000000\r\n',
        result.data.decode('utf-8'))


def list_entity_links(test_case):
    result = service.list_entity_links(
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

    test_case.assertEqual(link, result)

    result = service.list_entity_links(
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

    test_case.assertEqual(link, result)

    result = service.list_entity_links(
                currency='eth',
                entity=107925000,
                neighbor=107925001)
    txs = Links(links=[tx1_eth, tx2_eth])
    test_case.assertEqual(txs, result)


def list_entity_links_csv(test_case):
    result = service.list_entity_links_csv(
                currency='btc',
                entity=144534,
                neighbor=10102718)

    csv = ('height,input_value_eur,input_value_usd,'
           'input_value_value,output_value_eur,output_value_usd,'
           'output_value_value,timestamp,tx_hash,tx_type\r\n'
           '2,-0.01,-0.03,-1260000,0.01,0.03,1260000,'
           '1511153263,abcdef,utxo\r\n')

    test_case.assertEqual(csv, result.data.decode('utf-8'))

    result = service.list_entity_links_csv(
                currency='eth',
                entity=107925000,
                neighbor=107925001)

    csv = ('height,timestamp,tx_hash,tx_type,value_eur,'
           'value_usd,value_value\r\n'
           '1,15,af6e0000,account,123.0,246.0,123000000000000000000\r\n'
           '1,16,af6e0003,account,123.0,246.0,123000000000000000000\r\n')
    test_case.assertEqual(csv, result.data.decode('utf-8'))
