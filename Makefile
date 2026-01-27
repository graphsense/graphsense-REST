all: format lint

-include .env

GS_REST_SERVICE_VERSIONM ?= "25.12.0rc2"
GS_REST_SERVICE_VERSION ?= "1.16.0rc2"

GS_REST_DEV_PORT ?= 9000
NUM_WORKERS ?= 1
NUM_THREADS ?= 1

# Migration test settings
OLD_SERVER_PORT ?= 9001
NEW_SERVER_PORT ?= 9003  # Note: adev uses OLD_SERVER_PORT+1 for aux/livereload server
MIGRATION_BASE_REF ?= master
WORKTREE_DIR ?= ../.graphsense-rest-old

test: install-dev
	uv run pytest -x -rx -vv

test-reset-cassandra-image:
	docker rmi graphsense/cassandra-test:4.1.4

test-regression:
	@export SKIP_REST_CONTAINER_SETUP=True && uv run pytest -m "regression" -s

# Migration testing targets
test-migration: setup-migration-worktree
	@echo "Starting migration test pipeline..."
	@./scripts/run_migration_tests.sh $(WORKTREE_DIR) $(OLD_SERVER_PORT) $(NEW_SERVER_PORT)

setup-migration-worktree:
	@if [ ! -d "$(WORKTREE_DIR)" ]; then \
		echo "Creating worktree for $(MIGRATION_BASE_REF) at $(WORKTREE_DIR)..."; \
		git worktree add $(WORKTREE_DIR) $(MIGRATION_BASE_REF); \
	else \
		echo "Worktree already exists at $(WORKTREE_DIR)"; \
		cd $(WORKTREE_DIR) && git checkout $(MIGRATION_BASE_REF) && git pull origin $(MIGRATION_BASE_REF) 2>/dev/null || true; \
	fi
	@cd $(WORKTREE_DIR) && uv sync --all-extras --dev
	@if [ -f "instance/config.yaml" ] && [ ! -e "$(WORKTREE_DIR)/instance/config.yaml" ]; then \
		echo "Symlinking config.yaml to worktree..."; \
		mkdir -p "$(WORKTREE_DIR)/instance"; \
		ln -sf "$(PWD)/instance/config.yaml" "$(WORKTREE_DIR)/instance/config.yaml"; \
	fi

clean-migration-worktree:
	@if [ -d "$(WORKTREE_DIR)" ]; then \
		echo "Removing worktree at $(WORKTREE_DIR)..."; \
		git worktree remove $(WORKTREE_DIR) --force; \
	fi

serve-old:
	@echo "Starting old server on port $(OLD_SERVER_PORT)..."
	cd $(WORKTREE_DIR) && GS_REST_DEV_PORT=$(OLD_SERVER_PORT) uv run adev runserver -p $(OLD_SERVER_PORT) --root . --app-factory main gsrest/__init__.py

serve-new:
	@echo "Starting new server on port $(NEW_SERVER_PORT)..."
	uv run uvicorn gsrest.app:create_app --factory --host localhost --port $(NEW_SERVER_PORT)

lint:
	uv run ruff check .

format:
	uv run ruff check --select I --fix
	uv run ruff format

install-dev:
	uv sync --all-extras --dev --force-reinstall

pre-commit:
	uv run pre-commit run --all-files

serve:
	uv run uvicorn gsrest.app:create_app --factory --host localhost --port ${GS_REST_DEV_PORT} --reload

build-docker:
	docker build -t graphsense-rest .

serve-docker:
	docker run --rm -it --network='host' -e NUM_THREADS=1 -e NUM_WORKERS=1 -v "${PWD}/instance/config.yaml:/config.yaml:Z" -e CONFIG_FILE=/config.yaml graphsense-rest:latest

run-codegen: generate-python-client

generate-python-client: update-package-version
	cd clients/python; make generate-openapi-client

run-designer:
	docker run --rm -d -p 8080:8080 swaggerapi/swagger-editor
	echo 'Designer UI is running on port 8080'

update-package-version:
	sed -i -r 's/(version = ).*/\1$(GS_REST_SERVICE_VERSION)/' pyproject.toml
	sed -i -r 's/(version = ).*/\1$(GS_REST_SERVICE_VERSION)/' clients/python/pyproject.toml

ensure-versions-alignment:
	python scripts/ensure_versions_alignment.py

tag-version: ensure-versions-alignment
	-git diff --exit-code && git diff --staged --exit-code && git tag -a v$(GS_REST_SERVICE_VERSIONM) -m 'Release v$(GS_REST_SERVICE_VERSION)' || (echo "Repo is dirty please commit first" && exit 1)
	git diff --exit-code && git diff --staged --exit-code && git tag -a v$(GS_REST_SERVICE_VERSION) -m 'Release v$(GS_REST_SERVICE_VERSION)' || (echo "Repo is dirty please commit first" && exit 1)

.PHONY: format lint test ensure-versions-alignment run-codegen serve serve-docker pre-commit install-dev tag-version generate-python-client build-docker build-test-cassandra test-reset-cassandra-image test-migration setup-migration-worktree clean-migration-worktree serve-old serve-new test-regression
