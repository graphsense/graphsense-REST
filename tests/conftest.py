import os
import tempfile

import pytest

from gsrest import create_app

from gsrest.db.user_db import init_db
from gsrest.service.user_service import create_user


@pytest.fixture
def application():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        create_user('john', 'doe')

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(application):
    return application.test_client()


@pytest.fixture
def runner(application):
    return application.test_cli_runner()
