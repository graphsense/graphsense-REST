import importlib

connection = None


async def get_connection(app):
    config = app['config']['database']
    driver = config['driver'].lower()
    app.logger.info(f"Opening {driver} connection ...")
    mod = importlib.import_module('gsrest.db.'+driver)
    cls = getattr(mod, driver.capitalize())
    app['db'] = cls(config, app.logger)
    yield

    app['db'].close()
    app.logger.info("Closed {} connection.".format(driver))
