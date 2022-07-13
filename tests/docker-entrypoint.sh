#!/usr/bin/env bash
set -e

exec /usr/bin/find /src/gsrest -type f -name "*.py" | entr $@
