import importlib
from tagstore.db.database import get_db_engine_async

connection = None


async def get_connection(app):
    config = app['config']['database']
    driver = config['driver'].lower()
    app.logger.info(f"Opening {driver} connection ...")
    mod = importlib.import_module('gsrest.db.' + driver)
    cls = getattr(mod, driver.capitalize())
    app['db'] = cls(config, app.logger)
    # app['tagstores'] = [
    #     Tagstore(conf, app.logger) for conf in app['config']['tagstores']
    # ]

    app['gs-tagstore'] = get_db_engine_async(
        app['config']['gs-tagstore']['url'])
    # aws = [ts.connect() for ts in app['tagstores']]
    # await asyncio.gather(*aws)
    yield

    app['db'].close()
    app.logger.info(f"Closed {driver} connection.")

    # aws = [ts.close() for ts in app['tagstores']]
    # await asyncio.gather(*aws)
    # app.logger.info("Closed tagstore connections.")
