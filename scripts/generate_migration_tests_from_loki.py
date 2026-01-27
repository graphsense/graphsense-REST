#!/usr/bin/env python3
"""
Generate migration test cases from Loki API gateway logs.

This script fetches successful API calls from Loki and creates a dataset
that can be used to verify the FastAPI migration produces identical results.

Usage:
    uv run scripts/generate_migration_tests_from_loki.py

    # With custom options
    uv run scripts/generate_migration_tests_from_loki.py --hours 48 --limit 1000 --output tests/loki_calls.json

Environment:
    LOKI_URL: Loki endpoint (required, e.g. http://loki.example.com:3100)
"""

import argparse
import json
import logging
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

LOKI_URL = os.environ.get("LOKI_URL", "")

# Endpoints to exclude (health checks, metrics, scanner noise, etc.)
EXCLUDE_PATTERNS = [
    r"^/health",
    r"^/metrics",
    r"^/openapi",
    r"^/docs",
    r"^/ui",  # Swagger UI - returns HTML
    r"^/favicon",
    r"^/$",
    # Scanner noise - match anywhere in path
    r"/\.env",  # .env files anywhere
    r"wp-includes",  # WordPress
    r"wp-content",
    r"wp-admin",
    r"wordpress",
    r"WordPress",
    r"/actuator",  # Spring Boot
    r"wlwmanifest",
    r"\.php",
    r"\.asp",
    r"\.aspx",
    r"\.cgi",
    r"\.xml$",
    r"^/cgi-bin",
    r"^/shell",
    r"^/eval",
    r"^/\.",  # Hidden files/dirs like /.git, /.env, /.trash
    r"^/sitemap",
    r"^/swagger\.json",
    r"^/robots",
    r"^/admin",
    r"^/backend",
    r"^/api/\.",  # /api/.env etc
    r"^/app/\.",  # /app/.env etc
    # Static files and more scanner noise
    r"swagger-ui",
    r"\.js$",
    r"\.css$",
    r"\.map$",
    r"\.ico$",
    r"\.png$",
    r"\.jpg$",
    r"\.gif$",
    r"\.woff",
    r"\.ttf$",
    r"\.eot$",
    r"\.svg$",
    # Malformed paths with quotes or special chars
    r'"',  # URIs containing quotes
    r"'",  # URIs containing single quotes
    r"<",  # URIs containing HTML
    r">",
    r"\|",  # Pipe chars
    r"\\\\",  # Backslashes
]

# Max examples per endpoint pattern to avoid too many similar calls
MAX_EXAMPLES_PER_PATTERN = 25


def fetch_loki_logs(
    hours: int = 24, limit: int = 5000, loki_url: str = LOKI_URL
) -> list[dict]:
    """Fetch logs from Loki with pagination support for large datasets."""
    from datetime import timedelta

    query = '{service="apisix-gateway"}'
    url = f"{loki_url}/loki/api/v1/query_range"

    # Loki has a 5000 limit per request - fetch in batches if needed
    batch_size = 5000
    total_fetched = 0
    all_results = []

    # Calculate time range
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)

    # Convert to nanoseconds (Loki uses nanosecond timestamps)
    current_end = int(end_time.timestamp() * 1e9)
    start_ns = int(start_time.timestamp() * 1e9)

    log.info(f"Fetching logs from Loki: {url}")
    log.info(f"  Query: {query}")
    log.info(
        f"  Time range: last {hours} hours ({start_time.isoformat()} to {end_time.isoformat()})"
    )
    log.info(f"  Target limit: {limit}")

    batch_num = 0
    while total_fetched < limit:
        batch_num += 1
        remaining = limit - total_fetched
        batch_limit = min(batch_size, remaining)

        params = {
            "query": query,
            "start": str(start_ns),
            "end": str(current_end),
            "limit": str(batch_limit),
            "direction": "backward",  # Most recent first
        }

        log.info(f"  Batch {batch_num}: fetching up to {batch_limit} entries...")
        response = requests.get(url, params=params, timeout=300)
        response.raise_for_status()

        batch_data = response.json()
        results = batch_data.get("data", {}).get("result", [])

        if not results:
            log.info(f"  Batch {batch_num}: no more results")
            break

        # Count entries in this batch
        batch_entries = sum(len(stream.get("values", [])) for stream in results)
        if batch_entries == 0:
            log.info(f"  Batch {batch_num}: no entries in results")
            break

        all_results.extend(results)
        total_fetched += batch_entries
        log.info(
            f"  Batch {batch_num}: got {batch_entries} entries (total: {total_fetched})"
        )

        # Find oldest timestamp in this batch to continue from
        oldest_ts = None
        for stream in results:
            for entry in stream.get("values", []):
                ts = int(entry[0])
                if oldest_ts is None or ts < oldest_ts:
                    oldest_ts = ts

        if oldest_ts is None or oldest_ts <= start_ns:
            log.info("  Reached start of time range")
            break

        # Move end time to just before the oldest entry we got
        current_end = oldest_ts - 1

        # Safety check - if we got fewer than requested, we've exhausted the data
        if batch_entries < batch_limit:
            log.info("  Batch returned fewer entries than limit, stopping")
            break

    log.info(f"Total entries fetched: {total_fetched}")

    # Return in the same format as a single query
    return {"data": {"result": all_results}}


def parse_log_entry(entry: dict) -> dict | None:
    """Parse a single log entry to extract API call info."""
    # Loki returns entries as [timestamp, log_line]
    # The log_line should be JSON from apisix
    timestamp, log_line = entry

    # Parse JSON - handle potential parse errors
    try:
        parsed = json.loads(log_line)
    except json.JSONDecodeError:
        return None

    # Filter for GraphSense REST API routes only
    route_name = parsed.get("route_name", "")
    server_host = parsed.get("server_host", "")

    # Only include gs-rest routes on api.* hosts
    if "gs-rest" not in route_name:
        return None
    if not server_host.startswith("api."):
        return None

    # Extract relevant fields from apisix log format
    # Common fields: request, upstream_uri, uri, method, status, etc.
    uri = parsed.get("uri") or parsed.get("request_uri") or parsed.get("upstream_uri")
    method = parsed.get("method", "GET")
    status = parsed.get("status")

    # Convert status to int if it's a string
    if isinstance(status, str):
        status = int(status)

    if not uri:
        return None

    # Skip non-GET requests for now (POST/bulk will need special handling)
    if method != "GET":
        return None

    # Skip excluded patterns (use search for patterns that can appear anywhere)
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, uri):
            return None

    return {
        "uri": uri,
        "method": method,
        "status": status or 200,
        "timestamp": timestamp,
        "host": server_host,
        "latency": parsed.get("latency"),
    }


def normalize_uri(uri: str) -> tuple[str, str]:
    """
    Normalize a URI to a pattern and return (pattern, original_uri).

    Replaces specific values with placeholders to group similar endpoints.
    """
    parsed = urlparse(uri)
    path = parsed.path

    # Patterns for path normalization
    replacements = [
        # BTC addresses (various formats)
        (
            r"/addresses/[13][a-km-zA-HJ-NP-Z1-9]{25,34}(?=/|$)",
            "/addresses/{btc_address}",
        ),
        (r"/addresses/bc1[a-z0-9]{39,59}(?=/|$)", "/addresses/{btc_bech32_address}"),
        # ETH/TRX addresses
        (r"/addresses/0x[a-fA-F0-9]{40}(?=/|$)", "/addresses/{eth_address}"),
        (r"/addresses/T[a-zA-Z0-9]{33}(?=/|$)", "/addresses/{trx_address}"),
        # Entity IDs
        (r"/entities/\d+(?=/|$)", "/entities/{entity_id}"),
        # Transaction hashes
        (r"/txs/0x[a-fA-F0-9]{64}(?=/|$)", "/txs/{eth_tx_hash}"),
        (r"/txs/[a-fA-F0-9]{64}(?=/|$)", "/txs/{tx_hash}"),
        # Block heights
        (r"/blocks/\d+(?=/|$)", "/blocks/{height}"),
        # Rates
        (r"/rates/\d+(?=/|$)", "/rates/{height}"),
        # Block by date
        (r"/block_by_date/[^/]+(?=/|$)", "/block_by_date/{date}"),
        # Actors
        (r"/actors/[^/]+(?=/|$)", "/actors/{actor}"),
        # Taxonomy concepts
        (r"/taxonomies/[^/]+/concepts", "/taxonomies/{taxonomy}/concepts"),
    ]

    pattern = path
    for regex, replacement in replacements:
        pattern = re.sub(regex, replacement, pattern)

    return pattern, uri


def extract_endpoint_calls(loki_data: dict) -> list[dict]:
    """Extract and deduplicate API calls from Loki response."""
    results = loki_data.get("data", {}).get("result", [])

    calls = []
    seen = set()

    for stream in results:
        values = stream.get("values", [])
        for entry in values:
            parsed = parse_log_entry(entry)
            if parsed:
                # Deduplicate exact URIs
                if parsed["uri"] not in seen:
                    seen.add(parsed["uri"])
                    calls.append(parsed)

    return calls


def group_by_pattern(calls: list[dict]) -> dict[str, list[dict]]:
    """Group calls by their normalized pattern and status code category."""
    grouped = defaultdict(list)

    for call in calls:
        pattern, _ = normalize_uri(call["uri"])
        # Group by pattern + status category (2xx, 4xx, 5xx)
        status = call.get("status", 200)
        status_category = f"{status // 100}xx"
        key = f"{pattern} [{status_category}]"
        grouped[key].append(call)

    return grouped


def group_by_pattern_only(calls: list[dict]) -> dict[str, list[dict]]:
    """Group calls by their normalized pattern only (for summary stats)."""
    grouped = defaultdict(list)

    for call in calls:
        pattern, _ = normalize_uri(call["uri"])
        grouped[pattern].append(call)

    return grouped


def select_representative_calls(
    grouped: dict[str, list[dict]], max_per_pattern: int = MAX_EXAMPLES_PER_PATTERN
) -> list[dict]:
    """Select representative calls from each pattern group."""
    selected = []

    for pattern_key, calls in sorted(grouped.items()):
        # Sort by timestamp (most recent first) and take first N
        sorted_calls = sorted(calls, key=lambda x: x["timestamp"], reverse=True)

        # Take diverse examples if possible (different query params)
        seen_params = set()
        for call in sorted_calls:
            parsed = urlparse(call["uri"])
            param_keys = frozenset(parse_qs(parsed.query).keys())

            if param_keys not in seen_params or len(seen_params) < max_per_pattern:
                seen_params.add(param_keys)
                selected.append(
                    {
                        "pattern": pattern_key,
                        "uri": call["uri"],
                        "method": call["method"],
                        "status": call.get("status", 200),
                    }
                )

                if (
                    len([s for s in selected if s["pattern"] == pattern_key])
                    >= max_per_pattern
                ):
                    break

    return selected


def generate_pytest_file(calls: list[dict], output_path: Path):
    """Generate a pytest file from the collected calls."""
    # Group by pattern for parametrized tests
    by_pattern = defaultdict(list)
    for call in calls:
        by_pattern[call["pattern"]].append((call["uri"], call.get("status", 200)))

    lines = [
        '"""',
        "Auto-generated migration tests from Loki API logs.",
        "",
        f"Generated at: {datetime.now().isoformat()}",
        f"Total endpoints: {len(calls)}",
        f"Unique patterns: {len(by_pattern)}",
        "",
        "These tests verify that both old and new servers return the same",
        "responses (both successful and error cases) for real production API calls.",
        '"""',
        "",
        "import pytest",
        "from tests.test_fastapi_migration import MigrationTestBase",
        "",
        "",
        "class TestLokiGeneratedCalls(MigrationTestBase):",
        '    """Tests generated from production API call logs."""',
        "",
    ]

    for pattern, uri_status_pairs in sorted(by_pattern.items()):
        # Create a safe test name from pattern
        test_name = pattern.replace("/", "_").replace("{", "").replace("}", "")
        test_name = re.sub(r"[^a-zA-Z0-9_]", "_", test_name)
        test_name = re.sub(r"_+", "_", test_name).strip("_")

        if len(uri_status_pairs) == 1:
            # Single URI - simple test
            uri, expected_status = uri_status_pairs[0]
            lines.extend(
                [
                    "    @pytest.mark.migration",
                    "    @pytest.mark.loki_generated",
                    f"    def test_{test_name}(self):",
                    f'        """Test {pattern} (expected status: {expected_status})"""',
                    f'        self.assert_endpoint_equal("{uri}")',
                    "",
                ]
            )
        else:
            # Multiple URIs - parametrized test
            lines.extend(
                [
                    "    @pytest.mark.migration",
                    "    @pytest.mark.loki_generated",
                    "    @pytest.mark.parametrize('uri,expected_status', [",
                ]
            )
            for uri, expected_status in uri_status_pairs:
                lines.append(f'        ("{uri}", {expected_status}),')
            lines.extend(
                [
                    "    ])",
                    f"    def test_{test_name}(self, uri, expected_status):",
                    f'        """Test {pattern}"""',
                    "        # Note: expected_status from production logs",
                    "        # Both servers should return same status (not necessarily expected_status)",
                    "        self.assert_endpoint_equal(uri)",
                    "",
                ]
            )

    output_path.write_text("\n".join(lines))
    log.info(f"Generated pytest file: {output_path}")


def generate_json_dataset(calls: list[dict], output_path: Path):
    """Generate a JSON dataset of calls."""
    output_path.write_text(json.dumps(calls, indent=2))
    log.info(f"Generated JSON dataset: {output_path}")


def log_summary(calls: list[dict], grouped: dict[str, list[dict]]):
    """Log a summary of collected calls."""
    # Get pattern-only grouping for cleaner stats
    patterns_only = group_by_pattern_only(calls)

    log.info("\n" + "=" * 60)
    log.info("SUMMARY")
    log.info("=" * 60)
    log.info(f"Total unique API calls: {len(calls)}")
    log.info(f"Unique endpoint patterns: {len(patterns_only)}")
    log.info(f"Pattern + status combinations: {len(grouped)}")
    log.info("")

    log.info("Status code distribution:")
    status_counts = Counter()
    for call in calls:
        status = call.get("status", 200)
        status_counts[status] += 1
    for status, count in sorted(status_counts.items()):
        log.info(f"  {count:4d}  HTTP {status}")

    log.info("")
    log.info("Top patterns by call count:")
    pattern_counts = [(p, len(c)) for p, c in patterns_only.items()]
    for pattern, count in sorted(pattern_counts, key=lambda x: -x[1])[:20]:
        log.info(f"  {count:4d}  {pattern}")

    log.info("")
    log.info("Currency distribution:")
    currencies = Counter()
    for call in calls:
        path = urlparse(call["uri"]).path
        parts = path.strip("/").split("/")
        if parts and parts[0] in ["btc", "eth", "trx", "ltc", "bch", "zec"]:
            currencies[parts[0]] += 1
        elif parts and parts[0] in ["search", "stats", "tags"]:
            currencies["general"] += 1
        else:
            currencies["other"] += 1

    for currency, count in currencies.most_common():
        log.info(f"  {count:4d}  {currency}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate migration test cases from Loki API logs"
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Hours of logs to fetch (default: 24)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5000,
        help="Max log entries to fetch (default: 5000)",
    )
    parser.add_argument(
        "--max-per-pattern",
        type=int,
        default=MAX_EXAMPLES_PER_PATTERN,
        help=f"Max examples per endpoint pattern (default: {MAX_EXAMPLES_PER_PATTERN})",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("tests/loki_generated_calls.json"),
        help="Output JSON file path",
    )
    parser.add_argument(
        "--output-pytest",
        type=Path,
        default=Path("tests/test_loki_generated.py"),
        help="Output pytest file path",
    )
    parser.add_argument(
        "--loki-url",
        default=LOKI_URL,
        help="Loki URL (or set LOKI_URL env var)",
    )

    args = parser.parse_args()

    # Validate Loki URL
    if not args.loki_url:
        log.error("Error: Loki URL is required.")
        log.error("Set LOKI_URL environment variable or use --loki-url argument.")
        sys.exit(1)

    # Fetch logs from Loki
    log.info("Fetching logs from Loki...")
    loki_data = fetch_loki_logs(
        hours=args.hours, limit=args.limit, loki_url=args.loki_url
    )

    # Extract API calls
    log.info("Extracting API calls...")
    calls = extract_endpoint_calls(loki_data)
    log.info(f"Found {len(calls)} unique API calls")

    if not calls:
        log.error("No API calls found. Check your Loki query and connection.")
        sys.exit(1)

    # Group by pattern
    grouped = group_by_pattern(calls)
    log.info(f"Grouped into {len(grouped)} endpoint patterns")

    # Select representative calls
    selected = select_representative_calls(
        grouped, max_per_pattern=args.max_per_pattern
    )
    log.info(f"Selected {len(selected)} representative calls for testing")

    # Log summary
    log_summary(calls, grouped)

    # Generate outputs
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_pytest.parent.mkdir(parents=True, exist_ok=True)

    generate_json_dataset(selected, args.output_json)
    generate_pytest_file(selected, args.output_pytest)

    log.info("")
    log.info("Next steps:")
    log.info("  1. Review the generated files")
    log.info("  2. Start both servers:")
    log.info("     OLD_SERVER: make serve-old  # or your old server")
    log.info(
        "     NEW_SERVER: uv run uvicorn gsrest.app:create_app --factory --port 9002"
    )
    log.info("  3. Run the tests:")
    log.info("     uv run pytest tests/test_loki_generated.py -v -m loki_generated")


if __name__ == "__main__":
    main()
