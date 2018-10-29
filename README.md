# GraphSense REST Interface

The GraphSense REST Interface provides access to denormalized views computed by the [Graphsense
Transformation Pipeline][graphsense-transformation]. It is used by the
[graphsense-dashboard][graphsense-dashboard] component.

Python3 is recommended.

## Run REST interface locally

You can run the API either using `pip` or `docker`
##### Using `pip`
Run 

    pip install -r requirements.txt

and then

    python graphsenserest.py

##### Using `docker`

After installing [docker](https://docs.docker.com/install/), run:

    docker/build.sh
    docker/start.sh

Test the service in your browser:

    http://localhost:9000/btc/block/10000


[graphsense-transformation]: https://github.com/graphsense/graphsense-transformation
[graphsense-dashboard]: https://github.com/graphsense/graphsense-dashboard

