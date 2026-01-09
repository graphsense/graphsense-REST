[![Test REST Interface](https://github.com/graphsense/graphsense-REST/actions/workflows/test.yml/badge.svg)](https://github.com/graphsense/graphsense-REST/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/graphsense/graphsense-REST/badge.svg?branch=develop)](https://coveralls.io/github/graphsense/graphsense-REST?branch=develop)

# GraphSense REST Interface

The GraphSense REST Interface provides access to denormalized views computed
by the [graphsense-transformation][graphsense-transformation] pipeline.
It is used by the [graphsense-dashboard][graphsense-dashboard] component.

It is built with [FastAPI][fastapi] and served via [Uvicorn][uvicorn].

## Python Client

For integrating the GraphSense API into your Python applications, we provide an official Python client library.

### Installation

Install the GraphSense Python client via pip:

```bash
pip install graphsense-python
```

### Usage

For detailed usage instructions and examples, see the [Python client documentation](./clients/python/README.md).

## REST Interface - Setup

Copy the configuration file template `instance/config.yaml.template`

    cp instance/config.yaml.template instance/config.yaml

Open `instance/config.yaml` and configure the database connection.

## Requirements

Make sure you are running Python > 3.10. We are using uv for packaging and dependency management. Please install [uv][uv].

Run

    make install-dev

to setup the project for development.

    uv sync --frozen

only installs the dependencies nessesary for running the project.

You need access to GraphSense raw and transformed keyspaces.
See [Graphsense Transformation Pipeline][graphsense-transformation]
for further details.

Run the REST interface

    make serve

Test the service in your browser:

    http://localhost:9000

On OS X you need to install GNU sed and link it on your system as `sed`.

## Deployment

For production deployment, run the REST interface through [Uvicorn][uvicorn] with multiple workers:

    uv run uvicorn gsrest.app:create_app --factory --host 0.0.0.0 --port 9000 --workers 4

Alternatively, use [Gunicorn][gunicorn] with Uvicorn workers for more control:

    uv run gunicorn gsrest.app:create_app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:9000

### Deployment with docker

To run the server on a [Docker][docker] container, please execute the following
from the root directory:

Build the image

    make build-docker

You may specifiy the number of workers and threads through the environments variables `NUM_WORKERS` and `NUM_THREADS` respectively.

Start up a container with 1 workers and 1 threads:

    make serve-docker

As an alternative you can use our prebuild docker images.

    docker run -e NUM_WORKERS=4 -e NUM_THREADS=4 -p 9000:9000 ghcr.io/graphsense/graphsense-rest:latest

## Customize REST interface configuration

Configuration parameters can be added at the top level of
`instance/config.yaml`. A configuration template file is provided in
`instance/config.yaml.template`.

You may define `ALLOWED_ORIGINS` in `instance/config.yaml` if the REST
interface is to be consumed by a Web browser, e.g.
by [graphsense-dashboard][graphsense-dashboard].


### Logging

REST log messages can be delivered via mail. See `instance/config.yaml.template` for an example.

## Development

### Setup Development Environment

We use pre-commit hooks to ensure code quality and consistency. After setting up the project, install the pre-commit hooks:

```bash
make install-dev
pre-commit install
```

This will automatically run code formatting, linting, and other checks before each commit. The hooks include:

- **Code formatting** with [ruff][ruff]
- **Linting** to catch potential issues
- **Import sorting** to maintain consistent import order
- **YAML/JSON validation** for configuration files
- **Code Generation** of the Python client

You can manually run all pre-commit hooks on all files:

```bash
pre-commit run --all-files
```

### Testing

Service tests are located in `gsrest/test`. These are called from the
controller tests located in `tests/test_*`.

To launch the integration tests run:

```
make test
```

This launches a mockup Cassandra database instance and ingests test data from
`tests/cassandra/data` and `tests/tagstore/data` via the corresponding `insert.py`
scripts in each folder.

Setup for the cassandra and postgres databases and the general configuration for
the rest interface for testing is defined in `conftest.py` as a pytest fixture.

[graphsense-transformation]: https://github.com/graphsense/graphsense-spark
[graphsense-dashboard]: https://github.com/graphsense/graphsense-dashboard
[fastapi]: https://fastapi.tiangolo.com
[uvicorn]: https://www.uvicorn.org
[docker]: https://www.docker.com
[gunicorn]: https://gunicorn.org/#docs
[uv]: https://docs.astral.sh/uv/getting-started/installation/
[ruff]: https://docs.astral.sh/ruff/
