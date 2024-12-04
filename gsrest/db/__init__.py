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

    engine = get_db_engine_async(app["config"]["gs-tagstore"]["url"])

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

    yield

    app["db"].close()
    app.logger.info(f"Closed {driver} connection.")
