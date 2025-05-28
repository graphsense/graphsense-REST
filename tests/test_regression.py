import requests
from typing import Dict, Any
import logging
from urllib.parse import urljoin
import time
import os
import pytest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


new_endpoint = "http://localhost:8000"
current_endpoint = "https://api.ikna.io"
current_key = os.environ.get("GS_API_KEY")

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def get_data_from_current_endpoint(endpoint: str, key: str) -> Dict[str, Any]:
    """Get data from the current endpoint with API key authentication."""
    now = time.time()
    url = urljoin(current_endpoint, endpoint)
    auth_headers = {
        "Authorization": key,
        **headers
    }
    try:
        response = requests.get(url, headers=auth_headers)
        response.raise_for_status()
        print(f"current took {time.time() - now} seconds")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching from current endpoint: {e}")
        raise


def get_data_from_new_endpoint(endpoint: str) -> Dict[str, Any]:
    """Get data from the new endpoint without authentication."""
    now = time.time()
    url = urljoin(new_endpoint, endpoint)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"New took {time.time() - now} seconds")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching from new endpoint: {e}")
        raise


def compare_outputs(current_data: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[
    str, Any]:
    """Compare outputs with detailed differences."""
    result = {
        "are_equal": False,
        "differences": [],
        "current_keys": list(current_data.keys()),
        "new_keys": list(new_data.keys())
    }

    # Check for missing keys
    missing_in_new = set(result["current_keys"]) - set(result["new_keys"])
    missing_in_current = set(result["new_keys"]) - set(result["current_keys"])

    if missing_in_new:
        result["differences"].append(
            f"Keys missing in new data: {list(missing_in_new)}")
    if missing_in_current:
        result["differences"].append(
            f"Keys missing in current data: {list(missing_in_current)}")

    # Compare common keys
    common_keys = set(result["current_keys"]) & set(result["new_keys"])
    for key in common_keys:
        if current_data[key] != new_data[key]:
            # For lists, compare lengths and first few items if different
            if isinstance(current_data[key], list) and isinstance(new_data[key], list):
                if len(current_data[key]) != len(new_data[key]):
                    result["differences"].append(
                        f"List length difference in key '{key}': {len(current_data[key])} != {len(new_data[key])}"
                    )
                else:
                    # Compare first few items if lists are different
                    for i, (current_item, new_item) in enumerate(
                            zip(current_data[key][:5], new_data[key][:5])):
                        if current_item != new_item:
                            result["differences"].append(
                                f"First difference in key '{key}' at index {i}: {current_item} != {new_item}"
                            )
                            break
            else:
                result["differences"].append(
                    f"Difference in key '{key}': {current_data[key]} != {new_data[key]}")

    result["are_equal"] = len(result["differences"]) == 0
    return result


def compare_instances(call) -> Dict[str, Any]:
    """Test and compare outputs from both endpoints."""
    try:
        new_data = get_data_from_new_endpoint(call)
        current_data = get_data_from_current_endpoint(call, current_key)
        comparison = compare_outputs(current_data, new_data)

        return comparison
    except Exception as e:
        logger.error(f"Error during testing: {e}")
        raise

@pytest.mark.regression
def test_links():
    """Run the regression test and return the comparison result."""

    call_0 = "eth/entities/316592288/links?neighbor=31455019&pagesize=100"  # old 60-70s, new 2s
    call_2 = "eth/addresses/0x8ccec5bfb049af5dd2916853a14974b0a9f47e4d/links?neighbor=0x453290aaf6dca3cee4325bad3f52b1346b6213a7&pagesize=100"  # old time: 17, new 0.6
    call_5 = "eth/entities/225414228/links?neighbor=229413023&pagesize=100"  # works
    call_6 = "eth/entities/276182118/links?neighbor=81071666&pagesize=100"  # old time 45s 3.5 seconds new
    call_7 = "eth/entities/225414228/links?neighbor=31455019&pagesize=100"  # 2 huge addresses
    call_8 = "btc/entities/2647118/links?neighbor=109578&pagesize=100"  # btc
    calls = [
        call_0, call_2, call_5, call_6, call_7, call_8
    ]
    for call in calls:
        logger.info(f"Testing call: {call}")
        comparison = compare_instances(call)
        assert comparison["are_equal"], f"Outputs differ for call: {call}, {comparison['differences']}"


@pytest.mark.regression
def test_txs_list():
    """Run the regression test and return the comparison result."""

    call_1 = "eth/addresses/0x10c318b1d817396a8a66016438ac9dfb615ffcf1/txs?pagesize=100&min_height=7957441&order=desc"  # 6 -> 1
    call_3 = "eth/addresses/0xdac17f958d2ee523a2206206994597c13d831ec7/txs?min_height=20698064&max_height=22567324&order=asc&pagesize=5"  # 1.3 -> 0.2
    call_4 = "eth/addresses/0x255c0dc1567739ceb2c8cd0fddcf1706563868d0/txs?pagesize=1"  # old time: 0.37s, new 0.12s
    calls = [
        call_1, call_3, call_4
    ]
    for call in calls:
        logger.info(f"Testing call: {call}")
        comparison = compare_instances(call)
        assert comparison["are_equal"], f"Outputs differ for call: {call}"
