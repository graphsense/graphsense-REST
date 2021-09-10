from flask import current_app
import importlib

connection = None


def get_connection():
    global connection
    if connection is not None:
        return connection

    config = current_app.config['database']
    driver = config['driver'].lower()
    current_app.logger.info(f"Opening {driver} connection ...")
    mod = importlib.import_module('gsrest.db.'+driver)
    cls = getattr(mod, driver.capitalize())
    connection = cls(config)
    return connection


def close_connection(e=None):
    if connection is None:
        return
    connection.close()
    driver = current_app.config['database']['driver']
    current_app.logger.info("Closed {} connection.".format(driver))
