import sys
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

USER_DB_PATH = 'db/user_db_schema.sql'


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db():
    if 'db' not in g:
        current_app.logger.info("Establishing user DB connection.")
        try:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
        except Exception:
            current_app.logger.error("User DB connection error")
            sys.exit()
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    try:
        with current_app.open_resource(USER_DB_PATH) as f:
            db.executescript(f.read().decode('utf8'))
    except Exception:
        current_app.logger.error("Execution of user DB SQL script failed")
        sys.exit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
