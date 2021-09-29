[![Test REST Interface](https://github.com/graphsense/graphsense-REST/actions/workflows/test.yml/badge.svg)](https://github.com/graphsense/graphsense-REST/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/graphsense/graphsense-REST/badge.svg?branch=develop)](https://coveralls.io/github/graphsense/graphsense-REST?branch=develop)

# GraphSense REST Interface

The GraphSense REST Interface provides access to denormalized views computed
by the [graphsense-transformation][graphsense-transformation] pipeline.
It is used by the [graphsense-dashboard][graphsense-dashboard] component.

It is based on a server stub generated by the
[OpenAPI Generator][openapi-generator] project.
It uses the [Connexion][connexion] library on top of [Flask][flask].

*Note:* This `README.md` is also generated. Changes must be made in
`templates/README.mustache`.

## Setup

Copy the configuration file template `instance/config.yaml.template`

    cp instance/config.yaml.template instance/config.yaml

Open `instance/config.yaml` and configure the database connection.

## Requirements

Make sure you are running Python 3.6+

    python3 --version

Create a Python environment for required dependencies

    python3 -m venv venv

Activate the environment

    . venv/bin/activate

Install the requirements

    pip install -r requirements.txt

Export REST interface environment variables

    export FLASK_APP=openapi_server:flask
    export FLASK_ENV=development

You need access to GraphSense raw and transformed keyspaces.
See [Graphsense Transformation Pipeline][graphsense-transformation]
for further details.

Run the REST interface

    flask run

Test the service in your browser:

    http://localhost:5000

## Deployment

When used in production, GraphSense-REST must be deployed to a WSGI server
because Flask's built-in server is not suitable for production -
it doesn't scale. From several [deployment options][flask-deployment],
we have chosen [Gunicorn][gunicorn].

Install gunicorn

    pip install gunicorn

If unspecified gunicorn is run with a number of workers and threads both equal to the number of CPUs x 2. 

Run production server, overriding number of workers and threads through command line options (4 workers, 4 threads):

    gunicorn -w 4 --threads 4 "openapi_server:main()"

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

## Development

### Generate server stub

```sh
BRANCH=master
URL=https://github.com/graphsense/graphsense-openapi/blob/$BRANCH/graphsense.yaml
docker run --rm \
  -v "${PWD}:/build" \
  -v "${PWD}/templates:/templates" \
  openapitools/openapi-generator-cli \
  generate -i "$URL" -g python-flask -o /build -t /templates
```

The service implementation (`gsrest/service`) should use the generated models
located in `openapi_server/models`.

Source code generation is based on templates. See the `templates` directory for
currently used templates. If you need more templates, retrieve them from the
generator like so:

    docker run --rm -v "/tmp/templates:/templates" openapitools/openapi-generator-cli author template -g python-flask -o /templates

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

[graphsense-blocksci]: https://github.com/graphsense/graphsense-blocksci
[graphsense-transformation]: https://github.com/graphsense/graphsense-transformation
[graphsense-dashboard]: https://github.com/graphsense/graphsense-dashboard
[openapi-generator]: https://openapi-generator.tech
[connexion]: https://github.com/zalando/connexion
[flask]: https://flask.palletsprojects.com
[docker]: https://docs.docker.com/install
[flask-deployment]: https://flask.palletsprojects.com/en/1.1.x/deploying/#self-hosted-options
[gunicorn]: https://gunicorn.org/#docs
[docker]: https://www.docker.com
