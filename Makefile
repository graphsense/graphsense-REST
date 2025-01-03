all: format lint

-include .env

GS_REST_SERVICE_VERSIONM ?= "25.01.0a6"
GS_REST_SERVICE_VERSION ?= "2.0.0a6"
GS_REST_DEV_PORT ?= 9000
NUM_WORKERS ?= 1
NUM_THREADS ?= 1

test:
	uv run pytest -x -rx -vv

test-all-env:
	uv run tox

lint:
	uv run ruff check .

format:
	uv run ruff check --select I --fix
	uv run ruff format

install-dev:
	uv sync --all-extras --dev

pre-commit:
	uv run pre-commit run --all-files

serve-old:
	uv run python -m aiohttp.web -H localhost -P ${GS_REST_DEV_PORT} gsrest:main

serve:
	uv run adev runserver -p ${GS_REST_DEV_PORT} --root . --app-factory main gsrest/__init__.py

build-docker:
	docker build -t graphsense-rest .

serve-docker:
	docker run -rm -it --network='host' -e NUM_THREADS=1 -e NUM_WORKERS=1 -v "${PWD}/instance/config.yaml:/config.yaml:Z" -e CONFIG_FILE=/config.yaml localhost/graphsense-rest:latest

generate-openapi-server: update-package-version
	docker run --rm   \
		-v "${PWD}:/build:Z" \
		-v "${PWD}/openapi_spec/templates:/templates" \
		-v "${PWD}/openapi_spec/:/graphsense:Z" \
		openapitools/openapi-generator-cli:v5.2.1 \
		generate -i "/graphsense/graphsense.yaml" \
		-g python-aiohttp \
		-o /build \
		-t /templates \
		--additional-properties=packageVersion=$(GS_REST_SERVICE_VERSION)
	yq -i 'del(.components.schemas.search_result_level1.example,.components.schemas.search_result_level2.example,.components.schemas.search_result_level3.example,.components.schemas.search_result_level4.example,.components.schemas.search_result_level5.example,.components.schemas.search_result_level6.example,.components.schemas.search_result_leaf.example)' openapi_server/openapi/openapi.yaml

run-designer:
	docker run --rm -d -p 8080:8080 swaggerapi/swagger-editor
	echo 'Designer UI is running on port 8080'

update-package-version: update-openapi-version
	sed -i -r 's/(version = ).*/\1$(GS_REST_SERVICE_VERSION)/' pyproject.toml

update-openapi-version:
	sed -i '/^info:/,/^  version:/s/^\(\s*version:\s*\).*/\1$(GS_REST_SERVICE_VERSION)/' openapi_spec/graphsense.yaml

tag-version:
	-git diff --exit-code && git diff --staged --exit-code && git tag -a v$(GS_REST_SERVICE_VERSIONM) -m 'Release v$(GS_REST_SERVICE_VERSION)' || (echo "Repo is dirty please commit first" && exit 1)
	git diff --exit-code && git diff --staged --exit-code && git tag -a v$(GS_REST_SERVICE_VERSION) -m 'Release v$(GS_REST_SERVICE_VERSION)' || (echo "Repo is dirty please commit first" && exit 1)



.PHONY: format lint test test-all-env serve generate-openapi-server get-openapi-spec-from-upstream serve-docker pre-commit install-dev update-openapi-version tag-version
