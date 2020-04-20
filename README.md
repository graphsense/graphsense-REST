[![Build Status](https://travis-ci.org/graphsense/graphsense-REST.svg?branch=master)](https://travis-ci.org/graphsense/graphsense-REST)
[![Coverage Status](https://coveralls.io/repos/github/graphsense/graphsense-REST/badge.svg?branch=master)](https://coveralls.io/github/graphsense/graphsense-REST?branch=master)

# GraphSense REST Interface

The GraphSense REST Interface provides access to denormalized views computed
by the [graphsense-transformation][graphsense-transformation] pipeline.
It is used by the [graphsense-dashboard][graphsense-dashboard] component.

## Prerequisites

Make sure you are running Python version >= 3.7

    python3 --version

Create a python environment for required dependencies

    python3 -m venv venv

Activate the environment

    . venv/bin/activate

Install the requirements

    pip3 install -r requirements.txt

Export REST interface environment variables

    export FLASK_APP=gsrest
    export FLASK_ENV=development

You need access to GraphSense raw and transformed keyspaces.
See [Graphsense Transformation Pipeline][graphsense-transformation]
for further details.

## Development (without Docker)

Create an instance folder and copy the configuration file template

    mkdir -p instance
    cp conf/config.py.tmp instance/config.py

Open `instance/config.py` and enter Cassandra connection configuration

Init the user database

    flask init-db

Create a username and password

    flask create-user john doe

Run the REST interface

    flask run

Test the service in your browser:

    http://localhost:5000

## Testing

Install project in local environment

    pip install -e .

Run tests

    pytest

Check test coverage

    coverage run -m pytest
    coverage report


## Deployment

When used in production, GraphSense-REST must be deployed to a WSGI server
because Flask's built-in server is not suitable for production -
it doesn't scale. From several [deployment options][flask-deployment],
we have chosen [Gunicorn][gunicorn].

Install gunicorn

    pip install gunicorn

Run production server

    gunicorn "gsrest:create_app()"

### Deployment with docker

#### Prerequisites

- [Docker][docker], see e.g. https://docs.docker.com/engine/install/
- Docker Compose: https://docs.docker.com/compose/install/

#### Configuration

Copy `docker/.env.template` to `.env`. Adjust the number of `gunicorn`
worker processes (variable `NUM_WORKER`, default three processes) and
set the Flask secret key (variable `SECRET_KEY`), e.g., to to a random
string using the provided script:

    docker/gen_secret_key.sh

Create an instance folder and copy the configuration file template

    mkdir -p instance
    cp conf/config.py.tmp instance/config.py

Open `instance/config.py` and enter Cassandra connection configuration.

#### Docker deployment

Build the image

    docker-compose build

and start a container (in detached mode):

    docker-compose up -d

Afterwards add users to the running container instance using

    docker/add_user.sh USERNAME PASSWORD

Finally, test the service in a web browser:

    http://localhost:9000

## Usage

### Authenticate your client app

All REST interface methods require authentication via [JSON Web Tokens (JWT][https://jwt.io/].

Request a JWT by calling the login interface using a given username/password combination:

    curl -X POST "http://localhost:5000/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"john\", \"password\": \"doe\"}"

This will return a JWT, which you must use in subsequent requests.
This is an example response:

    {
        "status": "success",
        "message": "Successfully logged in.",
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzE4MzQxNTMsImlhdCI6MTU3MTc0Nzc0OCwic3ViIjoiam9obiJ9.TxYnzE09A0BYfowvK4K5Zds6uyDJ_UrXkwF3NKqqvvA"
    }

Now use the JWT as part of the `Authorization` header field in subsequent requests:

    curl -X GET "http://localhost:5000/100/blocks/" -H "accept: application/json" -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzE4MzQxNTMsImlhdCI6MTU3MTc0Nzc0OCwic3ViIjoiam9obiJ9.TxYnzE09A0BYfowvK4K5Zds6uyDJ_UrXkwF3NKqqvvA"

Logging out will blacklist the JWT

    curl -X POST "http://localhost:5000/logout" -H "accept: application/json" -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzE3NzcyNTIsImlhdCI6MTU3MTY5MDg0Nywic3ViIjoic3RyaW5nIn0.muFr5f6vJEjh9NGwkXyxWgH3B0GuVkzxcu8fBgsKwdM"

## Customize REST interface configuration

Default configuration parameters are read from `app/config.py` during startup.

Parameters can be customized by placing a custom configuration file into the
Flask app instance folder, e.g., `instance/config.py`.
A configuration template file is provided in `conf/config.py.tmp`.

If you deploy the API behind a proxy, you can set `USE_PROXY = True`.

The secret key that will be used for signing authentication tokens is read
from the environment and should be set before starting the app

    export SECRET_KEY=$(python -c 'import os; print(os.urandom(16))')


[graphsense-blocksci]: https://github.com/graphsense/graphsense-blocksci
[graphsense-transformation]: https://github.com/graphsense/graphsense-transformation
[graphsense-dashboard]: https://github.com/graphsense/graphsense-dashboard
[docker]: https://docs.docker.com/install
[flask-deployment]: https://flask.palletsprojects.com/en/1.1.x/deploying/#self-hosted-options
[gunicorn]: https://gunicorn.org/#docs
[docker]: https://www.docker.com
