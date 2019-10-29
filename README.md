# GraphSense REST Interface

The GraphSense REST Interface provides access to denormalized views computed
by the [Graphsense Transformation Pipeline][graphsense-transformation].
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

Export REST interface env variables

    export FLASK_APP=gsrest
    export FLASK_ENV=development

You need access to GraphSense raw and transformed keyspaces. See [Graphsense Transformation Pipeline][graphsense-transformation] for further details.

## Development (without Docker)

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


## Authenticate your client app

All REST interface methods require authentication via [JSON Web Tokens (JWT][https://jwt.io/].

Request a JWT by calling the login interface using a given username / password commbination:

    curl -X POST "http://localhost:5000/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"john\", \"password\": \"doe\"}"

This will return a JWT, which you must use in subsequent requests. This is an example response:

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

Parameters can be customized by placing a custom configuration file into the Flask app instance folder, e.g., `instance/config.py`. Example

    MAPPING = {
    "tagpacks": "tagpacks",
    "btc": ["btc_raw", "btc_transformed_20190914"],
    "bch": ["bch_raw", "bch_transformed_20190930"],
    "ltc": ["ltc_raw", "ltc_transformed_20190930"],
    "zec": ["zec_raw", "zec_transformed_20190930"]
}

The secret key that will be used for signing authentication tokens is read from the environment and
should be set before starting the app

    export SECRET_KEY=$(python -c 'import os; print(os.urandom(16))')


[graphsense-blocksci]: https://github.com/graphsense/graphsense-blocksci
[graphsense-transformation]: https://github.com/graphsense/graphsense-transformation
[graphsense-dashboard]: https://github.com/graphsense/graphsense-dashboard
[docker]: https://docs.docker.com/install
