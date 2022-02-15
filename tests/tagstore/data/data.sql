INSERT INTO taxonomy (id, source, description) VALUES
    ('entity', 'http://entity', 'The entity taxonomy.'),
    ('abuse', 'http://abuse', 'The abuse taxonomy.');
INSERT INTO concept (id, label, source, description, taxonomy) VALUES 
    ('organization', 'An organization', 'https://organization', 'An organization is foo.', 'entity'),
    ('exchange', 'An exchange', 'https://exchange', 'An exchange is foo.', 'entity'),
    ('conceptB', 'Concept B', 'https://conceptB', 'A concept B.', 'abuse');
INSERT INTO tagpack (id, title, description, creator, owner, is_public) VALUES
    ('https://tagpack_uri', '', '', '', '', true),
    ('https://tagpack_uri_private', '', '', '', '', false),
    ('uriX', '', '', '', '', false),
    ('uriY', '', '', '', '', true);
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
    ('ETH', '0x123456');
INSERT INTO tag (label, address, currency, category, source, tagpack, lastmod, is_cluster_definer) VALUES
    ('Internet, Archive', 'addressA', 'BTC', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri', to_timestamp(1560290400), true),
    ('Internet Archive 2', 'addressA', 'BTC', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri_private', to_timestamp(1560290400), true),
    ('addressTag1', 'addressA', 'BTC', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri', to_timestamp(1), false),
    ('addressTag2', 'addressH', 'BTC', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri', to_timestamp(2), false),
    ('labelABC', 'a123456', 'BTC', 'exchange', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), true),
    ('labelX', 'address2818641', 'BTC', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), true),
    ('labelY', 'address2818641', 'BTC', 'organization', 'https://source', 'https://tagpack_uri_private', to_timestamp(1560290400), true),
    ('abcdefgLabel', 'abcdefg', 'BTC', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), false),
    ('labelX', 'addressE', 'BTC', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), false),
    ('labelY', 'addressE', 'BTC', 'organization', 'https://source', 'https://tagpack_uri_private', to_timestamp(1560290400), false),
    ('isolinks', 'addressX', 'BTC', 'exchange', 'Unspecified', 'https://tagpack_uri', to_timestamp(1), true),
    ('isolinks', 'addressY', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri_private', to_timestamp(1), true),
    ('cimedy', 'addressY', 'BTC', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false),
    ('cimedy', 'addressA', 'LTC', 'exchange', 'source', 'https://tagpack_uri', to_timestamp(3), false),
    ('coinbase', 'addressB', 'LTC', 'exchange', 'Team', 'https://tagpack_uri', to_timestamp(4), false),
    ('TagA', '0xabcdef', 'ETH', NULL, 'sourceX', 'uriX', to_timestamp(1), true),
    ('TagB', '0xabcdef', 'ETH', NULL, 'sourceY', 'uriY', to_timestamp(1), false),
    ('LabelX', '0x123456', 'ETH', NULL, 'sourceX', 'uriX', to_timestamp(1), false),
    ('LabelY', '0x123456', 'ETH', NULL, 'sourceY', 'uriY', to_timestamp(1), false);
INSERT INTO address_cluster_mapping (currency, address, gs_cluster_id, gs_cluster_def_addr) VALUES
    ('BTC', 'addressX', 123, ''),
    ('BTC', 'addressA', 17642138, ''),
    ('BTC', 'addressH', 17642138, ''),
    ('BTC', 'address2818641', 2818641, ''),
    ('ETH', '0xabcdef', 107925000, ''),
    ('ETH', '0x123456', 107925001, '');

REFRESH MATERIALIZED VIEW label;
REFRESH MATERIALIZED VIEW statistics;
