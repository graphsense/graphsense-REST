from gsrest.service.user_service import (create_user, find_user,
                                         create_user_command)

from gsrest.db.user_db import get_db


def test_create_user(app):
    with app.app_context():
        create_user('johnny', 'doey')
        result = get_db().execute(
            "SELECT * FROM user WHERE username LIKE '{}'"
            .format('johnny')
        ).fetchone()
        assert result is not None


def test_find_user(app):
    with app.app_context():
        user = find_user('john')
        assert user is not None
        assert user.username == 'john'
        assert user.check_password('doe')


def test_create_user_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_create_user(username, password):
        Recorder.called = True

    monkeypatch.setattr('gsrest.service.user_service.create_user',
                        fake_create_user)
    result = runner.invoke(create_user_command, ['johnny', 'doey'])
    assert 'Created user johnny' in result.output
    assert Recorder.called
