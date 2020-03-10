from gsrest import create_app


def test_config(runner, monkeypatch):

    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
