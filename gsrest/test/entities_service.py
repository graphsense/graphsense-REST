from gsrest.test.assertion import assertEqual
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.address import Address
from openapi_server.models.entity_addresses import EntityAddresses
from openapi_server.models.entity_with_tags import EntityWithTags
from openapi_server.models.values import Values
from openapi_server.models.search_paths import SearchPaths
from openapi_server.models.entity_tag import EntityTag
import json
import gsrest.service.entities_service as service
from gsrest.test.addresses_service import eth_addressWithTags, \
        eth_addressWithTagsOutNeighbors

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

entityWithTags = EntityWithTags(
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
   tag_coherence=0.5
)

eth_entityWithTags = EntityWithTags(
   no_outgoing_txs=eth_addressWithTags.no_outgoing_txs,
   last_tx=eth_addressWithTags.last_tx,
   total_spent=eth_addressWithTags.total_spent,
   in_degree=eth_addressWithTags.in_degree,
   no_addresses=1,
   total_received=eth_addressWithTags.total_received,
   no_incoming_txs=eth_addressWithTags.no_incoming_txs,
   entity=eth_addressWithTags.address + '_',
   out_degree=eth_addressWithTags.out_degree,
   first_tx=eth_addressWithTags.first_tx,
   balance=eth_addressWithTags.balance,
   tags=[],
   tag_coherence=0.5
)

eth_neighbors = []
for n in eth_addressWithTagsOutNeighbors.neighbors:
    nn = Neighbor(**n.to_dict())
    nn.id += '_'
    nn.node_type = 'entity'
    eth_neighbors.append(nn)

eth_entityWithTagsOutNeighbors = Neighbors(
        next_page=None,
        neighbors=eth_neighbors)

entityWithTagsOutNeighbors = Neighbors(
    next_page=None,
    neighbors=[
        Neighbor(
          received=Values(
             usd=3074.92,
             eur=2411.06,
             value=48610000000
          ),
          estimated_value=Values(
             eur=2411.06,
             usd=3074.92,
             value=48610000000
          ),
          id=2818641,
          node_type='entity',
          has_labels=False,
          no_txs=1,
          balance=Values(
             eur=0.0,
             usd=0.0,
             value=0
          )
        ),
        Neighbor(
          received=Values(
             usd=8517.93,
             eur=7064.18,
             value=7858798000
          ),
          estimated_value=Values(
             eur=1078.04,
             usd=1397.54,
             value=3375700000
          ),
          id=8361735,
          node_type='entity',
          has_labels=False,
          no_txs=3,
          balance=Values(
             eur=0.0,
             usd=0.0,
             value=0
          )
        )])

entityWithTagsInNeighbors = Neighbors(
    next_page=None,
    neighbors=[
        Neighbor(
          received=Values(
             usd=43253.96,
             eur=33809.55,
             value=71089119639
          ),
          estimated_value=Values(
             usd=0.96,
             eur=0.72,
             value=190000
          ),
          id=67065,
          node_type='entity',
          has_labels=False,
          no_txs=10,
          balance=Values(
             eur=0.0,
             usd=0.0,
             value=606
          )
        ),
        Neighbor(
          received=Values(
             usd=13.41,
             eur=9.87,
             value=5000000000
          ),
          estimated_value=Values(
             eur=295.7,
             usd=404.02,
             value=50000000
          ),
          id=144534,
          node_type='entity',
          has_labels=False,
          no_txs=1,
          balance=Values(
             eur=0.0,
             usd=0.0,
             value=0
          )
        )])


entityWithTagsAddresses = EntityAddresses(
        next_page=None,
        addresses=[
            Address(
               address="17gN64BPHtxi4mEM3qWrxdwhieUvRq8R2r",
               last_tx=TxSummary(
                  tx_hash="d325b684f4e6252d6bfdc83b75dc"
                  "7ea650c9463ce286b023cf4ecaf305cf44a6",
                  height=572187,
                  timestamp=1555605191
               ),
               no_outgoing_txs=35,
               balance=Values(
                  value=0,
                  eur=0.0,
                  usd=0.0
               ),
               out_degree=27,
               first_tx=TxSummary(
                  timestamp=1323298692,
                  height=156529,
                  tx_hash="dc035c562acc3230cec8c870293c1"
                  "119d62e60b13932565231dbe5c407ff7508"
               ),
               total_received=Values(
                  value=95010277876,
                  eur=16105.63,
                  usd=21341.98
               ),
               total_spent=Values(
                  value=95010277876,
                  eur=70943.62,
                  usd=95316.24
               ),
               no_incoming_txs=859,
               in_degree=1200
            ),
            Address(
               in_degree=1,
               first_tx=TxSummary(
                  timestamp=1326139563,
                  tx_hash="f73df637a912ac5f536d1e3b33695823a18a"
                  "9e89ae7f3def89d9b06d6a475a52",
                  height=161451
               ),
               total_spent=Values(
                  eur=0.2,
                  value=763736,
                  usd=0.26
               ),
               no_outgoing_txs=1,
               total_received=Values(
                  usd=0.05,
                  eur=0.04,
                  value=763736
               ),
               balance=Values(
                  usd=0.0,
                  eur=0.0,
                  value=0
               ),
               no_incoming_txs=1,
               out_degree=1,
               last_tx=TxSummary(
                  timestamp=1362160247,
                  tx_hash="c4f3c81d946d189265929212fdc76b18eabade"
                  "7ab1fb0a86a2389c18b5851878",
                  height=223777
               ),
               address="1KeDrQdATuXaZFW4CL9tfe2zpQ5SrmBFWc"
            )
            ]
        )


def get_entity_with_tags(test_case):
    result = service.get_entity_with_tags(currency='btc',
                                          entity=entityWithTags.entity)

    # tag_coherence tested by tests/util/test_tag_coherence.py so hardcode here
    result.tag_coherence = 0.5
    test_case.assertEqual(entityWithTags, result)

    result = service.get_entity_with_tags(currency='eth',
                                          entity=eth_entityWithTags.entity)

    # tag_coherence tested by tests/util/test_tag_coherence.py so hardcode here
    result.tag_coherence = 0.5
    test_case.assertEqual(eth_entityWithTags, result)


def list_tags_by_entity(test_case):
    result = service.list_tags_by_entity(currency='btc',
                                         entity=entityWithTags.entity)
    test_case.assertEqual([tag2, tag], result)
    result = service.list_tags_by_entity(currency='eth',
                                         entity=eth_entityWithTags.entity)
    test_case.assertEqual(eth_entityWithTags.tags, result)


def list_tags_by_entity_csv(test_case):
    csv = ("abuse,active,category,currency,entity,label,lastmod,source,"
           "tagpack_uri\r\n"
           ",True,organization,btc,17642138,"
           "Internet Archive 2,1560290400,https://archive.org/donate/crypto"
           "currency,http://tagpack_uri\r\n"
           ",True,"
           "organization,btc,17642138,\"Internet, Archive\",1560290400,"
           "https://archive.org/donate/cryptocurrency,http://tagpack_uri\r\n"
           )
    assertEqual(csv, service.list_tags_by_entity_csv(
                        "btc",
                        entityWithTags.entity).data.decode('utf-8'))


def list_entity_neighbors(test_case):
    result = service.list_entity_neighbors(
        currency='btc',
        entity=entityWithTags.entity,
        direction='out')
    test_case.assertEqual(entityWithTagsOutNeighbors, result)

    result = service.list_entity_neighbors(
        currency='btc',
        entity=entityWithTags.entity,
        direction='in')
    test_case.assertEqual(entityWithTagsInNeighbors, result)

    result = service.list_entity_neighbors(
        currency='eth',
        entity=eth_entityWithTags.entity,
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
        [int(n['id']) for n in result['neighbors']]
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
        [int(n['id']) for n in result['neighbors']]
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
    csv = ("balance_eur,balance_usd,balance_value,estimated_value_eur,"
           "estimated_value_usd,estimated_value_value,has_labels,id,no_txs,"
           "node_type,received_eur,received_usd,received_value\r\n0.0,0.0,0"
           ",2411.06,3074.92,48610000000,False,2818641,1,entity,2411.06,"
           "3074.92,48610000000\r\n0.0,0.0,0,1078.04,1397.54,3375700000,"
           "False,8361735,3,entity,7064.18,8517.93,7858798000\r\n")
    result = service.list_entity_neighbors_csv(
        currency='btc',
        entity=entityWithTags.entity,
        direction='out')
    assertEqual(csv, result.data.decode('utf-8'))


def list_entity_addresses(test_case):
    result = service.list_entity_addresses(
                    currency='btc',
                    entity=entityWithTags.entity)
    test_case.assertEqual(entityWithTagsAddresses, result)

    result = service.list_entity_addresses(
                    currency='eth',
                    entity=eth_entityWithTags.entity)
    expected = Address(
            address=eth_addressWithTags.address,
            first_tx=eth_addressWithTags.first_tx,
            last_tx=eth_addressWithTags.last_tx,
            no_incoming_txs=eth_addressWithTags.no_incoming_txs,
            no_outgoing_txs=eth_addressWithTags.no_outgoing_txs,
            total_received=eth_addressWithTags.total_received,
            total_spent=eth_addressWithTags.total_spent,
            in_degree=eth_addressWithTags.in_degree,
            out_degree=eth_addressWithTags.out_degree,
            balance=eth_addressWithTags.balance
            )

    assertEqual(EntityAddresses(
        next_page=None,
        addresses=[expected]), result)


def list_entity_addresses_csv(test_case):
    '''
    result = service.list_entity_addresses_csv(
                    currency='btc',
                    entity=entityWithTags.entity)
    assertEqual("", result.data.decode('utf-8'))
    '''
    pass


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
    assertEqual(category, result.paths[0].paths[0].node.tags[0].category)

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
    assertEqual(category, result.paths[0].paths[0].node.tags[0].category)

    # Test addresses matching

    addresses = ['abcdefg', 'xyz1234']
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
    assertEqual(SearchPaths(paths=[]), result)
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
    assertEqual(100.0, result.paths[0].paths[0].node.total_received.eur)
