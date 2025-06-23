import pytest
from testcontainers.cassandra import CassandraContainer
from testcontainers.postgres import PostgresContainer

from tests import BaseTestCase
from tests.cassandra.insert import load_test_data as cas_load_test_data
from tests.tagstore.insert import load_test_data as tags_load_test_data
from os import environ

postgres = PostgresContainer("postgres:16-alpine")
cassandra = CassandraContainer("cassandra:4.1.4")


@pytest.fixture(scope="session", autouse=True)
def gs_rest_db_setup(request):
    SKIP_REST_CONTAINER_SETUP = environ.get("SKIP_REST_CONTAINER_SETUP", False)
    if SKIP_REST_CONTAINER_SETUP:
        return

    postgres.start()
    cassandra.start()

    def remove_container():
        postgres.stop()
        cassandra.stop()

    request.addfinalizer(remove_container)

    cas_host = cassandra.get_container_host_ip()
    cas_port = cassandra.get_exposed_port(9042)

    postgres_sync_url = postgres.get_connection_url()
    portgres_async_url = postgres_sync_url.replace("psycopg2", "asyncpg")

    config = {
        "logging": {"level": "DEBUG"},
        "database": {
            "driver": "cassandra",
            "port": cas_port,
            "nodes": [cas_host],
            "currencies": {
                "btc": {
                    "raw": "resttest_btc_raw",
                    "transformed": "resttest_btc_transformed",
                },
                "ltc": {
                    "raw": "resttest_ltc_raw",
                    "transformed": "resttest_ltc_transformed",
                },
                "eth": {
                    "raw": "resttest_eth_raw",
                    "transformed": "resttest_eth_transformed",
                },
                "trx": {
                    "raw": "resttest_trx_raw",
                    "transformed": "resttest_trx_transformed",
                },
            },
        },
        "gs-tagstore": {"url": portgres_async_url},
        "show_private_tags": {"on_header": {"Authorization": "x"}},
    }

    # Ugly hack to pass parameters
    BaseTestCase.config = config

    cas_load_test_data(cas_host, cas_port)

    tags_load_test_data(postgres_sync_url.replace("+psycopg2", ""))

    return config
