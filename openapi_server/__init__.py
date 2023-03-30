import os
import logging
import connexion
import aiohttp_cors
import gsrest.db
import yaml
import importlib
from gsrest.plugins import get_subclass

CONFIG_FILE = "./instance/config.yaml"


def load_config(config_file):
    if not os.path.exists(config_file):
        raise ValueError("Config file {} not found.".format(config_file))

    with open(config_file, 'r') as input_file:
        config = yaml.safe_load(input_file)
    return config


def setup_logging(logger, config):
    level = config.get('level', 'INFO').upper()
    level = getattr(logging, level)
    logger.setLevel(level)
    logger.info('info')
    logger.debug('test')
    smtp = config.get('smtp', None)
    if not smtp:
        return
    credentials = None
    secure = None
    if smtp.get('username', None) is not None:
        credentials = (smtp.get('username'), smtp.get('password'))
        if smtp.get('secure', None) is True:
            secure = ()
    handler = logging.handlers.SMTPHandler(mailhost=(smtp.get('host'),
                                                     smtp.get('port', None)),
                                           fromaddr=smtp.get('from'),
                                           toaddrs=smtp.get('to'),
                                           subject=smtp.get('subject'),
                                           credentials=credentials,
                                           secure=secure,
                                           timeout=smtp.get('timeout', None))

    handler.setLevel(getattr(logging, smtp.get('level', 'CRITICAL')))
    logger.addHandler(handler)


def factory(config_file=None, validate_responses=False):
    if not config_file:
        config_file = CONFIG_FILE
    options = {"swagger_ui": True, "serve_spec": True}
    specification_dir = os.path.join(os.path.dirname(__file__), 'openapi')
    app = connexion.AioHttpApp(__name__,
                               specification_dir=specification_dir,
                               only_one_api=True,
                               options=options)
    openapi_yaml = 'openapi.yaml'
    app.add_api(openapi_yaml,
                arguments={'title': 'GraphSense API'},
                pythonic_params=True,
                validate_responses=validate_responses,
                pass_context_arg_name='request')
    app.app.logger.info(f'reading config from {config_file}')
    app.app['config'] = load_config(config_file)
    setup_logging(app.app.logger, app.app['config'].get('logging', {}))
    with open(os.path.join(specification_dir, openapi_yaml)) as yaml_file:
        app.app['openapi'] = yaml.safe_load(yaml_file)

    app.app.cleanup_ctx.append(gsrest.db.get_connection)

    origins = app.app['config']['ALLOWED_ORIGINS'] \
        if 'ALLOWED_ORIGINS' in app.app['config'] else '*'

    options = aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )

    defaults = {}

    for origin in origins:
        defaults[origin] = options

    app.app.logger.info('ALLOWED_ORIGINS: {}'.format(origins))
    # Enable CORS for all origins.
    cors = aiohttp_cors.setup(app.app, defaults=defaults)

    # Register all routers for CORS.
    for route in list(app.app.router.routes()):
        cors.add(route)

    app.app['config']['hide_private_tags'] = \
        app.app['config'].get('hide_private_tags', False)

    app.app['plugins'] = []
    app.app['plugin_contexts'] = {}
    for name in app.app['config'].get('plugins', []):
        subcl = get_subclass(importlib.import_module(name))
        app.app['plugins'].append(subcl)
        app.app['plugin_contexts'][name] = {}
        if hasattr(subcl, 'setup'):
            app.app.cleanup_ctx.append(plugin_setup(subcl, name))

    return app


def plugin_setup(plugin, name):
    def setup(app):
        a = {
            'config': app['config'].get(name, None),
            'context': app['plugin_contexts'][name]
        }
        return plugin.setup(a)

    return setup


def main(args=None):
    return factory(args).app


def run(args=None):
    factory().run(port=8080)
