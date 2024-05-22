all: format lint

test:
	tox -e py39 -- graphsense

test-all-env:
	tox -- graphsense

lint:
	flake8 ./gsrest --count --max-line-length=80 --statistics --exclude plugins

format:
	autopep8 --in-place --recursive gsrest
	yapf --in-place --recursive gsrest

serve:
	python -m aiohttp.web -H localhost -P 9000 openapi_server:main

dev:
	adev runserver -p 9000 --root . --app-factory main openapi_server/__init__.py

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


# get-openapi-spec-from-upstream:
# 	wget -O openapi_server/openapi/openapi.yaml https://raw.githubusercontent.com/graphsense/graphsense-openapi/master/graphsense.yaml

run-designer:
	docker run -d -p 8080:8080 swaggerapi/swagger-editor
	echo 'Designer UI is running on port 8080'


.PHONY: format lint test test-all-env serve drop-integration-db generate-openapi-server get-openapi-spec-from-upstream serve-docker
