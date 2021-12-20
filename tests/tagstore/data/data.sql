INSERT INTO taxonomy (id, source, description) VALUES
    ('entity', 'http://entity', 'The entity taxonomy.'),
    ('abuse', 'http://abuse', 'The abuse taxonomy.');
INSERT INTO concept (id, label, source, description, taxonomy) VALUES 
    ('organization', 'An organization', 'https://organization', 'An organization is foo.', 'entity'),
    ('exchange', 'An exchange', 'https://exchange', 'An exchange is foo.', 'entity'),
    ('conceptB', 'Concept B', 'https://conceptB', 'A concept B.', 'abuse');

 INSERT INTO tagpack (id, title, description, creator, owner) VALUES
    ("http://tagpack_uri", "", "", "", ""),
    ("uriX", "", "", "", ""),
    ("uriY", "", "", "", "");
    
 INSERT INTO tag (label, address, currency, category, source, tagpack, lastmod, is_cluster_definer) VALUES
    ("Internet, Archive", "addressA", "btc", "organization", "https://archive.org/donate/cryptocurrency", "http://tagpack_uri", 1560290400, true),
    ("Internet, Archive 2", "addressA", "btc", "organization", "https://archive.org/donate/cryptocurrency", "http://tagpack_uri", 1560290400, true),
    ("labelABC", "a123456", "btc", "exchange", "https://source", "http://tagpack_uri", 1560290400, true),
    ("labelX", "address2818641", "btc", "organization", "https://source", "http://tagpack_uri", 1560290400, true),
    ("labelY", "address2818641", "btc", "organization", "https://source", "http://tagpack_uri", 1560290400, true),
    ("abcdefgLabel", "abcdefg", "btc", "organization", "https://source", "http://tagpack_uri", 1560290400),
    ("labelX", "addressE", "btc", "organization", "https://source", "http://tagpack_uri", 1560290400),
    ("labelY", "addressE", "btc", "organization", "https://source", "http://tagpack_uri", 1560290400),
    ("cimedy", "addressA", "ltc", "exchange", "source", "https://tagpack_uri", 3),
    ("coinbase", "addressB", "ltc", "exchange", "Team", "https://tagpack_uri", 4),
    ("TagA", "0xabcdef", "eth", NULL, "sourceX", "uriX", 1),
    ("TagB", "0xabcdef", "eth", NULL, "sourceY", "uriY", 1),
    ("LabelX", "0x123456", "eth", NULL, "sourceX", "uriX", 1),
    ("LabelY", "0x123456", "eth", NULL, "sourceY", "uriY", 1);
