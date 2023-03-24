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

drop-integration-db:
	docker stop cassandra_mock; docker stop tagstore_mock; rm ./tests/.runcass ./tests/.runts

.PHONY: format lint test test-all-env serve drop-integration-db
