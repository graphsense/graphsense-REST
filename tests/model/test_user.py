import pytest

from gsrest.model.user import User
from gsrest.util.exceptions import MissingConfigError


def test_get_password():
    user = User('john')
    with(pytest.raises(AttributeError)):
        print(user.password)


def test_check_password():
    user = User('john', 'doe')
    assert user.check_password('doe')


def test_encode_auth_token(app):

    with app.app_context():
        user = User('john', 'doe')
        auth_token = user.encode_auth_token()

    assert isinstance(auth_token, bytes)


def test_encode_auth_token_failure(app):

    with app.app_context():
        user = User('john', 'doe')
        app.config['JWT_ACCESS_TOKEN_EXPIRES_DAYS'] = None
        with pytest.raises(MissingConfigError) as e:
            user.encode_auth_token()
            'not set' in e


def test_decode_auth_token(app):

    with app.app_context():
        user = User('john', 'doe')
        auth_token = user.encode_auth_token()
        decoded = User.decode_auth_token(auth_token)

    assert isinstance(auth_token, bytes)

    assert decoded == 'john'


def test_print_user():
    user = User('john', 'doe')
    assert 'john' in str(user)
    assert 'doe' not in str(user)
