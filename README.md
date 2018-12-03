# GraphSense REST Interface

The GraphSense REST Interface provides access to denormalized views computed
by the [Graphsense Transformation Pipeline][graphsense-transformation].
It is used by the [graphsense-dashboard][graphsense-dashboard] component.

## Configuration

Update the application configuration file `config.json` by setting
appropriate values for `SECRET_KEY`, `CASSANDRA_NODES` (default `localhost`)
and `MAPPING`. For each currency two keyspaces are needed, which are
created by the [GraphSense Blocksci][graphsense-blocksci] backend and the
[GraphSense transformation][graphsense-transformation] pipeline respectively.
The keyspace names must follow this naming convention:

    {<CURRENCY>: <TRANSFORMED_KEYSPACE_NAME>,
     <CURRENCY>_raw: <RAW_KEYSPACE_NAME>,
     ...
    }

## Run REST interface locally

The REST interface is implemented in Python, Python version 3 is recommended.

You can run the API either using `pip` or `docker`:

##### Using `pip`

Run 

    pip install -r requirements.txt

and then

    python graphsenserest.py

##### Using `docker`

After installing [docker][docker], run:

    docker/build.sh
    docker/start.sh


Test the service in your browser:

    http://localhost:9000/btc/block/10000


[graphsense-blocksci]: https://github.com/graphsense/graphsense-blocksci
[graphsense-transformation]: https://github.com/graphsense/graphsense-transformation
[graphsense-dashboard]: https://github.com/graphsense/graphsense-dashboard
[docker]: https://docs.docker.com/install
