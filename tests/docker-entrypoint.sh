#!/usr/bin/env bash
set -e

exec /usr/bin/find /src -type f -name "*.py" | entr $@
