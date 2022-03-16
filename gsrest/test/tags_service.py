from openapi_server.models.address_tag import AddressTag
from openapi_server.models.entity_tag import EntityTag
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.entity_tags import EntityTags
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.concept import Concept

tag1 = AddressTag(
    category="organization",
    label="Internet, Archive",
    abuse=None,
    lastmod=1560290400,
    source="https://archive.org/donate/cryptocurrency",
    address="addressA",
    tagpack_uri="https://tagpack_uri",
    active=True,
    currency='BTC',
    is_public=True,
    is_cluster_definer=True
)

tag2 = AddressTag(
    category="organization",
    label="Internet Archive 2",
    abuse=None,
    lastmod=1560290400,
    source="https://archive.org/donate/cryptocurrency",
    address="addressA",
    tagpack_uri="https://tagpack_uri_private",
    active=True,
    currency='BTC',
    is_public=False,
    is_cluster_definer=True
)

tag3 = AddressTag(
    abuse=None,
    active=True,
    address='addressA',
    category='organization',
    currency='BTC',
    label='addressTag1',
    lastmod=1,
    source='https://archive.org/donate/cryptocurrency',
    tagpack_uri='https://tagpack_uri',
    is_public=True,
    is_cluster_definer=False
)

tag4 = AddressTag(
    abuse=None,
    active=True,
    address='addressH',
    category='organization',
    currency='BTC',
    label='addressTag2',
    lastmod=2,
    source='https://archive.org/donate/cryptocurrency',
    tagpack_uri='https://tagpack_uri',
    is_public=True,
    is_cluster_definer=False
)

eth_tag1 = AddressTag(
    category=None,
    label="TagA",
    abuse=None,
    lastmod=1,
    source="sourceX",
    address="0xabcdef",
    tagpack_uri="uriX",
    active=True,
    currency='ETH',
    is_public=False,
    is_cluster_definer=True
)

eth_tag2 = AddressTag(
    category=None,
    label="TagB",
    abuse=None,
    lastmod=1,
    source="sourceY",
    address="0xabcdef",
    tagpack_uri="uriY",
    active=True,
    currency='ETH',
    is_public=True,
    is_cluster_definer=False
)

etag1 = EntityTag(
    category=tag1.category,
    label=tag1.label,
    abuse=tag1.abuse,
    lastmod=tag1.lastmod,
    source=tag1.source,
    entity=17642138,
    address=tag1.address,
    tagpack_uri=tag1.tagpack_uri,
    active=tag1.active,
    currency=tag1.currency,
    is_cluster_definer=True,
    is_public=tag1.is_public
)

etag2 = EntityTag(
    tagpack_uri="https://tagpack_uri",
    lastmod=1,
    label="isolinks",
    source="Unspecified",
    category='exchange',
    active=True,
    currency="BTC",
    entity=123,
    address="addressX",
    abuse=None,
    is_public=True,
    is_cluster_definer=True
)

tag5 = AddressTag(
    tagpack_uri="https://tagpack_uri",
    lastmod=1,
    label="isolinks",
    source="Unspecified",
    category='exchange',
    active=True,
    currency="BTC",
    address="addressX",
    abuse=None,
    is_public=True,
    is_cluster_definer=True
)

tag6 = AddressTag(
    lastmod=2,
    source="Unspecified",
    abuse=None,
    address="addressY",
    category=None,
    tagpack_uri="https://tagpack_uri",
    currency="BTC",
    label="cimedy",
    active=True,
    is_public=True,
    is_cluster_definer=False
)

tag7 = AddressTag(
    lastmod=3,
    source="source",
    abuse=None,
    address="addressA",
    category="exchange",
    tagpack_uri="https://tagpack_uri",
    currency="LTC",
    label="cimedy",
    active=True,
    is_public=True,
    is_cluster_definer=False
)

eth_tag3 = AddressTag(
    lastmod=1,
    source="sourceX",
    abuse=None,
    address="0xabcdef",
    category=None,
    tagpack_uri="uriX",
    currency="ETH",
    label="TagA",
    active=True,
    is_public=False,
    is_cluster_definer=True
)

eth_etag1 = eth_tag1.to_dict()
eth_etag1['entity'] = 107925000
eth_etag1 = EntityTag(**eth_etag1)

etag4 = EntityTag(
    category=tag2.category,
    label=tag2.label,
    abuse=tag2.abuse,
    lastmod=tag2.lastmod,
    source=tag2.source,
    entity=17642138,
    address=tag2.address,
    tagpack_uri=tag2.tagpack_uri,
    active=tag2.active,
    currency=tag2.currency,
    is_cluster_definer=True,
    is_public=tag2.is_public
)


async def list_tags(test_case):
    path = '/{currency}/tags?label={label}&level={level}'
    result = await test_case.request(path, currency='btc', label='isolinks',
                                     level='address')
    t1 = tag5.to_dict()
    t2 = {**t1}
    t2['address'] = 'addressY'
    t2.pop('category')
    t2['tagpack_uri'] = 'https://tagpack_uri_private'
    t2['is_public'] = False
    test_case.assertEqual(
        [t1, t2],
        result['address_tags'])

    result = await test_case.request(path, currency='btc', auth='unauthorized',
                                     label='isolinks', level='address')
    test_case.assertEqual(
        [t1],
        result['address_tags'])

    result = await test_case.request(path, currency='btc', label='cimedy',
                                     level='address')
    test_case.assertEqual([tag6.to_dict()], result['address_tags'])

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
        [etag2.to_dict()],
        result['entity_tags'])

    result = await test_case.request(path, currency='btc', label='cimedy',
                                     level='entity')
    test_case.assertEqual(EntityTags(entity_tags=[]).to_dict(), result)

    result = await test_case.request(path, currency='eth', label='TagA',
                                     level='address')
    test_case.assertEqual([eth_tag3.to_dict()],
                          result['address_tags'])

    result = await test_case.request(path, currency='eth', label='TagA',
                                     level='entity')
    test_case.assertEqual([eth_etag1.to_dict()], result['entity_tags'])

    result = await test_case.request(path, currency='ltc', label='cimedy',
                                     level='address')
    test_case.assertEqual([tag7.to_dict()], result['address_tags'])
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
