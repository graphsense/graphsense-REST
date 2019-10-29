import pytest
import json

from gsrest.db.user_db import get_db


@pytest.mark.parametrize(
    ('username', 'password', 'code', 'status', 'message'),
    (
        ('john', 'doe', 200, 'success', 'Success'),
        ('notjohn', 'notdoe', 401, 'fail', 'Error')
    ))
def test_login(client, username, password, code, status, message):
    response = client.post(
        '/login',
        data=json.dumps(dict(
            username=username,
            password=password
        )),
        content_type='application/json'
    )
    assert response.status_code == code
    data = json.loads(response.data.decode())
    assert data['status'] == status
    assert message in data['message']
    if response.status_code == 200:
        assert data['Authorization'] is not None


def test_logout(app, client):
    auth_token = 'test_token'
    response = client.post(
        '/logout',
        headers={'Authorization': auth_token}
    )
    assert response.status_code == 200
    with app.app_context():
        result = get_db().execute(
            "SELECT * FROM blacklist_tokens WHERE token LIKE '{}'"
            .format(auth_token)
        ).fetchone()
        assert result is not None
