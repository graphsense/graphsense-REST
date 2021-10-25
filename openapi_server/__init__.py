import os
import connexion
import aiohttp_cors
import gsrest.db
import yaml
import logging

CONFIG_FILE = "config.yaml"


def load_config(instance_path):
    # ensure that instance path and config file exists
    config_file_path = os.path.join(instance_path, CONFIG_FILE)
    if not os.path.exists(config_file_path):
        raise ValueError("Instance path with {} file is missing."
                         .format(CONFIG_FILE))

    with open(config_file_path, 'r') as input_file:
        config = yaml.safe_load(input_file)
    return config


def factory(args=None):
    options = {
        "swagger_ui": True,
        "serve_spec": True
        }
    specification_dir = os.path.join(os.path.dirname(__file__), 'openapi')
    app = connexion.AioHttpApp(__name__,
                               specification_dir=specification_dir,
                               only_one_api=True,
                               options=options)
    logging.basicConfig(level=logging.DEBUG)
    app.add_api('openapi.yaml',
                arguments={'title': 'GraphSense API'},
                pythonic_params=True,
                pass_context_arg_name='request')
    instance_path = './instance'
    app.app['config'] = load_config(instance_path)

    app.app.cleanup_ctx.append(gsrest.db.get_connection)

    origins = app.app['config']['ALLOWED_ORIGINS'] \
        if 'ALLOWED_ORIGINS' in app.app['config'] else '*'

    app.app.logger.info('ALLOWED_ORIGINS: {}'.format(origins))
    # Enable CORS for all origins.
    cors = aiohttp_cors.setup(app.app, defaults={
        origins: aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # Register all routers for CORS.
    for route in list(app.app.router.routes()):
        cors.add(route)

    return app


def main(args=None):
    return factory(args).app


def run(args=None):
    factory().run(port=8080)
