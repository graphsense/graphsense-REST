"""
Test to compare FastAPI migration against original aiohttp/Connexion version.

This test runs both server versions and compares their JSON outputs to ensure
the migration maintains exact functional equivalence.

Usage:
    # Start old server on port 9001
    GS_REST_DEV_PORT=9001 make serve-old

    # Start new FastAPI server on port 9002
    uv run uvicorn gsrest.app:create_app --factory --port 9002

    # Run comparison tests
    uv run pytest tests/test_fastapi_migration.py -v -s
"""

import json
import logging
import os
import time
from typing import Any
from urllib.parse import urljoin

import pytest
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server endpoints - can be overridden via environment variables
OLD_SERVER = os.environ.get("OLD_SERVER", "http://localhost:9001")
NEW_SERVER = os.environ.get("NEW_SERVER", "http://localhost:9002")

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Test data constants
BTC_ADDRESS = "1Archive1n2C579dMsAu3iC6tWzuQJz8dN"
ETH_ADDRESS = "0xdac17f958d2ee523a2206206994597c13d831ec7"
BTC_ENTITY = 109578
BTC_TX = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
BTC_HEIGHT = 100000


def get_response(base_url: str, endpoint: str, auth: str = "test") -> tuple[dict, int, float]:
    """Get response from an endpoint, returning (data, status_code, elapsed_time)."""
    url = urljoin(base_url + "/", endpoint.lstrip("/"))
    headers = {**HEADERS, "Authorization": auth}

    start = time.time()
    response = requests.get(url, headers=headers, timeout=30)
    elapsed = time.time() - start

    try:
        data = response.json()
    except json.JSONDecodeError:
        data = {"_raw": response.text}

    return data, response.status_code, elapsed


def post_response(base_url: str, endpoint: str, body: dict, auth: str = "test") -> tuple[dict, int, float]:
    """POST request to an endpoint, returning (data, status_code, elapsed_time)."""
    url = urljoin(base_url + "/", endpoint.lstrip("/"))
    headers = {**HEADERS, "Authorization": auth}

    start = time.time()
    response = requests.post(url, headers=headers, json=body, timeout=60)
    elapsed = time.time() - start

    try:
        data = response.json()
    except json.JSONDecodeError:
        data = {"_raw": response.text}

    return data, response.status_code, elapsed


def normalize_response(data: Any) -> Any:
    """Normalize response data for comparison.

    Handles known differences that are acceptable:
    - Floating point precision differences
    - Ordering of certain list items (where order doesn't matter)
    """
    if isinstance(data, dict):
        return {k: normalize_response(v) for k, v in sorted(data.items())}
    elif isinstance(data, list):
        return [normalize_response(item) for item in data]
    elif isinstance(data, float):
        # Round floats to avoid precision issues
        return round(data, 8)
    return data


# Keys for which list order doesn't matter (unordered results from database)
UNORDERED_LIST_KEYS = {"address_tags", "addresses", "tags"}


def get_sort_key(item: Any) -> Any:
    """Get a sort key for list items."""
    if isinstance(item, dict):
        # Use '_request_address' or 'address' as primary sort key, then 'label'
        if "_request_address" in item:
            return (item.get("_request_address", ""), str(item))
        if "address" in item:
            return (item.get("address", ""), item.get("label", ""), str(item))
        return str(sorted(item.items()))
    return str(item)


def should_sort_list(data: list, path: str) -> bool:
    """Determine if a list should be sorted before comparison."""
    # Check if path ends with an unordered key
    path_key = path.split(".")[-1] if path else ""
    if path_key in UNORDERED_LIST_KEYS:
        return True
    # Top-level lists (bulk results) with address items should be sorted
    if path == "" and data and isinstance(data[0], dict):
        if "_request_address" in data[0] or "address" in data[0]:
            return True
    return False


def compare_responses(old_data: Any, new_data: Any, path: str = "") -> list[str]:
    """Compare two responses and return list of differences."""
    differences = []

    if type(old_data) != type(new_data):
        differences.append(f"{path}: type mismatch: {type(old_data).__name__} vs {type(new_data).__name__}")
        return differences

    if isinstance(old_data, dict):
        old_keys = set(old_data.keys())
        new_keys = set(new_data.keys())

        missing_in_new = old_keys - new_keys
        missing_in_old = new_keys - old_keys

        if missing_in_new:
            differences.append(f"{path}: keys missing in new: {missing_in_new}")
        if missing_in_old:
            differences.append(f"{path}: extra keys in new: {missing_in_old}")

        for key in old_keys & new_keys:
            sub_path = f"{path}.{key}" if path else key
            differences.extend(compare_responses(old_data[key], new_data[key], sub_path))

    elif isinstance(old_data, list):
        if len(old_data) != len(new_data):
            differences.append(f"{path}: list length mismatch: {len(old_data)} vs {len(new_data)}")
        else:
            # Check if this is an unordered list
            if should_sort_list(old_data, path):
                # Sort both lists before comparing
                old_sorted = sorted(old_data, key=get_sort_key)
                new_sorted = sorted(new_data, key=get_sort_key)
                for i, (old_item, new_item) in enumerate(zip(old_sorted, new_sorted)):
                    differences.extend(compare_responses(old_item, new_item, f"{path}[{i}]"))
            else:
                for i, (old_item, new_item) in enumerate(zip(old_data, new_data)):
                    differences.extend(compare_responses(old_item, new_item, f"{path}[{i}]"))

    elif old_data != new_data:
        # Truncate long values for readability
        old_str = str(old_data)[:100]
        new_str = str(new_data)[:100]
        differences.append(f"{path}: value mismatch: {old_str} vs {new_str}")

    return differences


def check_servers_available():
    """Check if both servers are running."""
    for name, url in [("OLD", OLD_SERVER), ("NEW", NEW_SERVER)]:
        try:
            response = requests.get(f"{url}/stats", headers=HEADERS, timeout=5)
            if response.status_code not in [200, 401, 403]:
                pytest.skip(f"{name} server at {url} returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            pytest.skip(f"{name} server not available at {url}")


class MigrationTestBase:
    """Base class for migration tests with shared utilities."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Check servers are available before each test."""
        check_servers_available()

    def compare_endpoint(self, endpoint: str, auth: str = "test") -> dict:
        """Compare an endpoint between old and new servers."""
        old_data, old_status, old_time = get_response(OLD_SERVER, endpoint, auth)
        new_data, new_status, new_time = get_response(NEW_SERVER, endpoint, auth)

        result = {
            "endpoint": endpoint,
            "old_status": old_status,
            "new_status": new_status,
            "old_time": old_time,
            "new_time": new_time,
            "speedup": old_time / new_time if new_time > 0 else 0,
            "differences": [],
        }

        if old_status != new_status:
            result["differences"].append(f"Status code mismatch: {old_status} vs {new_status}")
        elif old_status == 200:
            # Only compare content if both succeeded
            old_normalized = normalize_response(old_data)
            new_normalized = normalize_response(new_data)
            result["differences"] = compare_responses(old_normalized, new_normalized)

        return result

    def compare_post_endpoint(self, endpoint: str, body: dict, auth: str = "test") -> dict:
        """Compare a POST endpoint between old and new servers."""
        old_data, old_status, old_time = post_response(OLD_SERVER, endpoint, body, auth)
        new_data, new_status, new_time = post_response(NEW_SERVER, endpoint, body, auth)

        result = {
            "endpoint": endpoint,
            "body": body,
            "old_status": old_status,
            "new_status": new_status,
            "old_time": old_time,
            "new_time": new_time,
            "differences": [],
        }

        if old_status != new_status:
            result["differences"].append(f"Status code mismatch: {old_status} vs {new_status}")
        elif old_status == 200:
            old_normalized = normalize_response(old_data)
            new_normalized = normalize_response(new_data)
            result["differences"] = compare_responses(old_normalized, new_normalized)

        return result

    def assert_endpoint_equal(self, endpoint: str, auth: str = "test"):
        """Assert that an endpoint returns identical results from both servers."""
        result = self.compare_endpoint(endpoint, auth)

        logger.info(
            f"  {endpoint}: old={result['old_time']:.3f}s, new={result['new_time']:.3f}s, "
            f"speedup={result['speedup']:.1f}x"
        )

        if result["differences"]:
            diff_str = "\n  ".join(result["differences"][:10])  # Show first 10 differences
            if len(result["differences"]) > 10:
                diff_str += f"\n  ... and {len(result['differences']) - 10} more differences"
            pytest.fail(f"Endpoint {endpoint} has differences:\n  {diff_str}")

    def assert_post_endpoint_equal(self, endpoint: str, body: dict, auth: str = "test"):
        """Assert that a POST endpoint returns identical results from both servers."""
        result = self.compare_post_endpoint(endpoint, body, auth)

        logger.info(f"  {endpoint}: old={result['old_time']:.3f}s, new={result['new_time']:.3f}s")

        if result["differences"]:
            diff_str = "\n  ".join(result["differences"][:10])
            if len(result["differences"]) > 10:
                diff_str += f"\n  ... and {len(result['differences']) - 10} more differences"
            pytest.fail(f"Endpoint {endpoint} has differences:\n  {diff_str}")


class TestFastAPIMigrationBasic(MigrationTestBase):
    """Basic endpoint tests - one test per endpoint with default parameters."""

    @pytest.mark.migration
    def test_openapi_spec(self):
        """Test that OpenAPI specs have matching endpoints and operations."""
        old_resp = requests.get(f"{OLD_SERVER}/openapi.json", headers=HEADERS, timeout=30)
        new_resp = requests.get(f"{NEW_SERVER}/openapi.json", headers=HEADERS, timeout=30)

        assert old_resp.status_code == 200, f"Old server OpenAPI returned {old_resp.status_code}"
        assert new_resp.status_code == 200, f"New server OpenAPI returned {new_resp.status_code}"

        old_spec = old_resp.json()
        new_spec = new_resp.json()

        # Normalize paths by stripping trailing slashes
        def normalize_path(p):
            return p.rstrip("/") if p != "/" else p

        # Compare paths (endpoints)
        old_paths = {normalize_path(p) for p in old_spec.get("paths", {}).keys()}
        new_paths = {normalize_path(p) for p in new_spec.get("paths", {}).keys()}

        missing_in_new = old_paths - new_paths
        extra_in_new = new_paths - old_paths

        differences = []
        if missing_in_new:
            differences.append(f"Paths missing in FastAPI: {sorted(missing_in_new)}")
        if extra_in_new:
            differences.append(f"Extra paths in FastAPI: {sorted(extra_in_new)}")

        # Build normalized path to original path mappings
        old_path_map = {normalize_path(p): p for p in old_spec.get("paths", {}).keys()}
        new_path_map = {normalize_path(p): p for p in new_spec.get("paths", {}).keys()}

        # Compare operations for each shared path
        for norm_path in old_paths & new_paths:
            old_orig = old_path_map[norm_path]
            new_orig = new_path_map[norm_path]

            old_methods = set(old_spec["paths"][old_orig].keys())
            new_methods = set(new_spec["paths"][new_orig].keys())

            # Filter out non-HTTP methods like 'parameters'
            http_methods = {"get", "post", "put", "delete", "patch", "head", "options"}
            old_methods = old_methods & http_methods
            new_methods = new_methods & http_methods

            if old_methods != new_methods:
                differences.append(
                    f"Path {norm_path}: methods differ - old={old_methods}, new={new_methods}"
                )

        if differences:
            pytest.fail(f"OpenAPI spec differences:\n  " + "\n  ".join(differences))

    @pytest.mark.migration
    def test_stats(self):
        """Test /stats endpoint."""
        self.assert_endpoint_equal("stats")

    @pytest.mark.migration
    def test_search_basic(self):
        """Test /search endpoint."""
        self.assert_endpoint_equal("search?q=binance&limit=5")

    @pytest.mark.migration
    def test_get_address_btc(self):
        """Test BTC address endpoint."""
        self.assert_endpoint_equal(f"btc/addresses/{BTC_ADDRESS}")

    @pytest.mark.migration
    def test_get_address_eth(self):
        """Test ETH address endpoint."""
        self.assert_endpoint_equal(f"eth/addresses/{ETH_ADDRESS}")

    @pytest.mark.migration
    def test_get_entity_btc(self):
        """Test BTC entity endpoint."""
        self.assert_endpoint_equal(f"btc/entities/{BTC_ENTITY}")

    @pytest.mark.migration
    def test_get_block(self):
        """Test block endpoint."""
        self.assert_endpoint_equal(f"btc/blocks/{BTC_HEIGHT}")

    @pytest.mark.migration
    def test_get_tx(self):
        """Test transaction endpoint."""
        self.assert_endpoint_equal(f"btc/txs/{BTC_TX}")

    @pytest.mark.migration
    def test_get_exchange_rates(self):
        """Test exchange rates endpoint."""
        self.assert_endpoint_equal(f"btc/rates/{BTC_HEIGHT}")

    @pytest.mark.migration
    def test_list_address_txs(self):
        """Test address transactions endpoint."""
        self.assert_endpoint_equal(f"btc/addresses/{BTC_ADDRESS}/txs?pagesize=5")

    @pytest.mark.migration
    def test_list_address_neighbors(self):
        """Test address neighbors endpoint."""
        self.assert_endpoint_equal(f"btc/addresses/{BTC_ADDRESS}/neighbors?direction=out&pagesize=5")

    @pytest.mark.migration
    def test_list_entity_addresses(self):
        """Test entity addresses endpoint."""
        self.assert_endpoint_equal(f"btc/entities/{BTC_ENTITY}/addresses?pagesize=5")

    @pytest.mark.migration
    def test_list_entity_neighbors(self):
        """Test entity neighbors endpoint."""
        self.assert_endpoint_equal(f"btc/entities/{BTC_ENTITY}/neighbors?direction=out&pagesize=5")

    @pytest.mark.migration
    def test_list_tags_by_address(self):
        """Test address tags endpoint."""
        self.assert_endpoint_equal(f"btc/addresses/{BTC_ADDRESS}/tags")

    @pytest.mark.migration
    def test_list_taxonomies(self):
        """Test taxonomies endpoint."""
        self.assert_endpoint_equal("tags/taxonomies")

    @pytest.mark.migration
    def test_supported_tokens(self):
        """Test supported tokens endpoint."""
        self.assert_endpoint_equal("eth/supported_tokens/")


class TestSearchParameters(MigrationTestBase):
    """Test search endpoint with various parameter configurations."""

    @pytest.mark.migration
    @pytest.mark.parametrize("currency", [None, "btc", "eth"])
    def test_search_currency_filter(self, currency):
        """Test search with currency filter."""
        if currency:
            self.assert_endpoint_equal(f"search?q=binance&currency={currency}&limit=5")
        else:
            self.assert_endpoint_equal("search?q=binance&limit=5")

    @pytest.mark.migration
    @pytest.mark.parametrize("include_labels,include_actors", [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ])
    def test_search_include_flags(self, include_labels, include_actors):
        """Test search with include flags."""
        endpoint = f"search?q=binance&limit=5&include_labels={str(include_labels).lower()}&include_actors={str(include_actors).lower()}"
        self.assert_endpoint_equal(endpoint)

    @pytest.mark.migration
    @pytest.mark.parametrize("include_txs,include_addresses", [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ])
    def test_search_include_results(self, include_txs, include_addresses):
        """Test search with result type flags."""
        endpoint = f"search?q=binance&limit=5&include_txs={str(include_txs).lower()}&include_addresses={str(include_addresses).lower()}"
        self.assert_endpoint_equal(endpoint)


class TestAddressParameters(MigrationTestBase):
    """Test address endpoints with various parameter configurations."""

    @pytest.mark.migration
    @pytest.mark.parametrize("include_actors", [True, False])
    def test_get_address_include_actors(self, include_actors):
        """Test get_address with include_actors parameter."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}?include_actors={str(include_actors).lower()}"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("direction", ["in", "out"])
    def test_list_address_txs_direction(self, direction):
        """Test list_address_txs with direction parameter."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}/txs?direction={direction}&pagesize=5"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("order", ["asc", "desc"])
    def test_list_address_txs_order(self, order):
        """Test list_address_txs with order parameter."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}/txs?order={order}&pagesize=5"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("direction,order", [
        ("in", "asc"),
        ("in", "desc"),
        ("out", "asc"),
        ("out", "desc"),
    ])
    def test_list_address_txs_direction_order(self, direction, order):
        """Test list_address_txs with direction and order parameters."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}/txs?direction={direction}&order={order}&pagesize=5"
        )

    @pytest.mark.migration
    def test_list_address_txs_height_filter(self):
        """Test list_address_txs with height filtering."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}/txs?min_height=100000&max_height=200000&pagesize=5"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("direction", ["in", "out"])
    def test_list_address_neighbors_direction(self, direction):
        """Test list_address_neighbors with direction parameter."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}/neighbors?direction={direction}&pagesize=5"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("include_labels", [True, False])
    def test_list_address_neighbors_include_labels(self, include_labels):
        """Test list_address_neighbors with include_labels parameter."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}/neighbors?direction=out&include_labels={str(include_labels).lower()}&pagesize=5"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("include_actors", [True, False])
    def test_list_address_neighbors_include_actors(self, include_actors):
        """Test list_address_neighbors with include_actors parameter."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}/neighbors?direction=out&include_actors={str(include_actors).lower()}&pagesize=5"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("include_best_cluster_tag", [True, False])
    def test_list_tags_by_address_include_cluster_tag(self, include_best_cluster_tag):
        """Test list_tags_by_address with include_best_cluster_tag parameter."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}/tags?include_best_cluster_tag={str(include_best_cluster_tag).lower()}"
        )

    @pytest.mark.migration
    def test_list_tags_by_address_pagesize(self):
        """Test list_tags_by_address with pagesize parameter."""
        self.assert_endpoint_equal(f"btc/addresses/{BTC_ADDRESS}/tags?pagesize=10")

    @pytest.mark.migration
    @pytest.mark.parametrize("include_best_cluster_tag", [True, False])
    def test_get_tag_summary_by_address(self, include_best_cluster_tag):
        """Test get_tag_summary_by_address with include_best_cluster_tag parameter."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}/tag_summary?include_best_cluster_tag={str(include_best_cluster_tag).lower()}"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("include_actors", [True, False])
    def test_get_address_entity_include_actors(self, include_actors):
        """Test get_address_entity with include_actors parameter."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}/entity?include_actors={str(include_actors).lower()}"
        )


class TestEntityParameters(MigrationTestBase):
    """Test entity endpoints with various parameter configurations."""

    @pytest.mark.migration
    @pytest.mark.parametrize("include_actors", [True, False])
    def test_get_entity_include_actors(self, include_actors):
        """Test get_entity with include_actors parameter."""
        self.assert_endpoint_equal(
            f"btc/entities/{BTC_ENTITY}?include_actors={str(include_actors).lower()}"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("exclude_best_address_tag", [True, False])
    def test_get_entity_exclude_best_tag(self, exclude_best_address_tag):
        """Test get_entity with exclude_best_address_tag parameter."""
        self.assert_endpoint_equal(
            f"btc/entities/{BTC_ENTITY}?exclude_best_address_tag={str(exclude_best_address_tag).lower()}"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("direction", ["in", "out"])
    def test_list_entity_neighbors_direction(self, direction):
        """Test list_entity_neighbors with direction parameter."""
        self.assert_endpoint_equal(
            f"btc/entities/{BTC_ENTITY}/neighbors?direction={direction}&pagesize=5"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("include_labels", [True, False])
    def test_list_entity_neighbors_include_labels(self, include_labels):
        """Test list_entity_neighbors with include_labels parameter."""
        self.assert_endpoint_equal(
            f"btc/entities/{BTC_ENTITY}/neighbors?direction=out&include_labels={str(include_labels).lower()}&pagesize=5"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("include_actors", [True, False])
    def test_list_entity_neighbors_include_actors(self, include_actors):
        """Test list_entity_neighbors with include_actors parameter."""
        self.assert_endpoint_equal(
            f"btc/entities/{BTC_ENTITY}/neighbors?direction=out&include_actors={str(include_actors).lower()}&pagesize=5"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("exclude_best_address_tag", [True, False])
    def test_list_entity_neighbors_exclude_best_tag(self, exclude_best_address_tag):
        """Test list_entity_neighbors with exclude_best_address_tag parameter."""
        self.assert_endpoint_equal(
            f"btc/entities/{BTC_ENTITY}/neighbors?direction=out&exclude_best_address_tag={str(exclude_best_address_tag).lower()}&pagesize=5"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("direction", ["in", "out"])
    def test_list_entity_txs_direction(self, direction):
        """Test list_entity_txs with direction parameter."""
        self.assert_endpoint_equal(
            f"btc/entities/{BTC_ENTITY}/txs?direction={direction}&pagesize=5"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("order", ["asc", "desc"])
    def test_list_entity_txs_order(self, order):
        """Test list_entity_txs with order parameter."""
        self.assert_endpoint_equal(
            f"btc/entities/{BTC_ENTITY}/txs?order={order}&pagesize=5"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("direction,order", [
        ("in", "asc"),
        ("in", "desc"),
        ("out", "asc"),
        ("out", "desc"),
    ])
    def test_list_entity_txs_direction_order(self, direction, order):
        """Test list_entity_txs with direction and order parameters."""
        self.assert_endpoint_equal(
            f"btc/entities/{BTC_ENTITY}/txs?direction={direction}&order={order}&pagesize=5"
        )

    @pytest.mark.migration
    def test_list_entity_txs_height_filter(self):
        """Test list_entity_txs with height filtering."""
        self.assert_endpoint_equal(
            f"btc/entities/{BTC_ENTITY}/txs?min_height=100000&max_height=200000&pagesize=5"
        )

    @pytest.mark.migration
    def test_list_entity_addresses_pagesize(self):
        """Test list_entity_addresses with pagesize parameter."""
        self.assert_endpoint_equal(f"btc/entities/{BTC_ENTITY}/addresses?pagesize=10")

    @pytest.mark.migration
    @pytest.mark.xfail(
        reason="Pagination without explicit ordering returns different items from database"
    )
    def test_list_address_tags_by_entity_pagesize(self):
        """Test list_address_tags_by_entity with pagesize parameter."""
        self.assert_endpoint_equal(f"btc/entities/{BTC_ENTITY}/tags?pagesize=10")


class TestTransactionParameters(MigrationTestBase):
    """Test transaction endpoints with various parameter configurations."""

    @pytest.mark.migration
    @pytest.mark.parametrize("include_io", [True, False])
    def test_get_tx_include_io(self, include_io):
        """Test get_tx with include_io parameter."""
        self.assert_endpoint_equal(
            f"btc/txs/{BTC_TX}?include_io={str(include_io).lower()}"
        )

    @pytest.mark.migration
    def test_get_tx_include_io_index(self):
        """Test get_tx with include_io and include_io_index parameters."""
        self.assert_endpoint_equal(
            f"btc/txs/{BTC_TX}?include_io=true&include_io_index=true"
        )

    @pytest.mark.migration
    def test_get_tx_include_nonstandard_io(self):
        """Test get_tx with include_io and include_nonstandard_io parameters."""
        self.assert_endpoint_equal(
            f"btc/txs/{BTC_TX}?include_io=true&include_nonstandard_io=true"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("io", ["inputs", "outputs"])
    def test_get_tx_io(self, io):
        """Test get_tx_io with inputs/outputs parameter."""
        self.assert_endpoint_equal(f"btc/txs/{BTC_TX}/{io}")

    @pytest.mark.migration
    @pytest.mark.parametrize("io", ["inputs", "outputs"])
    def test_get_tx_io_include_io_index(self, io):
        """Test get_tx_io with include_io_index parameter."""
        self.assert_endpoint_equal(f"btc/txs/{BTC_TX}/{io}?include_io_index=true")

    @pytest.mark.migration
    @pytest.mark.parametrize("io", ["inputs", "outputs"])
    def test_get_tx_io_include_nonstandard(self, io):
        """Test get_tx_io with include_nonstandard_io parameter."""
        self.assert_endpoint_equal(f"btc/txs/{BTC_TX}/{io}?include_nonstandard_io=true")


class TestTagsParameters(MigrationTestBase):
    """Test tags endpoints with various parameter configurations."""

    @pytest.mark.migration
    def test_list_taxonomies(self):
        """Test list_taxonomies endpoint."""
        self.assert_endpoint_equal("tags/taxonomies")

    @pytest.mark.migration
    def test_list_concepts(self):
        """Test list_concepts endpoint."""
        self.assert_endpoint_equal("tags/taxonomies/entity/concepts")

    @pytest.mark.migration
    def test_list_address_tags(self):
        """Test list_address_tags endpoint."""
        self.assert_endpoint_equal("tags?label=binance&pagesize=5")

    @pytest.mark.migration
    def test_list_address_tags_pagesize(self):
        """Test list_address_tags with different pagesize."""
        self.assert_endpoint_equal("tags?label=binance&pagesize=10")


class TestBlockParameters(MigrationTestBase):
    """Test block endpoints with various parameter configurations."""

    @pytest.mark.migration
    def test_get_block(self):
        """Test get_block endpoint."""
        self.assert_endpoint_equal(f"btc/blocks/{BTC_HEIGHT}")

    @pytest.mark.migration
    def test_list_block_txs(self):
        """Test list_block_txs endpoint."""
        self.assert_endpoint_equal(f"btc/blocks/{BTC_HEIGHT}/txs")

    @pytest.mark.migration
    def test_get_block_by_date(self):
        """Test get_block_by_date endpoint."""
        # Use ISO 8601 datetime format (required by old Connexion server)
        self.assert_endpoint_equal("btc/block_by_date/2012-01-01T00:00:00Z")


class TestBulkEndpoints(MigrationTestBase):
    """Test bulk endpoints for migration parity."""

    @pytest.mark.migration
    def test_bulk_json_get_address(self):
        """Test bulk JSON get_address endpoint."""
        body = {"address": [BTC_ADDRESS]}
        self.assert_post_endpoint_equal("btc/bulk.json/get_address?num_pages=1", body)

    @pytest.mark.migration
    def test_bulk_json_get_address_multiple(self):
        """Test bulk JSON get_address with multiple addresses."""
        body = {"address": [BTC_ADDRESS, "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"]}
        self.assert_post_endpoint_equal("btc/bulk.json/get_address?num_pages=1", body)

    @pytest.mark.migration
    def test_bulk_json_get_entity(self):
        """Test bulk JSON get_entity endpoint."""
        body = {"entity": [BTC_ENTITY]}
        self.assert_post_endpoint_equal("btc/bulk.json/get_entity?num_pages=1", body)

    @pytest.mark.migration
    def test_bulk_csv_get_address(self):
        """Test bulk CSV get_address endpoint returns valid CSV."""
        # For CSV, we just check that both servers return the same status
        # since CSV comparison is more complex
        body = {"address": [BTC_ADDRESS]}
        headers = {**HEADERS, "Authorization": "test"}

        old_url = urljoin(OLD_SERVER + "/", "btc/bulk.csv/get_address?num_pages=1")
        new_url = urljoin(NEW_SERVER + "/", "btc/bulk.csv/get_address?num_pages=1")

        old_response = requests.post(old_url, headers=headers, json=body, timeout=60)
        new_response = requests.post(new_url, headers=headers, json=body, timeout=60)

        assert old_response.status_code == new_response.status_code, (
            f"Status mismatch: {old_response.status_code} vs {new_response.status_code}"
        )


class TestMultiCurrency(MigrationTestBase):
    """Test endpoints across multiple currencies."""

    @pytest.mark.migration
    @pytest.mark.parametrize("currency,address", [
        ("btc", BTC_ADDRESS),
        ("eth", ETH_ADDRESS),
    ])
    def test_get_address_multi_currency(self, currency, address):
        """Test get_address across different currencies."""
        self.assert_endpoint_equal(f"{currency}/addresses/{address}")

    @pytest.mark.migration
    @pytest.mark.parametrize("currency", ["btc", "eth"])
    def test_supported_tokens_multi_currency(self, currency):
        """Test supported_tokens across different currencies."""
        self.assert_endpoint_equal(f"{currency}/supported_tokens/")


class TestPagination(MigrationTestBase):
    """Test pagination parameters."""

    @pytest.mark.migration
    @pytest.mark.parametrize("pagesize", [1, 5, 10, 25])
    def test_list_address_txs_pagesize(self, pagesize):
        """Test list_address_txs with various pagesize values."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}/txs?pagesize={pagesize}"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("pagesize", [1, 5, 10])
    def test_list_address_neighbors_pagesize(self, pagesize):
        """Test list_address_neighbors with various pagesize values."""
        self.assert_endpoint_equal(
            f"btc/addresses/{BTC_ADDRESS}/neighbors?direction=out&pagesize={pagesize}"
        )

    @pytest.mark.migration
    @pytest.mark.parametrize("pagesize", [1, 5, 10])
    def test_list_entity_neighbors_pagesize(self, pagesize):
        """Test list_entity_neighbors with various pagesize values."""
        self.assert_endpoint_equal(
            f"btc/entities/{BTC_ENTITY}/neighbors?direction=out&pagesize={pagesize}"
        )


if __name__ == "__main__":
    # Quick manual test
    check_servers_available()
    test = TestFastAPIMigrationBasic()
    test.setup()

    endpoints = [
        "stats",
        "search?q=binance&limit=5",
        f"btc/addresses/{BTC_ADDRESS}",
        f"btc/entities/{BTC_ENTITY}",
        f"btc/blocks/{BTC_HEIGHT}",
    ]

    for endpoint in endpoints:
        result = test.compare_endpoint(endpoint)
        status = "PASS" if not result["differences"] else "FAIL"
        print(f"{status}: {endpoint} (old={result['old_time']:.3f}s, new={result['new_time']:.3f}s)")
        if result["differences"]:
            for diff in result["differences"][:5]:
                print(f"  - {diff}")
