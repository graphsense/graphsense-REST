import json
import os
import tempfile

import pytest

from gsrest import create_app

from gsrest.db.user_db import init_db
from gsrest.service.user_service import create_user
from instance import config


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='john', password='doe'):
        response = self._client.post(
            '/login',
            data=json.dumps(dict(
                username=username,
                password=password
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self._client.environ_base['HTTP_AUTHORIZATION'] = data['Authorization']
        return response

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def app(monkeypatch):

    # temp user db location
    db_fd, db_path = tempfile.mkstemp()

    # we don't want to load exchange rates during testing
    def fake_load_all_exchange_rates():
        pass

    monkeypatch.setattr('gsrest.service.rates_service.load_all_exchange_rates',
                        fake_load_all_exchange_rates)

    db_test_conf = {
        'TESTING': True,
        'DATABASE': db_path,
        'JWT_ACCESS_TOKEN_EXPIRES_DAYS': 5,
        'SECRET_KEY': 'testing_secret',
        'MAPPING': config.MAPPING,
        'CASSANDRA_NODES': config.CASSANDRA_NODES
    }

    app = create_app(db_test_conf)

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
