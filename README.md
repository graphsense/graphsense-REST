# GraphSense REST Interface

The GraphSense REST Interface provides access to denormalized views computed
by the [Graphsense Transformation Pipeline][graphsense-transformation].
It is used by the [graphsense-dashboard][graphsense-dashboard] component.

## Prerequisites

Make sure you are running Python version >= 3.7

    python3 --version

You need access to GraphSense raw and transformed keyspaces. See [Graphsense Transformation Pipeline][graphsense-transformation] for further details.

## Run REST interface locally without Docker

Create a python environment for required dependencies

    python3 -m venv venv

Activate the environment

    . venv/bin/activate

Install the requirements

    pip3 install -r requirements.txt

Init the user database

    flask init-db

Create a username and password

    flask create-user john johnspwd

Run the REST interface

    export FLASK_APP=app
    export FLASK_ENV=development

    flask run

Test the service in your browser:

    http://localhost:5000

## Authorize your client

All REST interface methods require authentication via [JSON Web Tokens (JWT][https://jwt.io/].

Request a JWT by calling the login interface using a given username / password commbination:

    curl -X POST "http://localhost:5000/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"john\", \"password\": \"johnspwd\"}"

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


[graphsense-blocksci]: https://github.com/graphsense/graphsense-blocksci
[graphsense-transformation]: https://github.com/graphsense/graphsense-transformation
[graphsense-dashboard]: https://github.com/graphsense/graphsense-dashboard
[docker]: https://docs.docker.com/install
