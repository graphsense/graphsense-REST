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

tag_eth = AddressTag(
   lastmod=1,
   source="sourceX",
   abuse=None,
   address="0xabcdef",
   category=None,
   tagpack_uri="uriX",
   currency="ETH",
   label="TagA",
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
    t1 = tag1.to_dict()
    t2 = {**t1}
    t2['address'] = 'addressY'
    test_case.assertEqual(
        [t1, t2],
        result['address_tags'])

    result = await test_case.request(path, currency='btc', label='cimedy',
                                     level='address')
    test_case.assertEqual([tag2.to_dict()], result['address_tags'])

    # test paging

    path_with_page = path + '&pagesize={pagesize}'
    result = await test_case.request(path_with_page, currency='btc',
                                     label='isolinks',
                                     level='address', pagesize=1,
                                     page=None)
    test_case.assertEqual(
        [t1],
        result['address_tags'])
    path_with_page += '&page={page}'
    result = await test_case.request(path_with_page, currency='btc',
                                     label='isolinks',
                                     level='address', pagesize=1,
                                     page=result['next_page'])
    test_case.assertEqual(
        [t2],
        result['address_tags'])
    result = await test_case.request(path_with_page, currency='btc',
                                     label='isolinks',
                                     level='address', pagesize=1,
                                     page=result['next_page'])
    test_case.assertEqual(AddressTags(address_tags=[]).to_dict(), result)

    # test entity tags

    result = await test_case.request(path, currency='btc', label='isolinks',
                                     level='entity')
    test_case.assertEqual(
        [ctag.to_dict()],
        result['entity_tags'])

    result = await test_case.request(path, currency='btc', label='cimedy',
                                     level='entity')
    test_case.assertEqual(EntityTags(entity_tags=[]).to_dict(), result)

    result = await test_case.request(path, currency='eth', label='TagA',
                                     level='address')
    test_case.assertEqual([tag_eth.to_dict()],
                          result['address_tags'])

    result = await test_case.request(path, currency='eth', label='TagA',
                                     level='entity')
    test_case.assertEqual(EntityTags(entity_tags=[]).to_dict(), result)

    result = await test_case.request(path, currency='ltc', label='cimedy',
                                     level='address')
    test_case.assertEqual([tag3.to_dict()], result['address_tags'])
    result = await test_case.request(path, currency='ltc', label='cimedy',
                                     level='entity')
    test_case.assertEqual(EntityTags(entity_tags=[]).to_dict(), result)


organization = Concept(
   uri="https://organization",
   id="organization",
   taxonomy="entity",
   label="An organization",
   description="An organization is foo."
)

exchange = Concept(
   uri="https://exchange",
   id="exchange",
   taxonomy="entity",
   label="An exchange",
   description="An exchange is foo."
)

conceptB = Concept(
   uri="https://conceptB",
   id="conceptB",
   taxonomy="abuse",
   label="Concept B",
   description="A concept B."
)

taxonomies = [
        Taxonomy(taxonomy="entity", uri="http://entity"),
        Taxonomy(taxonomy="abuse", uri="http://abuse")
        ]


async def list_concepts(test_case):
    path = '/tags/taxonomies/{taxonomy}/concepts'
    result = await test_case.request(path, taxonomy='entity')
    test_case.assertEqual([organization.to_dict(), exchange.to_dict()], result)
    result = await test_case.request(path, taxonomy='abuse')
    test_case.assertEqual([conceptB.to_dict()], result)


async def list_taxonomies(test_case):
    result = await test_case.request('/tags/taxonomies')
    test_case.assertEqual([t.to_dict() for t in taxonomies], result)
