# GraphSense REST Interface

The GraphSense REST Interface provides access to denormalized views computed
by the [Graphsense Transformation Pipeline][graphsense-transformation].
It is used by the [graphsense-dashboard][graphsense-dashboard] component.

## Configuration

Create a configuration file

    cp app/config.json.template app/config.json

and update the values for `SECRET_KEY`, `CASSANDRA_NODES` (default
`localhost`) and `MAPPING`. For each currency two keyspaces are needed, which
are created by the [GraphSense Blocksci][graphsense-blocksci] backend and the
[GraphSense transformation][graphsense-transformation] pipeline respectively.
The keyspaces are configured according to the following structure

    {<CURRENCY_1>: [<RAW_KEYSPACE_NAME_CURRENCY_1>, <TRANSFORMED_KEYSPACE_NAME_CURRENCY_1>],
     <CURRENCY_2>: [<RAW_KEYSPACE_NAME_CURRENCY_2>, <TRANSFORMED_KEYSPACE_NAME_CURRENCY_2>],
     ...
     "tagpacks": "tagpacks"
    }

## Run REST interface locally

The REST interface is implemented in Python, Python version 3 is recommended.

You can run the API either using `pip` or `docker`:

##### Using `pip`

Run 

    pip install -r requirements.txt

then create a new user and password of your choice and start the interface with

    cd app/
    sudo ./adduser_and_start_rest.sh <user> <password>

##### Using `docker`

After installing [docker][docker], set the REST password (and username)
in `docker/build.sh` and run:

    docker/build.sh
    docker/start.sh

Test the service in your browser:

    http://localhost:9000

[graphsense-blocksci]: https://github.com/graphsense/graphsense-blocksci
[graphsense-transformation]: https://github.com/graphsense/graphsense-transformation
[graphsense-dashboard]: https://github.com/graphsense/graphsense-dashboard
[docker]: https://docs.docker.com/install
