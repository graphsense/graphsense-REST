from openapi_server.models.address_tag import AddressTag
from openapi_server.models.entity_tag import EntityTag
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.entity_tags import EntityTags
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.concept import Concept

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
    path = '/{currency}/tags?label={label}&level={level}'
    result = await test_case.request(path, currency='btc', label='isolinks',
                                     level='address')
    test_case.assertEqual(
        AddressTags(address_tags=[tag1]).to_dict(),
        result)
    result = await test_case.request(path, currency='btc', label='isolinks',
                                     level='entity')
    test_case.assertEqual(
        EntityTags(entity_tags=[ctag]).to_dict(),
        result)
    result = await test_case.request(path, currency='btc', label='cimedy',
                                     level='address')
    test_case.assertEqual(AddressTags([tag2]).to_dict(), result)

    result = await test_case.request(path, currency='btc', label='cimedy',
                                     level='entity')
    test_case.assertEqual(EntityTags(entity_tags=[]).to_dict(), result)

    tag_eth = AddressTag(**tag2.to_dict())
    tag_eth.currency = 'ETH'
    tag_eth.address = '0x' + tag_eth.address
    result = await test_case.request(path, currency='eth', label='cimedy',
                                     level='address')
    test_case.assertEqual(AddressTags(address_tags=[tag_eth]).to_dict(),
                          result)

    result = await test_case.request(path, currency='eth', label='cimedy',
                                     level='entity')
    test_case.assertEqual(EntityTags(entity_tags=[]).to_dict(), result)

    result = await test_case.request(path, currency='ltc', label='cimedy',
                                     level='address')
    test_case.assertEqual(AddressTags([tag3]).to_dict(), result)
    result = await test_case.request(path, currency='ltc', label='cimedy',
                                     level='entity')
    test_case.assertEqual(EntityTags(entity_tags=[]).to_dict(), result)


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


async def list_concepts(test_case):
    path = '/tags/taxonomies/{taxonomy}/concepts'
    result = await test_case.request(path, taxonomy='entity')
    test_case.assertEqual([conceptA.to_dict()], result)
    result = await test_case.request(path, taxonomy='abuse')
    test_case.assertEqual([conceptB.to_dict()], result)


async def list_taxonomies(test_case):
    result = await test_case.request('/tags/taxonomies')
    test_case.assertEqual([t.to_dict() for t in taxonomies], result)
