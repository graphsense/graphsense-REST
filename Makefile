all: format lint

-include .env

GS_REST_SERVICE_VERSIONM ?= "25.12.0rc2"
GS_REST_SERVICE_VERSION ?= "1.16.0rc2"

GS_REST_DEV_PORT ?= 9000
NUM_WORKERS ?= 1
NUM_THREADS ?= 1

test: install-dev
	uv run pytest -x -rx -vv

test-regression:
	@export SKIP_REST_CONTAINER_SETUP=True && uv run pytest -m "regression" -s

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

.PHONY: format lint test ensure-versions-alignment run-codegen serve serve-docker pre-commit install-dev tag-version generate-python-client build-docker
