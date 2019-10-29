import os
import tempfile

import pytest

from gsrest import create_app

from gsrest.db.user_db import init_db
from gsrest.service.user_service import create_user


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='john', password='doe'):
        return self._client.post(
            '/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'JWT_ACCESS_TOKEN_EXPIRES_DAYS': 5,
        'SECRET_KEY': 'testing_secret'
    })

    with app.app_context():
        init_db()
        create_user('john', 'doe')

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    return AuthActions(client)
