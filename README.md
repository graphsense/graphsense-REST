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

[graphsense-blocksci]: https://github.com/graphsense/graphsense-blocksci
[graphsense-transformation]: https://github.com/graphsense/graphsense-transformation
[graphsense-dashboard]: https://github.com/graphsense/graphsense-dashboard
[docker]: https://docs.docker.com/install
