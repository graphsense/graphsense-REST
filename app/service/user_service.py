import click
from flask.cli import with_appcontext

from app.model.user import User
from app.db.user_db import get_db


def init_app(app):
    app.cli.add_command(create_user_command)


def create_user(username, password):
    db = get_db()

    user = User(username, password)

    db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
               (user.username, user.password_hash)
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
