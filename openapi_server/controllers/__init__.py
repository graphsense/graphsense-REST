#!/usr/bin/env python3

import connexion
import os
import yaml
import gsrest.db
from flask_cors import CORS

from openapi_server import encoder

CONFIG_FILE = "config.yaml"


def load_config(app, instance_path):
    instance_path = app.instance_path if not instance_path else instance_path
    # ensure that instance path and config file exists
    config_file_path = os.path.join(instance_path, CONFIG_FILE)
    if not os.path.exists(config_file_path):
        raise ValueError("Instance path with {} file is missing."
                         .format(CONFIG_FILE))

    with open(config_file_path, 'r') as input_file:
        config = yaml.safe_load(input_file)
        app.config.from_object(config)
        for k, v in config.items():
            app.config[k] = v


def main(instance_path=None):
    app = connexion.App(
        __name__,
        specification_dir='./openapi/',
        options={"swagger_ui": True, "serve_spec": True})

    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'GraphSense API'},
                pythonic_params=True)
    load_config(app.app, instance_path)
    with app.app.app_context():
        gsrest.db.get_connection()
    origins = app.app.config['ALLOWED_ORIGINS'] \
        if 'ALLOWED_ORIGINS' in app.app.config else '*'
    app.app.logger.info('ALLOWED_ORIGINS: {}'.format(origins))
    CORS(app.app, supports_credentials=True, origins=origins)
    return app


def flask():
    return main().app
