INSERT INTO taxonomy (id, source, description) VALUES
    ('entity', 'http://entity', 'The entity taxonomy.'),
    ('abuse', 'http://abuse', 'The abuse taxonomy.');
INSERT INTO concept (id, label, source, description, taxonomy) VALUES 
    ('organization', 'An organization', 'https://organization', 'An organization is foo.', 'entity'),
    ('exchange', 'An exchange', 'https://exchange', 'An exchange is foo.', 'entity'),
    ('conceptB', 'Concept B', 'https://conceptB', 'A concept B.', 'abuse');
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
    ('BTC', 'tag_addressB'),
    ('BTC', 'tag_addressA');
INSERT INTO confidence (id, label, description, level) VALUES 
    ('ownership', 'Proven address ownership', 'Creator controls the private key the address associated with a tag', 100),
	('forensic', 'Forensic reports', 'Creator retrieved data attribution data from somehow trusted reports (e.g. academic papers)', 50),
	('web_crawl', 'Web crawls', 'Attribution tags were retrieved from crawling the web or other data dumps', 20);

INSERT INTO tag (label, address, currency, category, source, tagpack, lastmod, is_cluster_definer, confidence) VALUES
    ('Internet, Archive', 'addressA', 'BTC', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri', to_timestamp(1560290400), true, 'ownership'),
    ('Internet Archive 2', 'addressA', 'BTC', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri_private', to_timestamp(1560290400), true, 'web_crawl'),
    ('addressTag1', 'addressA', 'BTC', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri', to_timestamp(1), false, 'forensic'),
    ('addressTag2', 'addressH', 'BTC', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri', to_timestamp(2), false, 'ownership'),
    ('labelABC', 'a123456', 'BTC', 'exchange', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), true, 'ownership'),
    ('labelX', 'address2818641', 'BTC', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), true, 'ownership'),
    ('labelY', 'address2818641', 'BTC', 'organization', 'https://source', 'https://tagpack_uri_private', to_timestamp(1560290400), true, 'ownership'),
    ('abcdefgLabel', 'abcdefg', 'BTC', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), false, 'ownership'),
    ('labelX', 'addressE', 'BTC', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), false, 'ownership'),
    ('labelY', 'addressE', 'BTC', 'organization', 'https://source', 'https://tagpack_uri_private', to_timestamp(1560290400), false, 'ownership'),
    ('isolinks', 'addressX', 'BTC', 'exchange', 'Unspecified', 'https://tagpack_uri', to_timestamp(1), true, 'ownership'),
    ('isolinks', 'addressY', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri_private', to_timestamp(1), true, 'ownership'),
    ('cimedy', 'addressY', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false, 'ownership'),
    ('x', 'tag_addressA', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false, 'ownership'),
    ('y', 'tag_addressB', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false, 'ownership'),
    ('cimedy', 'addressA', 'LTC', 'exchange', 'source', 'https://tagpack_uri', to_timestamp(3), false, 'ownership'),
    ('coinbase', 'addressB', 'LTC', 'exchange', 'Team', 'https://tagpack_uri', to_timestamp(4), false, 'ownership'),
    ('TagA', '0xabcdef', 'ETH', NULL, 'sourceX', 'uriX', to_timestamp(1), true, 'ownership'),
    ('TagB', '0xabcdef', 'ETH', NULL, 'sourceY', 'uriY', to_timestamp(1), false, 'ownership'),
    ('LabelX', '0x123456', 'ETH', NULL, 'sourceX', 'uriX', to_timestamp(1), false, 'ownership'),
    ('LabelY', '0x123456', 'ETH', NULL, 'sourceY', 'uriY', to_timestamp(1), false, 'ownership');
INSERT INTO address_cluster_mapping (currency, address, gs_cluster_id, gs_cluster_def_addr, gs_cluster_no_addr) VALUES
    ('BTC', 'addressX', 123, '', 10),
    ('BTC', 'addressY', 456, '', 10),
    ('BTC', 'addressA', 17642138, '', 20),
    ('BTC', 'addressH', 17642138, '', 20),
    ('BTC', 'address2818641', 2818641, '', 30),
    ('BTC', 'tag_addressA', 12, '', 2),
    ('BTC', 'tag_addressB', 12, '', 2),
    ('LTC', 'addressA', 1234, '', 20),
    ('ETH', '0xabcdef', 107925000, '', 40),
    ('ETH', '0x123456', 107925001, '', 50);

REFRESH MATERIALIZED VIEW label;
REFRESH MATERIALIZED VIEW statistics;
REFRESH MATERIALIZED VIEW tag_count_by_cluster;
REFRESH MATERIALIZED VIEW cluster_defining_tags_by_frequency_and_maxconfidence;
