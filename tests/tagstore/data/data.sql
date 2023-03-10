INSERT INTO taxonomy (id, source, description) VALUES
    ('entity', 'http://entity', 'The entity taxonomy.'),
    ('abuse', 'http://abuse', 'The abuse taxonomy.'),
    ('country', 'http://country', 'The country taxonomy.');
INSERT INTO concept (id, label, source, description, taxonomy) VALUES 
    ('organization', 'An organization', 'https://organization', 'An organization is foo.', 'entity'),
    ('exchange', 'An exchange', 'https://exchange', 'An exchange is foo.', 'entity'),
    ('conceptB', 'Concept B', 'https://conceptB', 'A concept B.', 'abuse'),
    ('AT', 'Austria', 'https://austria', 'A concept austria.', 'country'),
    ('SC', 'Singapore', 'https://singapore', 'A concept SC.', 'country'),
    ('VU', 'Vanuatu', 'https://Vanuatu', 'A concept VU.', 'country');
INSERT INTO tagpack (id, title, description, creator, is_public) VALUES
    ('https://tagpack_uri', '', '', 'x', true),
    ('https://tagpack_uri_private', '', '', 'x', false),
    ('uriX', '', '', 'x', false),
    ('uriY', '', '', 'x', true);
INSERT INTO address (currency, address) VALUES
    ('BTC', 'addressA'),
    ('BTC', 'a123456'),
    ('BTC', 'address2818641'),
    ('BTC', 'abcdefg'),
    ('BTC', 'addressE'),
    ('BTC', 'addressX'),
    ('BTC', 'addressY'),
    ('BTC', 'addressH'),
    ('LTC', 'addressA'),
    ('LTC', 'addressB'),
    ('ETH', '0xabcdef'),
    ('ETH', '0x123456'),
    ('BTC', 'tag_addressI'),
    ('BTC', 'tag_addressH'),
    ('BTC', 'tag_addressG'),
    ('BTC', 'tag_addressF'),
    ('BTC', 'tag_addressE'),
    ('BTC', 'tag_addressD'),
    ('BTC', 'tag_addressC'),
    ('BTC', 'tag_addressB'),
    ('BTC', 'tag_addressA');
INSERT INTO confidence (id, label, description, level) VALUES 
    ('ownership', 'Proven address ownership', 'Creator controls the private key the address associated with a tag', 100),
	('forensic', 'Forensic reports', 'Creator retrieved data attribution data from somehow trusted reports (e.g. academic papers)', 50),
	('web_crawl', 'Web crawls', 'Attribution tags were retrieved from crawling the web or other data dumps', 20);
INSERT INTO actorpack (id, title, creator, description, is_public, uri, lastmod) VALUES
    ('actorpack', 'ActorPack', '', '', true, '', to_timestamp(0)),
    ('actorpackprivate', 'ActorPack private', '', '', false, '', to_timestamp(0));
INSERT INTO actor (id, uri, label, lastmod, actorpack) VALUES
    ('actorX', 'http://actorX', 'Actor X', to_timestamp(0), 'actorpack'),
    ('actorY', 'http://actorY', 'Actor Y', to_timestamp(0), 'actorpackprivate'),
    ('anotherActor', 'http://anotherActor', 'Another Actor Y', to_timestamp(0), 'actorpackprivate');
INSERT INTO actor_categories (actor_id, category_id) VALUES
    ('actorX', 'exchange'),
    ('actorX', 'organization'),
    ('actorY', 'conceptB');
INSERT INTO actor_jurisdictions (actor_id, country_id) VALUES
    ('actorX', 'VU'),
    ('actorX', 'SC'),
    ('actorY', 'AT');
INSERT INTO tag (label, address, currency, category, source, tagpack, lastmod, is_cluster_definer, confidence, actor) VALUES
    ('Internet, Archive', 'addressA', 'BTC', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri', to_timestamp(1560290400), true, 'ownership', NULL),
    ('Internet Archive 2', 'addressA', 'BTC', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri_private', to_timestamp(1560290400), true, 'web_crawl', NULL),
    ('addressTag1', 'addressA', 'BTC', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri', to_timestamp(1), false, 'forensic', NULL),
    ('addressTag2', 'addressH', 'BTC', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri', to_timestamp(2), false, 'ownership', NULL),
    ('labelABC', 'a123456', 'BTC', 'exchange', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), true, 'ownership', NULL),
    ('labelX', 'address2818641', 'BTC', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), true, 'ownership', NULL),
    ('labelY', 'address2818641', 'BTC', 'organization', 'https://source', 'https://tagpack_uri_private', to_timestamp(1560290400), true, 'ownership', NULL),
    ('abcdefgLabel', 'abcdefg', 'BTC', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), false, 'ownership', 'actorX'),
    ('labelX', 'addressE', 'BTC', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), false, 'ownership', 'actorY'),
    ('labelY', 'addressE', 'BTC', 'organization', 'https://source', 'https://tagpack_uri_private', to_timestamp(1560290400), false, 'ownership', NULL),
    ('isolinks', 'addressX', 'BTC', 'exchange', 'Unspecified', 'https://tagpack_uri', to_timestamp(1), true, 'ownership', NULL),
    ('isolinks', 'addressY', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri_private', to_timestamp(1), true, 'ownership', NULL),
    ('cimedy', 'addressY', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false, 'ownership', NULL),
    ('x', 'tag_addressA', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false, 'ownership', NULL),
    ('y', 'tag_addressB', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false, 'ownership', NULL),
    ('x', 'tag_addressC', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), true, 'ownership', NULL),
    ('y', 'tag_addressD', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false, 'ownership', NULL),
    ('x', 'tag_addressE', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), true, 'ownership', NULL),
    ('y', 'tag_addressF', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), true, 'forensic', NULL),
    ('z', 'tag_addressG', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), true, 'web_crawl', NULL),
    ('x', 'tag_addressH', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false, 'ownership', NULL),
    ('x', 'tag_addressI', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false, 'ownership', NULL),
    ('y', 'tag_addressI', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false, 'ownership', NULL),
    ('z', 'tag_addressI', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false, 'ownership', NULL),
    ('cimedy', 'addressA', 'LTC', 'exchange', 'source', 'https://tagpack_uri', to_timestamp(3), false, 'ownership', NULL),
    ('coinbase', 'addressB', 'LTC', 'exchange', 'Team', 'https://tagpack_uri', to_timestamp(4), false, 'ownership', NULL),
    ('TagA', '0xabcdef', 'ETH', NULL, 'sourceX', 'uriX', to_timestamp(1), true, 'ownership', NULL),
    ('TagB', '0xabcdef', 'ETH', NULL, 'sourceY', 'uriY', to_timestamp(1), false, 'ownership', NULL),
    ('LabelX', '0x123456', 'ETH', NULL, 'sourceX', 'uriX', to_timestamp(1), false, 'ownership', 'actorX'),
    ('LabelY', '0x123456', 'ETH', NULL, 'sourceY', 'uriY', to_timestamp(1), false, 'ownership', 'actorY');
INSERT INTO address_cluster_mapping (currency, address, gs_cluster_id, gs_cluster_def_addr, gs_cluster_no_addr) VALUES
    ('BTC', 'addressX', 123, '', 10),
    ('BTC', 'addressY', 456, '', 10),
    ('BTC', 'addressA', 17642138, '', 20),
    ('BTC', 'addressH', 17642138, '', 20),
    ('BTC', 'address2818641', 2818641, '', 30),
    ('BTC', 'tag_addressA', 12, '', 2),
    ('BTC', 'tag_addressB', 12, '', 2),
    ('BTC', 'tag_addressC', 14, '', 2),
    ('BTC', 'tag_addressD', 14, '', 2),
    ('BTC', 'tag_addressE', 16, '', 3),
    ('BTC', 'tag_addressF', 16, '', 3),
    ('BTC', 'tag_addressG', 16, '', 3),
    ('BTC', 'tag_addressH', 19, '', 1),
    ('BTC', 'tag_addressI', 20, '', 1),
    ('LTC', 'addressA', 1234, '', 20),
    ('ETH', '0xabcdef', 107925000, '', 40),
    ('ETH', '0x123456', 107925001, '', 50);

REFRESH MATERIALIZED VIEW label;
REFRESH MATERIALIZED VIEW statistics;
REFRESH MATERIALIZED VIEW tag_count_by_cluster;
REFRESH MATERIALIZED VIEW cluster_defining_tags_by_frequency_and_maxconfidence;
