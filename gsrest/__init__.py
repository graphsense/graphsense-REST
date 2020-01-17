import os

from flask import Flask
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix

from gsrest.config import Config


def load_config_from_file(app):
    # load default config, when not testing
    config = Config(instance_path=app.instance_path)
    app.config.from_object(config)
    # override with instance config, if available
    app.config.from_pyfile('config.py', silent=False)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    # read the configuration
    if test_config is None:
        # load default config from file
        load_config_from_file(app)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register user database
    from gsrest.db import user_db
    user_db.init_app(app)

    # register user service
    from gsrest.service import user_service
    user_service.init_app(app)

    # register cassandra database
    from gsrest.db import cassandra
    cassandra.init_app(app)

    # register exchange rates service
    from gsrest.service import rates_service
    rates_service.init_app(app)

    # register api namespaces
    from gsrest.apis import api
    api.init_app(app)

    return app
