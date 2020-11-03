from gsrest.test.assertion import assertEqual
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.entity_with_tags import EntityWithTags
from openapi_server.models.values import Values
from openapi_server.models.tag import Tag
import gsrest.service.entities_service as service

tag = Tag(
           category="organization",
           label="Internet Archive",
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
   tags=[tag, tag2],
   tag_coherence=0.9411764705882353
)

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
          labels=[],
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
          labels=[],
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
          labels=[],
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
          labels=[],
          no_txs=1,
          balance=Values(
             eur=0.0,
             usd=0.0,
             value=0
          )
        )])

def get_entity_with_tags(test_case):
    result = service.get_entity_with_tags(currency='btc', entity=17642138)
    assertEqual(entityWithTags, result)


def list_entity_tags(test_case):
    result = service.list_entity_tags(currency='btc', entity=17642138)
    assertEqual([tag, tag2], result)


def list_entity_tags_csv(test_case):
    csv = "abuse,active,address,category,currency,label,lastmod,source,tagpack_uri\nNone,True,1Archive1n2C579dMsAu3iC6tWzuQJz8dN,organization,btc,Internet Archive,1560290400,https://archive.org/donate/cryptocurrency,http://tagpack_uri\nNone,True,1Archive1n2C579dMsAu3iC6tWzuQJz8dN,organization,btc,Internet Archive 2,1560290400,https://archive.org/donate/cryptocurrency,http://tagpack_uri\n"
    assertEqual(csv, service.list_entity_tags_csv(
                        "btc",
                        entityWithTags.entity).data.decode('utf-8'))


def list_entity_neighbors(test_case):
    result = service.list_entity_neighbors(
        currency='btc',
        entity=entityWithTags.entity,
        direction='out')
    assertEqual(entityWithTagsOutNeighbors, result)

    result = service.list_entity_neighbors(
        currency='btc',
        entity=entityWithTags.entity,
        direction='in')
    assertEqual(entityWithTagsInNeighbors, result)


def list_entity_neighbors_csv(test_case):
    csv = "balance_eur,balance_usd,balance_value,estimated_value_eur,estimated_value_usd,estimated_value_value,id,labels,no_txs,node_type,received_eur,received_usd,received_value\n0.0,0.0,0,2411.06,3074.92,48610000000,2818641,[],1,entity,2411.06,3074.92,48610000000\n0.0,0.0,0,1078.04,1397.54,3375700000,8361735,[],3,entity,7064.18,8517.93,7858798000\n"
    result = service.list_entity_neighbors_csv(
        currency='btc',
        entity=entityWithTags.entity,
        direction='out')
    assertEqual(csv, result.data.decode('utf-8'))
