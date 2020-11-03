from gsrest.test.assertion import assertEqual
from openapi_server.models.tx_summary import TxSummary
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


def get_entity_with_tags(test_case):
    result = service.get_entity_with_tags(currency='btc', entity_id=17642138)
    assertEqual(entityWithTags, result)


def list_entity_tags(test_case):
    result = service.list_entity_tags(currency='btc', entity_id=17642138)
    assertEqual([tag, tag2], result)


def list_entity_tags_csv(test_case):
    csv = "abuse,active,address,category,currency,label,lastmod,source,tagpack_uri\nNone,True,1Archive1n2C579dMsAu3iC6tWzuQJz8dN,organization,btc,Internet Archive,1560290400,https://archive.org/donate/cryptocurrency,http://tagpack_uri\nNone,True,1Archive1n2C579dMsAu3iC6tWzuQJz8dN,organization,btc,Internet Archive 2,1560290400,https://archive.org/donate/cryptocurrency,http://tagpack_uri\n"
    assertEqual(csv, service.list_entity_tags_csv(
                        "btc",
                        entityWithTags.entity).data.decode('utf-8'))
