import os

from flask import Flask
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix

from gsrest.config import Config


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # read production config, when not testing
    if test_config is None:
        # ensure that instance path and config file exists
        config_file_path = os.path.join(app.instance_path, "config.py")
        if not os.path.exists(config_file_path):
            app.logger.error("Instance path with config.py file is missing.")
        # load default config, when not testing
        config = Config(instance_path=app.instance_path)
        app.config.from_object(config)
        # override with instance config, if available
        app.config.from_pyfile('config.py', silent=False)
        if 'USE_PROXY' in app.config and app.config['USE_PROXY']:
            app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    CORS(app, supports_credentials=True,
         origins=app.config['ALLOWED_ORIGINS'] if 'ALLOWED_ORIGINS'
                                                  in app.config else '*')

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
