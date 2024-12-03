import logging
import os
from functools import cache
from pathlib import Path

import requests
from cassandra.cluster import Cluster

DATA_DIR = Path(__file__).parent.resolve() / "data"

TAG = "master"
SCHEMA_BASE = f"https://raw.githubusercontent.com/graphsense/graphsense-lib/{TAG}/src/graphsenselib/schema/resources/"

SCHEMA_MAPPING = {"btc": "utxo", "ltc": "utxo", "eth": "account", "trx": "account_trx"}

SCHEMA_MAPPING_OVERRIDE = {("trx", "transformed"): "account"}

MAGIC_REPLACE_CONSTANT = "0x8BADF00D"
MAGIC_REPLACE_CONSTANT2 = f"{MAGIC_REPLACE_CONSTANT}_REPLICATION_CONFIG"

SIMPLE_REPLICATION_CONFIG = "{'class': 'SimpleStrategy', 'replication_factor': 1}"


@cache
def get_schema_file(file: str):
    res = requests.get(SCHEMA_BASE + file)
    return res.text


def load_test_data(host, port):
    cluster = Cluster([host], port=port)
    session = cluster.connect()

    for k, v in SCHEMA_MAPPING.items():
        for st in ["raw", "transformed"]:
            v = SCHEMA_MAPPING_OVERRIDE.get((k, st), v)
            filename = f"{st}_{v}_schema.sql"
            keyspace = f"resttest_{k}_{st}"

            logging.info(f"creating db tables cassandra {filename}")
            schema_str = (
                get_schema_file(filename)
                .replace(MAGIC_REPLACE_CONSTANT2, SIMPLE_REPLICATION_CONFIG)
                .replace(MAGIC_REPLACE_CONSTANT, keyspace)
            )
            for x in schema_str.split(";"):
                x = x.strip()
                if x:
                    session.execute(x)

    for x in DATA_DIR.iterdir():
        if not x.is_file():
            continue
        table_name = os.path.basename(x)
        content = x.read_text()
        for x in content.split("\n"):
            x = x.strip()
            if x:
                session.execute(
                    f"""
                    INSERT INTO {table_name} JSON '{x}'
                    """
                )
