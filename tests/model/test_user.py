import pytest

from gsrest.model.user import User


def test_get_password():
    user = User('john')
    with(pytest.raises(AttributeError)):
        print(user.password)


def test_check_password():
    user = User('john', 'doe')
    assert user.check_password('doe')


def test_encode_decode_auth_token(app):

    with app.app_context():
        user = User('john', 'doe')
        auth_token = user.encode_auth_token()
        decoded = User.decode_auth_token(auth_token)

    assert isinstance(auth_token, bytes)

    assert decoded == 'john'
