#!/bin/bash
# Migration test runner script
# Starts both old and new servers, runs comparison tests, and cleans up

set -e

WORKTREE_DIR="${1:-.graphsense-rest-old}"
OLD_PORT="${2:-9001}"
NEW_PORT="${3:-9003}"  # adev uses OLD_PORT+1 for aux server, so we skip 9002
TIMEOUT="${4:-60}"

OLD_PID=""
NEW_PID=""

kill_port() {
    local port=$1
    # Try fuser first
    if command -v fuser &> /dev/null; then
        fuser -k "$port/tcp" 2>/dev/null || true
    fi
    # Also try lsof + kill as fallback
    if command -v lsof &> /dev/null; then
        local pids=$(lsof -ti :"$port" 2>/dev/null || true)
        if [ -n "$pids" ]; then
            echo "$pids" | xargs kill -9 2>/dev/null || true
        fi
    fi
}

cleanup() {
    echo ""
    echo "Cleaning up..."
    if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
        echo "Stopping old server (PID $OLD_PID)..."
        kill "$OLD_PID" 2>/dev/null || true
        sleep 1
        kill -9 "$OLD_PID" 2>/dev/null || true
    fi
    if [ -n "$NEW_PID" ] && kill -0 "$NEW_PID" 2>/dev/null; then
        echo "Stopping new server (PID $NEW_PID)..."
        kill "$NEW_PID" 2>/dev/null || true
        sleep 1
        kill -9 "$NEW_PID" 2>/dev/null || true
    fi
    # Kill any remaining processes on the ports
    kill_port "$OLD_PORT"
    kill_port "$NEW_PORT"
}

trap cleanup EXIT INT TERM

wait_for_server() {
    local url=$1
    local name=$2
    local max_attempts=$3
    local attempt=1

    echo "Waiting for $name at $url..."
    while [ $attempt -le $max_attempts ]; do
        if curl -s -o /dev/null -w "%{http_code}" "$url/stats" 2>/dev/null | grep -q "200\|401\|403"; then
            echo "$name is ready!"
            return 0
        fi
        echo "  Attempt $attempt/$max_attempts..."
        sleep 2
        attempt=$((attempt + 1))
    done
    echo "ERROR: $name failed to start after $max_attempts attempts"
    return 1
}

echo "=========================================="
echo "Migration Test Pipeline"
echo "=========================================="
echo "Old server: http://localhost:$OLD_PORT (from $WORKTREE_DIR)"
echo "New server: http://localhost:$NEW_PORT (current branch)"
echo ""

# Check if ports are already in use and kill any existing processes
echo "Checking ports..."
for port in "$OLD_PORT" "$NEW_PORT"; do
    if lsof -ti :"$port" &>/dev/null || fuser "$port/tcp" &>/dev/null; then
        echo "WARNING: Port $port already in use, killing existing process..."
        kill_port "$port"
        sleep 2
    fi
done

# Start old server
echo "Starting old server..."
cd "$WORKTREE_DIR"
uv run adev runserver -p "$OLD_PORT" --root . --app-factory main gsrest/__init__.py > /tmp/old_server.log 2>&1 &
OLD_PID=$!
cd - > /dev/null

# Give old server time to bind its port
sleep 2

# Start new server
echo "Starting new server..."
uv run uvicorn gsrest.app:create_app --factory --host localhost --port "$NEW_PORT" > /tmp/new_server.log 2>&1 &
NEW_PID=$!

# Give servers time to start
sleep 2

# Wait for servers to be ready
if ! wait_for_server "http://localhost:$OLD_PORT" "Old server" 30; then
    echo "Old server logs:"
    tail -50 /tmp/old_server.log
    exit 1
fi

if ! wait_for_server "http://localhost:$NEW_PORT" "New server" 30; then
    echo "New server logs:"
    tail -50 /tmp/new_server.log
    exit 1
fi

echo ""
echo "=========================================="
echo "Running migration tests..."
echo "=========================================="
echo ""

# Run the tests
OLD_SERVER="http://localhost:$OLD_PORT" \
NEW_SERVER="http://localhost:$NEW_PORT" \
uv run pytest tests/test_fastapi_migration.py -v -m migration --tb=short

TEST_EXIT_CODE=$?

echo ""
echo "=========================================="
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "Migration tests PASSED"
else
    echo "Migration tests FAILED (exit code: $TEST_EXIT_CODE)"
fi
echo "=========================================="

exit $TEST_EXIT_CODE
