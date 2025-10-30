import importlib
import logging
import logging.handlers
import os
from typing import Optional

import aiohttp_cors
import connexion
import yaml
from graphsenselib.config import AppConfig
from graphsenselib.utils.slack import SlackLogHandler

import gsrest.db
from gsrest.config import GSRestConfig, LoggingConfig
from gsrest.dependencies import ConceptsCacheService, ServiceContainer
from gsrest.plugins import get_subclass
from gsrest.builtin.plugins.obfuscate_tags.obfuscate_tags import ObfuscateTags

CONFIG_FILE = "./instance/config.yaml"


def load_config(config_file):
    if not os.path.exists(config_file):
        raise ValueError("Config file {} not found.".format(config_file))

    with open(config_file, "r") as input_file:
        config = yaml.safe_load(input_file)
    return config


def setup_logging(
    logger,
    slack_exception_hook,
    default_environment: Optional[str],
    logging_config: LoggingConfig,
):
    level = logging_config.level.upper()
    level = getattr(logging, level)
    FORMAT = "%(asctime)s %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(level)

    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("connexion").setLevel(logging.WARNING)
    logging.getLogger("cassandra").setLevel(logging.INFO)

    for handler in logging.root.handlers:
        handler.setFormatter(
            logging.Formatter(
                "%(levelname)-8s %(asctime)s "
                "%(name)s:%(filename)s:%(lineno)d %(message)s"
            )
        )

    if slack_exception_hook is not None:
        for h in slack_exception_hook.hooks:
            slack_handler = SlackLogHandler(h, environment=default_environment)
            slack_handler.setLevel("ERROR")
            logger.addHandler(slack_handler)

    smtp = logging_config.smtp
    if not smtp:
        return

    credentials = None
    secure = None
    if smtp.username is not None:
        credentials = (smtp.username, smtp.password)
        if smtp.secure is True:
            secure = ()

    handler = logging.handlers.SMTPHandler(
        mailhost=(smtp.host, smtp.port),
        fromaddr=smtp.from_addr,
        toaddrs=smtp.to,
        subject=smtp.subject,
        credentials=credentials,
        secure=secure,
        timeout=smtp.timeout,
    )

    handler.setLevel(getattr(logging, smtp.level))
    logger.addHandler(handler)


def factory(config_file=None, validate_responses=False):
    if not config_file:
        config_file = CONFIG_FILE
    raw_config = load_config(config_file)
    config = GSRestConfig.from_dict(raw_config)

    gslibConfig = AppConfig()
    gslibConfig.load()
    # app.app.logger.info(f'reading config from {config_file}')
    return factory_internal(config, gslibConfig, validate_responses=validate_responses)


def factory_internal(
    config: GSRestConfig, gslibConfig: Optional[AppConfig], validate_responses=False
):
    options = {"swagger_ui": True, "serve_spec": True}

    specification_dir = os.path.join(
        os.path.dirname(__file__), "../openapi_server/openapi"
    )
    app = connexion.AioHttpApp(
        __name__,
        specification_dir=specification_dir,
        only_one_api=True,
        options=options,
    )

    openapi_yaml = "openapi.yaml"
    app.add_api(
        openapi_yaml,
        arguments={"title": "GraphSense API"},
        pythonic_params=True,
        validate_responses=validate_responses,
        pass_context_arg_name="request",
    )

    # set config
    if gslibConfig is not None:
        slack_exception_hook = gslibConfig.get_slack_hooks_by_topic("exceptions")
        slack_info_hook = gslibConfig.get_slack_hooks_by_topic("info")
        default_environment = config.environment or gslibConfig.default_environment
    else:
        slack_exception_hook = None
        slack_info_hook = None
        default_environment = config.environment

    config.slack_info_hook = slack_info_hook

    app.app["config"] = config
    setup_logging(
        app.app.logger,
        slack_exception_hook,
        default_environment,
        config.logging,
    )
    with open(os.path.join(specification_dir, openapi_yaml)) as yaml_file:
        app.app["openapi"] = yaml.safe_load(yaml_file)

    app.app.cleanup_ctx.append(gsrest.db.get_connection)

    # Initialize service container after db connection is established
    async def setup_services(app):
        app["services"] = ServiceContainer(
            config=app["config"],
            db=app["db"],
            tagstore_engine=app["gs-tagstore"],
            concepts_cache_service=ConceptsCacheService(app, app.logger),
            logger=app.logger,
        )
        yield

    app.app.cleanup_ctx.append(setup_services)

    origins = config.ALLOWED_ORIGINS if hasattr(config, "ALLOWED_ORIGINS") else "*"

    options = aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )

    defaults = {}

    for origin in origins:
        defaults[origin] = options

    app.app.logger.info("ALLOWED_ORIGINS: {}".format(origins))
    # Enable CORS for all origins.
    cors = aiohttp_cors.setup(app.app, defaults=defaults)

    # Register all routers for CORS.
    for route in list(app.app.router.routes()):
        cors.add(route)

    # Store the config object directly - no need to set individual values
    app.app["config"] = config

    app.app["plugins"] = []
    app.app["plugin_contexts"] = {}
    app.app["request_config"] = {}

    obfuscate_private_tags = any(
        1 for name in config.plugins if name.endswith("obfuscate_tags")
    )

    if obfuscate_private_tags:
        app.app.logger.warning(
            "Tag obfuscation plugin enabled, using built-in version. Skipping load of external plugin."
        )
        builtinPlugin = ObfuscateTags
        name = f"{builtinPlugin.__module__}"
        app.app["plugins"].append(builtinPlugin)
        app.app["plugin_contexts"][name] = {}
        if hasattr(builtinPlugin, "setup"):
            app.app.cleanup_ctx.append(plugin_setup(builtinPlugin, name))

    for name in config.plugins:
        if name.endswith("obfuscate_tags"):
            # already loaded builtin plugin
            continue

        subcl = get_subclass(importlib.import_module(name))
        app.app["plugins"].append(subcl)
        app.app["plugin_contexts"][name] = {}
        if hasattr(subcl, "setup"):
            app.app.cleanup_ctx.append(plugin_setup(subcl, name))

    return app


def plugin_setup(plugin, name):
    def setup(app):
        # Get plugin-specific config using the new method
        plugin_config = app["config"].get_plugin_config(name)
        a = {
            "config": plugin_config,
            "context": app["plugin_contexts"][name],
        }
        return plugin.setup(a)

    return setup


def main(args=None):
    return factory(args).app


def run(args=None):
    factory().run(port=8080)
