import importlib
from typing import Optional

from tagstore.db import TagstoreDbAsync, Taxonomies
from tagstore.db.database import get_db_engine_async


def get_cached_taxonomy_concept_label(app, tax, identifier) -> Optional[str]:
    return app["taxonomy-cache"]["labels"][tax].get(identifier, None)


def get_cached_is_abuse(app, identifier) -> bool:
    return identifier in app["taxonomy-cache"]["abuse"]


async def get_connection(app):
    config = app["config"]["database"]
    driver = config["driver"].lower()
    app.logger.info(f"Opening {driver} connection ...")
    mod = importlib.import_module("gsrest.db." + driver)
    cls = getattr(mod, driver.capitalize())
    app["db"] = cls(config, app.logger)

    ts_conf = app["config"]["gs-tagstore"]
    max_conn = ts_conf.get("pool_size", 50)
    max_pool_time = ts_conf.get("pool_timeout", 300)
    mo = ts_conf.get("max_overflow", 10)
    recycle = ts_conf.get("pool_recycle", 3600)
    engine = get_db_engine_async(
        ts_conf["url"],
        pool_size=int(max_conn),
        max_overflow=int(mo),
        pool_recycle=int(recycle),
        pool_timeout=int(max_pool_time),
        # echo=True,
    )

    # fetch taxonomy lookup
    tagstore_db = TagstoreDbAsync(engine)
    taxs = await tagstore_db.get_taxonomies({Taxonomies.CONCEPT, Taxonomies.COUNTRY})
    app["taxonomy-cache"] = {
        "labels": {
            Taxonomies.CONCEPT: {x.id: x.label for x in taxs.concept},
            Taxonomies.COUNTRY: {x.id: x.label for x in taxs.country},
        },
        "abuse": {x.id for x in taxs.concept if x.is_abuse},
    }

    app["gs-tagstore"] = engine

    app.logger.info("Setup done")

    yield

    app.logger.info("Begin app teardown")
    try:
        app["db"].close()
        app.logger.info(f"Closed {driver} connection.")
        app.logger.info(engine.pool.status())
        await engine.dispose()
        app.logger.info(engine.pool.status())
        app.logger.info("Closed Tagstore connection.")
    except Exception as x:
        app.logger.error(x)
