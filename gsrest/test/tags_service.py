from gsrest.test.assertion import assertEqual
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.tags import Tags
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.concept import Concept
import gsrest.service.tags_service as service

tag1 = AddressTag(
   tagpack_uri="https://tagpack_uri",
   lastmod=1,
   label="isolinks",
   source="Unspecified",
   category=None,
   active=True,
   currency="BTC",
   address="addressX",
   abuse=None
        )

tag2 = AddressTag(
   lastmod=2,
   source="Unspecified",
   abuse=None,
   address="addressY",
   category=None,
   tagpack_uri="https://tagpack_uri",
   currency="BTC",
   label="cimedy",
   active=True
        )

tag3 = AddressTag(
   lastmod=3,
   source="source",
   abuse=None,
   address="addressA",
   category="exchange",
   tagpack_uri="https://tagpack_uri",
   currency="LTC",
   label="cimedy",
   active=True
        )


def list_tags(test_case):
    result = service.list_tags(currency='btc', label='isolinks')
    assertEqual(Tags(address_tags=[tag1], entity_tags=[]), result)
    result = service.list_tags(currency='btc', label='cimedy')
    assertEqual(Tags([tag2], entity_tags=[]), result)
    result = service.list_tags(label='cimedy')
    result.address_tags.sort(key=lambda x: x.currency)
    assertEqual(Tags([tag2, tag3], entity_tags=[]),
                result)


conceptA = Concept(
   uri="https://conceptA",
   id="conceptA",
   taxonomy="taxo1",
   label="Concept A",
   description="A concept A."
)

conceptB = Concept(
   uri="https://conceptB",
   id="conceptB",
   taxonomy="taxo2",
   label="Concept B",
   description="A concept B."
)

taxonomies = [
        Taxonomy(taxonomy="taxo1", uri="https://taxo1"),
        Taxonomy(taxonomy="taxo2", uri="https://taxo2"),
        ]


def list_concepts(test_case):
    result = service.list_concepts('taxo1')
    assertEqual([conceptA], result)
    result = service.list_concepts('taxo2')
    assertEqual([conceptB], result)


def list_taxonomies(test_case):
    result = service.list_taxonomies()
    assertEqual(taxonomies, result)
