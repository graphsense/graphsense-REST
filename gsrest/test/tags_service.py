from openapi_server.models.address_tag import AddressTag
from openapi_server.models.entity_tag import EntityTag
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

ctag = EntityTag(
   tagpack_uri="https://tagpack_uri",
   lastmod=1,
   label="isolinks",
   source="Unspecified",
   category=None,
   active=True,
   currency="BTC",
   entity=123,
   abuse=None
        )


async def list_tags(test_case):
    result = await service.list_tags(currency='btc', label='isolinks')
    test_case.assertEqual(Tags(address_tags=[tag1], entity_tags=[ctag]),
                          result)
    result = await service.list_tags(currency='btc', label='cimedy')
    test_case.assertEqual(Tags([tag2], entity_tags=[]), result)
    result = await service.list_tags(label='cimedy')
    result.address_tags.sort(key=lambda x: x.currency)
    test_case.assertEqual(Tags([tag2, tag3], entity_tags=[]),
                          result)


conceptA = Concept(
   uri="https://conceptA",
   id="conceptA",
   taxonomy="entity",
   label="Concept A",
   description="A concept A."
)

conceptB = Concept(
   uri="https://conceptB",
   id="conceptB",
   taxonomy="abuse",
   label="Concept B",
   description="A concept B."
)

taxonomies = [
        Taxonomy(taxonomy="abuse", uri="https://abuse"),
        Taxonomy(taxonomy="entity", uri="https://entity"),
        ]


def list_concepts(test_case):
    result = service.list_concepts('entity')
    test_case.assertEqual([conceptA], result)
    result = service.list_concepts('abuse')
    test_case.assertEqual([conceptB], result)


def list_taxonomies(test_case):
    result = service.list_taxonomies()
    test_case.assertEqual(taxonomies, result)
