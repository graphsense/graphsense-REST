# This file contains instance specific configuration options.

# Cassandra host names and keyspace names are taken from the .env file. Consult README for more infromation.

import os
CASSANDRA_NODES = [os.getenv("CASSANDRA_HOST")]

MAPPING = {
    "tagpacks": os.getenv("TAG_KEYSPACE"),
    "btc": [os.getenv("RAW_KEYSPACE"), os.getenv("TARGET_KEYSPACE")]
}

#USE_PROXY = True

# Restrict allowed origins for CORS
#
# The origin, or list of origins to allow requests from. The origin(s) may be regular expressions, case-sensitive strings, or else an asterisk
# (see https://flask-cors.readthedocs.io/en/latest/api.html for further details)
#
# Default : ‘*’ 
# ALLOWED_ORIGINS = ['https://example.com']

