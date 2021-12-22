INSERT INTO taxonomy (id, source, description) VALUES
    ('entity', 'http://entity', 'The entity taxonomy.'),
    ('abuse', 'http://abuse', 'The abuse taxonomy.');
INSERT INTO concept (id, label, source, description, taxonomy) VALUES 
    ('organization', 'An organization', 'https://organization', 'An organization is foo.', 'entity'),
    ('exchange', 'An exchange', 'https://exchange', 'An exchange is foo.', 'entity'),
    ('conceptB', 'Concept B', 'https://conceptB', 'A concept B.', 'abuse');
INSERT INTO tagpack (id, title, description, creator, owner) VALUES
    ('https://tagpack_uri', '', '', '', ''),
    ('uriX', '', '', '', ''),
    ('uriY', '', '', '', '');
INSERT INTO address (currency, address) VALUES
    ('btc', 'addressA'),
    ('btc', 'a123456'),
    ('btc', 'address2818641'),
    ('btc', 'abcdefg'),
    ('btc', 'addressE'),
    ('btc', 'addressX'),
    ('btc', 'addressY'),
    ('ltc', 'addressA'),
    ('ltc', 'addressB'),
    ('eth', '0xabcdef'),
    ('eth', '0x123456');
INSERT INTO tag (label, address, currency, category, source, tagpack, lastmod, is_cluster_definer) VALUES
    ('Internet, Archive', 'addressA', 'btc', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri', to_timestamp(1560290400), true),
    ('Internet, Archive 2', 'addressA', 'btc', 'organization', 'https://archive.org/donate/cryptocurrency', 'https://tagpack_uri', to_timestamp(1560290400), true),
    ('labelABC', 'a123456', 'btc', 'exchange', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), true),
    ('labelX', 'address2818641', 'btc', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), true),
    ('labelY', 'address2818641', 'btc', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), true),
    ('abcdefgLabel', 'abcdefg', 'btc', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), false),
    ('labelX', 'addressE', 'btc', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), false),
    ('labelY', 'addressE', 'btc', 'organization', 'https://source', 'https://tagpack_uri', to_timestamp(1560290400), false),
    ('isolinks', 'addressX', 'btc', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(1), true),
    ('isolinks', 'addressY', 'btc', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(1), true),
    ('cimedy', 'addressY', 'btc', NULL, 'Unspecified', 'https://tagpack_uri', to_timestamp(2), false),
    ('cimedy', 'addressA', 'ltc', 'exchange', 'source', 'https://tagpack_uri', to_timestamp(3), false),
    ('coinbase', 'addressB', 'ltc', 'exchange', 'Team', 'https://tagpack_uri', to_timestamp(4), false),
    ('TagA', '0xabcdef', 'eth', NULL, 'sourceX', 'uriX', to_timestamp(1), false),
    ('TagB', '0xabcdef', 'eth', NULL, 'sourceY', 'uriY', to_timestamp(1), false),
    ('LabelX', '0x123456', 'eth', NULL, 'sourceX', 'uriX', to_timestamp(1), false),
    ('LabelY', '0x123456', 'eth', NULL, 'sourceY', 'uriY', to_timestamp(1), false);
INSERT INTO address_cluster_mapping (currency, address, gs_cluster_id, gs_cluster_def_addr) VALUES
    ('btc', 'addressX', 123, '');

