from flask import current_app, g
import importlib


def init_app(app):
    get_connection()
    app.teardown_appcontext(close_connection)


def get_connection():
    if hasattr(g, 'connection'):
        return g.connection

    config = current_app.config['database']
    driver = config['driver'].lower()
    current_app.logger.info("Opening new {} connection.".format(driver))
    mod = importlib.import_module('gsrest.db.'+driver)
    cls = getattr(mod, driver.capitalize())
    g.connection = cls(config)
    return g.connection


def close_connection(e=None):
    if not hasattr(g, 'connection'):
        pass
    g.connection.close()
    g.pop('connection', None)
    driver = current_app.config['database']['driver']
    current_app.logger.info("Closed {} connection.".format(driver))
