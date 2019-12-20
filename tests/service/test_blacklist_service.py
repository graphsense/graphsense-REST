from gsrest.db.user_db import get_db
from gsrest.service.blacklist_service import save_token, check_blacklist


def test_save_token(app):
    with app.app_context():
        save_token('test_token')
        result = get_db().execute(
            "SELECT * FROM blacklist_tokens WHERE token LIKE '{}'"
            .format('test_token')
        ).fetchone()
        assert result is not None


def test_save_existing_token(app):
    with app.app_context():
        save_token('test_token')
        save_token('test_token')
        result = get_db().execute(
            "SELECT count(*) FROM blacklist_tokens"
        ).fetchone()
        assert result[0] == 1


def test_check_blacklist(app):
    with app.app_context():
        save_token('test_token')
        assert check_blacklist('test_token') is True
        assert check_blacklist('no_token') is False
