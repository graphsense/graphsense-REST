import click
from flask import current_app
from flask.cli import with_appcontext
from sqlite3 import IntegrityError

from gsrest.model.user import User
from gsrest.db.user_db import get_db


def init_app(app):
    app.cli.add_command(create_user_command)


def create_user(username, password):
    db = get_db()

    user = User(username, password)

    try:
        db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
                   (user.username, user.password_hash))
        db.commit()
        current_app.logger.info('Created user %s', username)
    except IntegrityError:
        print('Error: Username already exists')


def find_user(username):
    db = get_db()

    db_user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if db_user is None:
        current_app.logger.info('User %s not found', username)
        return None
    else:
        user = User(username=db_user['username'])
        user.password_hash = db_user['password']
        current_app.logger.info('User %s found', username)
        return user


@click.command('create-user')
@click.argument('username')
@click.argument('password')
@with_appcontext
def create_user_command(username, password):
    """Clear the existing data and create new tables."""
    create_user(username, password)
    click.echo('Created user {}'.format(username))
