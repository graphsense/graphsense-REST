all: format lint

GS_REST_SERVICE_VERSION ?= "24.11.0"
GS_REST_DEV_PORT ?= 9000

test:
	tox -e py39 -- graphsense

test-all-env:
	tox -- graphsense

lint:
	ruff check gsrest

format:
	ruff check --select I --fix gsrest
	ruff format gsrest

install-dev:
	 pip install -r requirements.txt
	 pip install -r test-requirements.txt
	 pip install -r dev-requirements.txt
	 pre-commit install

pre-commit:
	pre-commit run --all-files

serve-old:
	python -m aiohttp.web -H localhost -P ${GS_REST_DEV_PORT} openapi_server:main

serve:
	adev runserver -p ${GS_REST_DEV_PORT} --root . --app-factory main openapi_server/__init__.py

build-docker:
	docker build -t graphsense-rest .

serve-docker: build-docker
	docker run -it --network='host' -v "${PWD}/instance/config.yaml:/config.yaml:Z" -e CONFIG_FILE=/config.yaml localhost/graphsense-rest:latest

drop-integration-db:
	docker stop cassandra_mock; docker stop tagstore_mock; rm ./tests/.runcass ./tests/.runts

generate-openapi-server:
	docker run --rm   \
		-v "${PWD}:/build:Z" \
		-v "${PWD}/templates:/templates" \
		-v "${PWD}/openapi_spec/:/graphsense:Z" \
		openapitools/openapi-generator-cli:v5.2.1 \
		generate -i "/graphsense/graphsense.yaml" \
		-g python-aiohttp \
		-o /build \
		-t /templates \
		--additional-properties=packageVersion=$(GS_REST_SERVICE_VERSION)
	yq -i 'del(.components.schemas.search_result_level1.example,.components.schemas.search_result_level2.example,.components.schemas.search_result_level3.example,.components.schemas.search_result_level4.example,.components.schemas.search_result_level5.example,.components.schemas.search_result_level6.example,.components.schemas.search_result_leaf.example)' openapi_server/openapi/openapi.yaml

run-designer:
	docker run -d -p 8080:8080 swaggerapi/swagger-editor
	echo 'Designer UI is running on port 8080'


.PHONY: format lint test test-all-env serve drop-integration-db generate-openapi-server get-openapi-spec-from-upstream serve-docker pre-commit install-dev
