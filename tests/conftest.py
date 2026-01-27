import subprocess
from os import environ
from pathlib import Path

import docker
import pytest
from testcontainers.cassandra import CassandraContainer
from testcontainers.postgres import PostgresContainer

from tests import BaseTestCase
from tests.cassandra.insert import load_test_data as cas_load_test_data
from tests.tagstore.insert import load_test_data as tags_load_test_data

postgres = PostgresContainer("postgres:16-alpine")

# Pre-baked Cassandra image with schemas and fast startup settings already configured
# Build with: make build-test-cassandra
# Baked-in optimizations: NUM_TOKENS=1, ring_delay_ms=100, skip_wait_for_gossip=0
CASSANDRA_TEST_IMAGE = environ.get(
    "CASSANDRA_TEST_IMAGE", "graphsense/cassandra-test:4.1.4"
)


def ensure_cassandra_image_exists():
    """Build Cassandra test image if it doesn't exist locally."""
    client = docker.from_env()
    try:
        client.images.get(CASSANDRA_TEST_IMAGE)
    except docker.errors.ImageNotFound:
        dockerfile_path = Path(__file__).parent / "cassandra"
        subprocess.run(
            ["docker", "build", "-t", CASSANDRA_TEST_IMAGE, str(dockerfile_path)],
            check=True,
        )


ensure_cassandra_image_exists()
cassandra = CassandraContainer(CASSANDRA_TEST_IMAGE)


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
            "strict_data_validation": False,
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
