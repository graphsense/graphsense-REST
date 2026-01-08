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


class TestFastAPIMigration:
    """Compare FastAPI responses against original aiohttp/Connexion version."""

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

    # === Test Cases ===

    @pytest.mark.migration
    def test_stats(self):
        """Test /stats endpoint."""
        self.assert_endpoint_equal("stats")

    @pytest.mark.migration
    def test_search(self):
        """Test /search endpoint."""
        self.assert_endpoint_equal("search?q=binance&limit=5")

    @pytest.mark.migration
    def test_get_address_btc(self):
        """Test BTC address endpoint."""
        self.assert_endpoint_equal("btc/addresses/1Archive1n2C579dMsAu3iC6tWzuQJz8dN")

    @pytest.mark.migration
    def test_get_address_eth(self):
        """Test ETH address endpoint."""
        self.assert_endpoint_equal("eth/addresses/0xdac17f958d2ee523a2206206994597c13d831ec7")

    @pytest.mark.migration
    def test_get_entity_btc(self):
        """Test BTC entity endpoint."""
        self.assert_endpoint_equal("btc/entities/109578")

    @pytest.mark.migration
    def test_get_block(self):
        """Test block endpoint."""
        self.assert_endpoint_equal("btc/blocks/100000")

    @pytest.mark.migration
    def test_get_tx(self):
        """Test transaction endpoint."""
        self.assert_endpoint_equal(
            "btc/txs/4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
        )

    @pytest.mark.migration
    def test_get_exchange_rates(self):
        """Test exchange rates endpoint."""
        self.assert_endpoint_equal("btc/rates/100000")

    @pytest.mark.migration
    def test_list_address_txs(self):
        """Test address transactions endpoint."""
        self.assert_endpoint_equal(
            "btc/addresses/1Archive1n2C579dMsAu3iC6tWzuQJz8dN/txs?pagesize=5"
        )

    @pytest.mark.migration
    def test_list_address_neighbors(self):
        """Test address neighbors endpoint."""
        self.assert_endpoint_equal(
            "btc/addresses/1Archive1n2C579dMsAu3iC6tWzuQJz8dN/neighbors?direction=out&pagesize=5"
        )

    @pytest.mark.migration
    def test_list_entity_addresses(self):
        """Test entity addresses endpoint."""
        self.assert_endpoint_equal("btc/entities/109578/addresses?pagesize=5")

    @pytest.mark.migration
    def test_list_entity_neighbors(self):
        """Test entity neighbors endpoint."""
        self.assert_endpoint_equal("btc/entities/109578/neighbors?direction=out&pagesize=5")

    @pytest.mark.migration
    def test_list_tags_by_address(self):
        """Test address tags endpoint."""
        self.assert_endpoint_equal(
            "btc/addresses/1Archive1n2C579dMsAu3iC6tWzuQJz8dN/tags"
        )

    @pytest.mark.migration
    def test_list_taxonomies(self):
        """Test taxonomies endpoint."""
        self.assert_endpoint_equal("tags/taxonomies")

    @pytest.mark.migration
    def test_supported_tokens(self):
        """Test supported tokens endpoint."""
        self.assert_endpoint_equal("eth/supported_tokens/")


class TestFastAPIMigrationBulk:
    """Test bulk endpoints for migration parity."""

    @pytest.fixture(autouse=True)
    def setup(self):
        check_servers_available()

    def compare_bulk_endpoint(self, endpoint: str, body: dict, auth: str = "test") -> dict:
        """Compare a bulk POST endpoint between old and new servers."""
        headers = {**HEADERS, "Authorization": auth}

        old_url = urljoin(OLD_SERVER + "/", endpoint.lstrip("/"))
        new_url = urljoin(NEW_SERVER + "/", endpoint.lstrip("/"))

        start = time.time()
        old_response = requests.post(old_url, headers=headers, json=body, timeout=60)
        old_time = time.time() - start

        start = time.time()
        new_response = requests.post(new_url, headers=headers, json=body, timeout=60)
        new_time = time.time() - start

        result = {
            "endpoint": endpoint,
            "old_status": old_response.status_code,
            "new_status": new_response.status_code,
            "old_time": old_time,
            "new_time": new_time,
            "differences": [],
        }

        if old_response.status_code != new_response.status_code:
            result["differences"].append(
                f"Status code mismatch: {old_response.status_code} vs {new_response.status_code}"
            )
        elif old_response.status_code == 200:
            old_data = old_response.json()
            new_data = new_response.json()
            old_normalized = normalize_response(old_data)
            new_normalized = normalize_response(new_data)
            result["differences"] = compare_responses(old_normalized, new_normalized)

        return result

    @pytest.mark.migration
    def test_bulk_json_get_address(self):
        """Test bulk JSON get_address endpoint."""
        body = {"address": ["1Archive1n2C579dMsAu3iC6tWzuQJz8dN"]}
        # Note: num_pages is required by old server, FastAPI has default
        result = self.compare_bulk_endpoint("btc/bulk.json/get_address?num_pages=1", body)

        logger.info(f"  bulk get_address: old={result['old_time']:.3f}s, new={result['new_time']:.3f}s")

        if result["differences"]:
            diff_str = "\n  ".join(result["differences"][:10])
            pytest.fail(f"Bulk endpoint has differences:\n  {diff_str}")


if __name__ == "__main__":
    # Quick manual test
    check_servers_available()
    test = TestFastAPIMigration()
    test.setup()

    endpoints = [
        "stats",
        "search?q=binance&limit=5",
        "btc/addresses/1Archive1n2C579dMsAu3iC6tWzuQJz8dN",
        "btc/entities/109578",
        "btc/blocks/100000",
    ]

    for endpoint in endpoints:
        result = test.compare_endpoint(endpoint)
        status = "PASS" if not result["differences"] else "FAIL"
        print(f"{status}: {endpoint} (old={result['old_time']:.3f}s, new={result['new_time']:.3f}s)")
        if result["differences"]:
            for diff in result["differences"][:5]:
                print(f"  - {diff}")
