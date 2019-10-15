from werkzeug.security import generate_password_hash

import click
from flask.cli import with_appcontext

from app.db.user_db import get_db


def init_app(app):
    app.cli.add_command(create_user_command)


def create_user(username, password):
    db = get_db()

    if not username:
        raise Exception("Username is required")
    if not password:
        raise Exception("Password is required")

    db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
               (username, generate_password_hash(password))
               )
    db.commit()


@click.command('create-user')
@click.argument('username')
@click.argument('password')
@with_appcontext
def create_user_command(username, password):
    """Clear the existing data and create new tables."""
    create_user(username, password)
    click.echo('Created user {}'.format(username))
