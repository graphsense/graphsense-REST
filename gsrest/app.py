import importlib
import logging
import logging.handlers
import os
from contextlib import asynccontextmanager
from typing import Optional

import yaml
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from graphsenselib.config import AppConfig
from graphsenselib.db.asynchronous.services.tags_service import ConceptProtocol
from graphsenselib.errors import (
    BadUserInputException,
    FeatureNotAvailableException,
    GsTimeoutException,
    NotFoundException,
)
from graphsenselib.tagstore.db import TagstoreDbAsync, Taxonomies
from graphsenselib.tagstore.db.database import get_db_engine_async
from graphsenselib.utils.slack import SlackLogHandler

from gsrest.builtin.plugins.obfuscate_tags.obfuscate_tags import ObfuscateTags
from gsrest.config import GSRestConfig, LoggingConfig
from gsrest.dependencies import ServiceContainer
from gsrest.middleware.empty_params import EmptyQueryParamsMiddleware
from gsrest.middleware.plugins import PluginMiddleware
from gsrest.plugins import get_subclass
from gsrest.routes import (
    addresses,
    blocks,
    bulk,
    entities,
    general,
    rates,
    tags,
    tokens,
    txs,
)

CONFIG_FILE = "./instance/config.yaml"
logger = logging.getLogger(__name__)


def load_config(config_file: str) -> dict:
    if not os.path.exists(config_file):
        raise ValueError(f"Config file {config_file} not found.")

    with open(config_file, "r") as input_file:
        config = yaml.safe_load(input_file)
    return config


def setup_logging(
    app_logger,
    slack_exception_hook,
    default_environment: Optional[str],
    logging_config: LoggingConfig,
):
    level = logging_config.level.upper()
    level = getattr(logging, level)
    FORMAT = "%(asctime)s %(message)s"
    logging.basicConfig(format=FORMAT)
    app_logger.setLevel(level)

    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
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
            app_logger.addHandler(slack_handler)

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
    app_logger.addHandler(handler)


async def setup_database(app: FastAPI):
    """Setup database connections (Cassandra + TagStore)"""
    config = app.state.config
    db_config = config.database
    driver = db_config.driver.lower()
    logger.info(f"Opening {driver} connection ...")

    mod = importlib.import_module("graphsenselib.db.asynchronous." + driver)
    cls = getattr(mod, driver.capitalize())
    app.state.db = cls(db_config, logger)

    ts_conf = config.tagstore
    max_conn = ts_conf.pool_size
    max_pool_time = ts_conf.pool_timeout
    mo = ts_conf.max_overflow
    recycle = ts_conf.pool_recycle
    enable_prepared_statements_cache = ts_conf.enable_prepared_statements_cache

    engine = get_db_engine_async(
        ts_conf.url
        + (
            "?prepared_statement_cache_size=0"
            if not enable_prepared_statements_cache
            else ""
        ),
        pool_size=int(max_conn),
        max_overflow=int(mo),
        pool_recycle=int(recycle),
        pool_timeout=int(max_pool_time),
        pool_pre_ping=True,
    )

    app.state.tagstore_engine = engine

    # Setup taxonomy cache
    await ConceptsCacheServiceFastAPI.setup_cache(engine, app)

    logger.info("Database setup done")


async def teardown_database(app: FastAPI):
    """Cleanup database connections"""
    logger.info("Begin app teardown")
    driver = app.state.config.database.driver.lower()
    app.state.db.close()
    logger.info(f"Closed {driver} connection.")
    logger.info(app.state.tagstore_engine.pool.status())
    await app.state.tagstore_engine.dispose()
    logger.info(app.state.tagstore_engine.pool.status())
    logger.info("Closed Tagstore connection.")


class ConceptsCacheServiceFastAPI(ConceptProtocol):
    """FastAPI-compatible concepts cache service"""

    def __init__(self, app: FastAPI):
        self.app = app

    def get_is_abuse(self, concept: str) -> bool:
        return concept in self.app.state.taxonomy_cache["abuse"]

    def get_taxonomy_concept_label(self, taxonomy, concept_id: str) -> str:
        return self.app.state.taxonomy_cache["labels"][taxonomy].get(concept_id, None)

    @classmethod
    async def setup_cache(cls, db_engine, app: FastAPI):
        tagstore_db = TagstoreDbAsync(db_engine)
        taxs = await tagstore_db.get_taxonomies(
            {Taxonomies.CONCEPT, Taxonomies.COUNTRY}
        )
        app.state.taxonomy_cache = {
            "labels": {
                Taxonomies.CONCEPT: {x.id: x.label for x in taxs.concept},
                Taxonomies.COUNTRY: {x.id: x.label for x in taxs.country},
            },
            "abuse": {x.id for x in taxs.concept if x.is_abuse},
        }


async def setup_services(app: FastAPI):
    """Setup service container"""
    config = app.state.config

    if config.tag_access_logger and config.tag_access_logger.enabled:
        logger.info("Tag access logging is enabled.")
        from redis import asyncio as aioredis

        redis_url = config.tag_access_logger.redis_url or "redis://localhost"
        logger.info(f"Connecting to Redis at {redis_url} for tag access logging.")
        redis_client = await aioredis.from_url(redis_url)
        log_tag_access_prefix = config.tag_access_logger.prefix
    else:
        redis_client = None
        log_tag_access_prefix = None

    app.state.services = ServiceContainer(
        config=config,
        db=app.state.db,
        tagstore_engine=app.state.tagstore_engine,
        concepts_cache_service=ConceptsCacheServiceFastAPI(app),
        logger=logger,
        redis_client=redis_client,
        log_tag_access_prefix=log_tag_access_prefix,
    )


async def setup_plugins(app: FastAPI):
    """Setup plugins"""
    config = app.state.config
    app.state.plugins = []
    app.state.plugin_contexts = {}

    obfuscate_private_tags = any(
        1 for name in config.plugins if name.endswith("obfuscate_tags")
    )

    if obfuscate_private_tags:
        logger.warning(
            "Tag obfuscation plugin enabled, using built-in version. "
            "Skipping load of external plugin."
        )
        builtin_plugin = ObfuscateTags
        name = f"{builtin_plugin.__module__}"
        app.state.plugins.append(builtin_plugin)
        app.state.plugin_contexts[name] = {"config": config.get_plugin_config(name)}
        if hasattr(builtin_plugin, "setup"):
            plugin_config = config.get_plugin_config(name)
            setup_args = {
                "config": plugin_config,
                "context": app.state.plugin_contexts[name],
            }
            setup_gen = builtin_plugin.setup(setup_args)
            # If setup is an async generator, iterate it for startup
            if hasattr(setup_gen, "__anext__"):
                await setup_gen.__anext__()
                app.state.plugin_cleanup_generators = [setup_gen]

    for name in config.plugins:
        if name.endswith("obfuscate_tags"):
            continue

        subcl = get_subclass(importlib.import_module(name))
        app.state.plugins.append(subcl)
        app.state.plugin_contexts[name] = {}
        if hasattr(subcl, "setup"):
            plugin_config = config.get_plugin_config(name)
            setup_args = {
                "config": plugin_config,
                "context": app.state.plugin_contexts[name],
            }
            setup_gen = subcl.setup(setup_args)
            if hasattr(setup_gen, "__anext__"):
                await setup_gen.__anext__()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await setup_database(app)
    await setup_services(app)
    await setup_plugins(app)

    yield

    # Shutdown
    await teardown_database(app)


def _register_exception_handlers(app: FastAPI):
    """Register common exception handlers on the app"""

    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=404,
            content={"detail": exc.get_user_msg()},
        )

    @app.exception_handler(BadUserInputException)
    async def bad_input_handler(request: Request, exc: BadUserInputException):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.get_user_msg()},
        )

    @app.exception_handler(FeatureNotAvailableException)
    async def feature_not_available_handler(
        request: Request, exc: FeatureNotAvailableException
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.get_user_msg()},
        )

    @app.exception_handler(GsTimeoutException)
    async def timeout_handler(request: Request, exc: GsTimeoutException):
        return JSONResponse(
            status_code=408,
            content={"detail": "Request timeout"},
        )


def _register_routers(app: FastAPI):
    """Register all API routers on the app"""
    app.include_router(general.router, tags=["general"])
    app.include_router(tags.router, tags=["tags"])
    app.include_router(addresses.router, prefix="/{currency}", tags=["addresses"])
    app.include_router(blocks.router, prefix="/{currency}", tags=["blocks"])
    app.include_router(entities.router, prefix="/{currency}", tags=["entities"])
    app.include_router(txs.router, prefix="/{currency}", tags=["txs"])
    app.include_router(rates.router, prefix="/{currency}", tags=["rates"])
    app.include_router(tokens.router, prefix="/{currency}", tags=["tokens"])
    app.include_router(bulk.router, prefix="/{currency}", tags=["bulk"])


def _setup_cors_middleware(app: FastAPI, config: GSRestConfig):
    """Setup CORS middleware on the app"""
    origins = config.ALLOWED_ORIGINS
    if isinstance(origins, str):
        origins = [origins] if origins != "*" else ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )


def create_app(
    config_file: str = None,
    validate_responses: bool = False,
    config: Optional[GSRestConfig] = None,
) -> FastAPI:
    """FastAPI application factory

    Args:
        config_file: Path to YAML config file
        validate_responses: Whether to validate responses (for testing)
        config: Pre-built GSRestConfig object (for testing, overrides config_file)
    """
    if config is None:
        if not config_file:
            config_file = CONFIG_FILE
        raw_config = load_config(config_file)
        config = GSRestConfig.from_dict(raw_config)

    # Load graphsense-lib config for slack hooks
    gslib_config = AppConfig()
    gslib_config.load()

    if gslib_config is not None:
        slack_exception_hook = gslib_config.get_slack_hooks_by_topic("exceptions")
        slack_info_hook = gslib_config.get_slack_hooks_by_topic("info")
        default_environment = config.environment or gslib_config.default_environment
    else:
        slack_exception_hook = None
        slack_info_hook = None
        default_environment = config.environment

    config.slack_info_hook = slack_info_hook

    setup_logging(logger, slack_exception_hook, default_environment, config.logging)

    app = FastAPI(
        title="GraphSense API",
        description="GraphSense API provides programmatic access to various cryptocurrency analytics features.",
        version="1.16.0rc2",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.state.config = config

    logger.info(f"ALLOWED_ORIGINS: {config.ALLOWED_ORIGINS}")
    _setup_cors_middleware(app, config)

    # Plugin middleware
    app.add_middleware(PluginMiddleware)

    # Empty params middleware (must be after PluginMiddleware to run first)
    app.add_middleware(EmptyQueryParamsMiddleware)

    _register_exception_handlers(app)
    _register_routers(app)

    return app


def create_app_from_dict(config_dict: dict) -> FastAPI:
    """Create FastAPI app from config dictionary (for testing)"""
    config = GSRestConfig.from_dict(config_dict)

    app = FastAPI(
        title="GraphSense API",
        version="1.16.0rc2",
        lifespan=lifespan,
    )

    app.state.config = config

    _setup_cors_middleware(app, config)
    app.add_middleware(PluginMiddleware)

    _register_exception_handlers(app)
    _register_routers(app)

    return app
