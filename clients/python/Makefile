-include .env

OPENAPI_URL ?= http://localhost:9000/openapi.json
GENERATOR_VERSION ?= v7.19.0
TEMPLATES_DIR ?= ../python-templates

# Legacy v5.2.1 generator (for comparison/rollback)
generate-openapi-client-v5:
	@echo "Downloading openapi.json from $(OPENAPI_URL)..."
	curl -s $(OPENAPI_URL) > openapi.json.tmp
	@echo "Modifying server URL to production..."
	python scripts/openapi_spec_add_auth.py openapi.json.tmp https://api.ikna.io > openapi.json.modified
	@echo "Generating client with v5.2.1..."
	docker run --rm \
		--user $(shell id -u):$(shell id -g) \
		-v "${PWD}:/build:Z" \
		-v "${PWD}/$(TEMPLATES_DIR):/templates:Z" \
		openapitools/openapi-generator-cli:v5.2.1 \
		generate -i /build/openapi.json.modified \
		-g python \
		-t /templates \
		-o /build \
		--additional-properties=packageName=graphsense \
		--additional-properties=projectName=graphsense-python
	@echo "Cleaning up temporary files..."
	rm -f openapi.json.tmp openapi.json.modified

# v7 generator with backward compatibility patches
generate-openapi-client:
	@echo "Downloading openapi.json from $(OPENAPI_URL)..."
	curl -s $(OPENAPI_URL) > openapi.json.tmp
	@echo "Modifying server URL to production..."
	python scripts/openapi_spec_add_auth.py openapi.json.tmp https://api.ikna.io > openapi.json.modified
	@API_VERSION=$$(jq -r '.info.version' openapi.json.tmp) && \
	echo "Generating client with $(GENERATOR_VERSION) (API version: $$API_VERSION)..." && \
	docker run --rm \
		--user $(shell id -u):$(shell id -g) \
		-v "${PWD}:/build:Z" \
		-v "${PWD}/$(TEMPLATES_DIR):/templates:Z" \
		openapitools/openapi-generator-cli:$(GENERATOR_VERSION) \
		generate -i /build/openapi.json.modified \
		-g python \
		-t /templates \
		-o /build \
		--additional-properties=packageName=graphsense \
		--additional-properties=projectName=graphsense-python \
		--additional-properties=packageVersion=$$API_VERSION \
		--additional-properties=library=urllib3
	@echo "Applying backward compatibility patches..."
	python scripts/patch_compat.py .
	@echo "Verifying backward compatibility..."
	python scripts/test_compat.py
	@echo "Cleaning up temporary files..."
	rm -f openapi.json.tmp openapi.json.modified

# Just run the compatibility tests (useful during development)
test-compat:
	python scripts/test_compat.py

run-examples:
	API_KEY=$(API_KEY) python test_examples.py

.PHONY: generate-openapi-client generate-openapi-client-v5 test-compat run-examples
