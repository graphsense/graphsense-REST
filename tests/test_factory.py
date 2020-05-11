import gsrest
from gsrest import create_app


def test_config(runner, monkeypatch):

    def mock_load_config(*args, **kwargs):
        pass

    monkeypatch.setattr(gsrest, "load_config", mock_load_config)

    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
