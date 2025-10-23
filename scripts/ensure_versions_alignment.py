#!/usr/bin/env python3
# ruff: noqa: T201
"""
Script to ensure version alignment across multiple files in the GraphSense REST project.

This script checks versions in:
- pyproject.toml (root)
- clients/python/pyproject.toml
- openapi_spec/graphsense.yaml
- openapi_server/openapi/openapi.yaml

Exits with non-zero code if versions are misaligned.
"""

import re
import sys
from pathlib import Path

files = [
    Path("pyproject.toml"),
    Path("clients/python/pyproject.toml"),
    Path("openapi_spec/graphsense.yaml"),
    Path("openapi_server/openapi/openapi.yaml"),
    Path("Makefile"),
]

regex_patterns = {
    r"pyproject\.toml$": r'version\s*=\s*"([^"\n]+)"$',
    r"graphsense\.yaml$": r'version:\s*"([^"\n]+)"$',
    r"openapi\.yaml$": r"version:\s*([^\n]+)$",
    r"Makefile$": r'GS_REST_SERVICE_VERSION\s*\?=\s*"([^"\n]+)"$',
}


def main():
    versions = {}

    for file in files:
        if not file.exists():
            print(f"Error: {file} does not exist.")
            sys.exit(1)

        text = file.read_text()

        matched = False
        for path_pattern, version_pattern in regex_patterns.items():
            if re.search(path_pattern, str(file)):
                match = re.search(version_pattern, text, re.MULTILINE)
                if match:
                    version = match.group(1).strip()
                    print(f"Found version {version} in {file}")
                    versions[file] = version
                    matched = True
                    break
                else:
                    print(f"Error: No version found in {file}")
                    sys.exit(1)

        if not matched:
            print("Error: No pattern matched for {file}")
            sys.exit(1)

    # Check if all versions are the same
    unique_versions = set(versions.values())

    if len(unique_versions) == 1:
        print(f"\n✓ All versions are aligned: {list(unique_versions)[0]}")
        sys.exit(0)
    else:
        print("\n✗ Version mismatch detected!")
        print(f"Found {len(unique_versions)} different versions:")
        for file, version in versions.items():
            print(f"  {file}: {version}")
        sys.exit(1)


if __name__ == "__main__":
    main()
