[![Test REST Interface](https://github.com/graphsense/graphsense-REST/actions/workflows/test.yml/badge.svg)](https://github.com/graphsense/graphsense-REST/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/graphsense/graphsense-REST/badge.svg?branch=develop)](https://coveralls.io/github/graphsense/graphsense-REST?branch=develop)

# GraphSense REST Interface

The GraphSense REST Interface provides access to denormalized views computed
by the [graphsense-transformation][graphsense-transformation] pipeline.
It is used by the [graphsense-dashboard][graphsense-dashboard] component.

It is based on a server stub generated by the [OpenAPI Generator][openapi-generator] project against the [graphsense-openapi][graphsense-openapi] specification version 1.7.0.
It uses the [Connexion][connexion] library on top of [aiohttp][aiohttp].

*Note:* This `README.md` is also generated. Changes must be made in
`templates/README.mustache`.

## Setup

Copy the configuration file template `instance/config.yaml.template`

    cp instance/config.yaml.template instance/config.yaml

Open `instance/config.yaml` and configure the database connection.

## Requirements

Make sure you are running Python 3.9 or Python 3.10. 

    python3 --version

Create a Python environment for required dependencies

    python3 -m venv venv

Activate the environment

    . venv/bin/activate

Install the requirements

    pip install -r requirements.txt

You need access to GraphSense raw and transformed keyspaces.
See [Graphsense Transformation Pipeline][graphsense-transformation]
for further details.

Run the REST interface

    python -m aiohttp.web -H localhost -P 5000 openapi_server:main

Test the service in your browser:

    http://localhost:5000

## Deployment

In order to utilize multiple cores, you may run the REST interface through [Gunicorn][gunicorn].

Install gunicorn:

    pip install gunicorn

If unspecified gunicorn is run with a number of workers and threads both equal to the number of CPUs x 2. 

Run production server, overriding number of workers and threads through command line options (4 workers, 4 threads). Specify the aiohttp specific WebWorker class to leverage the full power of lightweight threads:

    gunicorn -w 4 --threads 4 "openapi_server:main()" --worker-class aiohttp.GunicornWebWorker

### Deployment with docker

To run the server on a [Docker][docker] container, please execute the following
from the root directory:

Build the image

    docker build -t openapi_server .

You may specifiy the number of workers and threads through the environments variables `NUM_WORKERS` and `NUM_THREADS` respectively.

Start up a container with 4 workers and 4 threads:

    docker run -e NUM_WORKERS=4 -e NUM_THREADS=4 -p 9000:9000 openapi_server

## Customize REST interface configuration

Flask configuration parameters can be added at the top level of
`instance/config.yaml`. A configuration template file is provided in
`conf/config.yaml.template`.

You may define `ALLOWED_ORIGINS` in `instance/config.yaml` if the REST
interface is to be consumed by a Web browser, e.g.
by [graphsense-dashboard][graphsense-dashboard].


### Logging

REST log messages can be delivered via mail. See `instance/config.yaml.template` for an example.

## Development

### Generate server stub

```sh
BRANCH=master
docker run --rm \
  -v "${PWD}:/build" \
  -v "${PWD}/templates:/templates" \
  openapitools/openapi-generator-cli \
  generate -i "https://raw.githubusercontent.com/graphsense/graphsense-openapi/${BRANCH}/graphsense.yaml" \
  -g python-aiohttp -o /build -t /templates
```

The service implementation (`gsrest/service`) should use the generated models
located in `openapi_server/models`.

Source code generation is based on templates. See the `templates` directory for
currently used templates. If you need more templates, retrieve them from the
generator like so:

    docker run --rm -v "/tmp/templates:/templates" openapitools/openapi-generator-cli author template -g python-aiohttp -o /templates

Templates are written to `/tmp/templates`. Copy the needed ones to this
project's `templates` directory.

### Testing

Service tests are located in `gsrest/test`. These are called from generated
controller tests located in `openapi_server/test/`.

To launch the integration tests, use `tox`:

```
pip install tox
tox
```

This launches a mockup Cassandra database instance and ingests test data from
`tests/data`. See `tox.ini` (`templates/tox.mustache` respectively) and
`tests/Makefile` for further details on test configuration and setup.

Test instance configuration template can be found in `tests/config.yaml.template`.
The test instance configuration is generated automatically from the template.
You may only need to edit the template if you add more test keyspaces.

You may use `tests/fetch_data.sh` to fetch live data and customize for testing.

### Testing in Docker

In order to have a reproducible test environment, tests can also be run via docker. 

```
export UID  # in order to inject user id into the docker container and avoid permission issues
cd tests
make test
```

On OS X you need to install GNU sed and link it on your system as `sed`. 

[graphsense-blocksci]: https://github.com/graphsense/graphsense-blocksci
[graphsense-transformation]: https://github.com/graphsense/graphsense-transformation
[graphsense-dashboard]: https://github.com/graphsense/graphsense-dashboard
[graphsense-openapi]: https://github.com/graphsense/graphsense-openapi
[openapi-generator]: https://openapi-generator.tech
[connexion]: https://github.com/zalando/connexion
[aiohttp]: https://docs.aiohttp.org/en/stable/
[docker]: https://docs.docker.com/install
[gunicorn]: https://gunicorn.org/#docs
[docker]: https://www.docker.com
