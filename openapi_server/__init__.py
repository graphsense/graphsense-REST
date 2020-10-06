#!/usr/bin/env python3

import connexion
import os

from openapi_server import encoder

CONFIG_FILE = "config.py"


def load_config(app, instance_path):
    print("instance_path {} {}".format(instance_path, app.instance_path), flush=True)
    instance_path = app.instance_path if not instance_path else instance_path
    # ensure that instance path and config file exists
    config_file_path = os.path.join(instance_path, CONFIG_FILE)
    if not os.path.exists(config_file_path):
        app.logger.error("Instance path with config.py file is missing.")
    # load default config, when not testing
    # override with instance config, if available
    app.config.from_pyfile(config_file_path, silent=False)


def init_services(app):
    # register cassandra database
    from gsrest.db import cassandra
    cassandra.init_app(app)

def main(instance_path = None):
    app = connexion.App(__name__, 
      specification_dir='./openapi/', 
      options={"swagger_ui": True, "serve_spec": True})

    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'GraphSense API'},
                pythonic_params=True)
    load_config(app.app, instance_path)
    init_services(app.app)
    return app


