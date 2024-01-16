all: format lint

test:
	tox -e py39 -- graphsense

test-all-env:
	tox -- graphsense

lint:
	flake8 gsrest

format:
	autopep8 --in-place --recursive gsrest
	yapf --in-place --recursive gsrest

serve:
	python -m aiohttp.web -H localhost -P 9000 openapi_server:main

build-docker:
	docker build -t graphsense-rest .

serve-docker: build-docker
	docker run -it --network='host' -v "${PWD}/instance/config.yaml:/config.yaml:Z" -e CONFIG_FILE=/config.yaml localhost/graphsense-rest:latest

drop-integration-db:
	docker stop cassandra_mock; docker stop tagstore_mock; rm ./tests/.runcass ./tests/.runts

generate-openapi-server:
	docker run --rm   \
		-v "${PWD}:/build:Z" \
		-v "${PWD}/openapi_server/openapi/openapi.yaml:/spec.yaml" \
		-v "${PWD}/templates:/templates" \
		openapitools/openapi-generator-cli:v5.2.1 \
		generate -i /spec.yaml \
		-g python-aiohttp \
		-o /build \
		-t /templates \
		--additional-properties=packageVersion=$(RELEASE)


get-openapi-spec-from-upstream:
	wget -O openapi_server/openapi/openapi.yaml https://raw.githubusercontent.com/graphsense/graphsense-openapi/master/graphsense.yaml


.PHONY: format lint test test-all-env serve drop-integration-db generate-openapi-server get-openapi-spec-from-upstream serve-docker
