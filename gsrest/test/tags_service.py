from openapi_server.models.address_tag import AddressTag
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.concept import Concept

tag1 = AddressTag(
    category="organization",
    label="Internet, Archive",
    abuse=None,
    lastmod=1560290400,
    source="https://archive.org/donate/cryptocurrency",
    address="addressA",
    currency='BTC',
    tagpack_uri='https://tagpack_uri',
    tagpack_is_public=True,
    is_cluster_definer=True,
    confidence='ownership',
    confidence_level=100,
    tagpack_creator='x',
    tagpack_title='',
    entity=17642138
)

tag2 = AddressTag(
    abuse=None,
    address='addressA',
    category='organization',
    currency='BTC',
    label='addressTag1',
    lastmod=1,
    source='https://archive.org/donate/cryptocurrency',
    tagpack_uri='https://tagpack_uri',
    tagpack_is_public=True,
    is_cluster_definer=False,
    confidence='forensic',
    confidence_level=50,
    tagpack_creator='x',
    tagpack_title='',
    entity=17642138
)

tag3 = AddressTag(
    category="organization",
    label="Internet Archive 2",
    abuse=None,
    lastmod=1560290400,
    source="https://archive.org/donate/cryptocurrency",
    address="addressA",
    tagpack_uri=None,
    currency='BTC',
    tagpack_is_public=False,
    is_cluster_definer=True,
    confidence='web_crawl',
    confidence_level=20,
    tagpack_creator='x',
    tagpack_title='',
    entity=17642138
)

tag4 = AddressTag(
    abuse=None,
    address='addressH',
    category='organization',
    currency='BTC',
    label='addressTag2',
    lastmod=2,
    source='https://archive.org/donate/cryptocurrency',
    tagpack_uri='https://tagpack_uri',
    tagpack_is_public=True,
    is_cluster_definer=False,
    tagpack_creator='x',
    tagpack_title='',
    confidence='ownership',
    confidence_level=100,
    entity=17642138
)

eth_tag1 = AddressTag(
    category=None,
    label="TagA",
    abuse=None,
    lastmod=1,
    source="sourceX",
    address="0xabcdef",
    tagpack_uri=None,
    currency='ETH',
    tagpack_is_public=False,
    is_cluster_definer=True,
    confidence='ownership',
    confidence_level=100,
    tagpack_creator='x',
    tagpack_title='',
    entity=107925000
)

eth_tag2 = AddressTag(
    category=None,
    label="TagB",
    abuse=None,
    lastmod=1,
    source="sourceY",
    address="0xabcdef",
    currency='ETH',
    tagpack_is_public=True,
    tagpack_uri="uriY",
    is_cluster_definer=False,
    confidence='ownership',
    confidence_level=100,
    tagpack_creator='x',
    tagpack_title='',
    entity=107925000
)

etag1 = AddressTag(
    category=tag1.category,
    label=tag1.label,
    abuse=tag1.abuse,
    lastmod=tag1.lastmod,
    source=tag1.source,
    address=tag1.address,
    tagpack_uri=tag1.tagpack_uri,
    currency=tag1.currency,
    confidence=tag1.confidence,
    confidence_level=tag1.confidence_level,
    tagpack_creator=tag1.tagpack_creator,
    tagpack_title=tag1.tagpack_title,
    is_cluster_definer=True,
    tagpack_is_public=tag1.tagpack_is_public
)

etag2 = AddressTag(
    tagpack_uri="https://tagpack_uri",
    lastmod=1,
    label="isolinks",
    source="Unspecified",
    category='exchange',
    currency="BTC",
    address="addressX",
    abuse=None,
    confidence=tag1.confidence,
    confidence_level=tag1.confidence_level,
    tagpack_is_public=True,
    is_cluster_definer=True
)

tag5 = AddressTag(
    tagpack_uri="https://tagpack_uri",
    lastmod=1,
    label="isolinks",
    source="Unspecified",
    category='exchange',
    currency="BTC",
    address="addressX",
    abuse=None,
    confidence='ownership',
    confidence_level=100,
    tagpack_creator='x',
    tagpack_title='',
    tagpack_is_public=True,
    is_cluster_definer=True,
    entity=123
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
    confidence='ownership',
    confidence_level=100,
    tagpack_creator='x',
    tagpack_title='',
    tagpack_is_public=True,
    is_cluster_definer=False,
    entity=456
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
    confidence='ownership',
    confidence_level=100,
    tagpack_creator='x',
    tagpack_title='',
    tagpack_is_public=True,
    is_cluster_definer=False,
    entity=1234
)

tag8 = AddressTag(
    category="organization",
    label="labelX",
    abuse=None,
    lastmod=1560290400,
    source="https://source",
    address="address2818641",
    currency='BTC',
    tagpack_is_public=True,
    is_cluster_definer=True,
    confidence='ownership',
    confidence_level=100,
    tagpack_creator='x',
    tagpack_title='',
    entity=2818641
)

eth_tag3 = AddressTag(
    lastmod=1,
    source="sourceX",
    abuse=None,
    address="0xabcdef",
    category=None,
    tagpack_uri=None,
    currency="ETH",
    label="TagA",
    tagpack_is_public=False,
    is_cluster_definer=True,
    confidence='ownership',
    confidence_level=100,
    tagpack_creator='x',
    tagpack_title='',
    entity=107925000
)

eth_etag1 = eth_tag1.to_dict()
eth_etag1 = AddressTag(**eth_etag1)

etag4 = AddressTag(
    category=tag2.category,
    label=tag2.label,
    abuse=tag2.abuse,
    lastmod=tag2.lastmod,
    source=tag2.source,
    address=tag2.address,
    tagpack_uri=tag2.tagpack_uri,
    currency=tag2.currency,
    is_cluster_definer=True,
    tagpack_is_public=tag2.tagpack_is_public
)


async def list_address_tags(test_case):
    path = '/tags?label={label}'
    result = await test_case.request(path, label='isolinks')
    t1 = tag5.to_dict()
    t2 = {**t1}
    t2['address'] = 'addressY'
    t2.pop('category')
    t2.pop('tagpack_uri')
    t2['tagpack_is_public'] = False
    t2['entity'] = 456
    test_case.assertEqual(
        [t1, t2],
        result['address_tags'])

    result = await test_case.request(path, auth='unauthorized',
                                     label='isolinks')
    test_case.assertEqual(
        [t1],
        result['address_tags'])

    result = await test_case.request(path, label='cimedy')
    test_case.assertEqual([tag6.to_dict(), tag7.to_dict()],
                          result['address_tags'])

    # test paging

    path_with_page = path + '&pagesize={pagesize}'
    result = await test_case.request(path_with_page,
                                     label='isolinks',
                                     pagesize=1,
                                     page=None)
    test_case.assertEqual(
        [t1],
        result['address_tags'])
    path_with_page += '&page={page}'
    result = await test_case.request(path_with_page,
                                     label='isolinks',
                                     pagesize=1,
                                     page=result['next_page'])
    test_case.assertEqual(
        [t2],
        result['address_tags'])
    result = await test_case.request(path_with_page,
                                     label='isolinks',
                                     pagesize=1,
                                     page=result['next_page'])
    test_case.assertEqual(AddressTags(address_tags=[]).to_dict(), result)

    result = await test_case.request(path, label='TagA')
    test_case.assertEqual([eth_tag3.to_dict()],
                          result['address_tags'])


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
