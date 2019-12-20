import gsrest
from gsrest import create_app


def test_config(runner, monkeypatch):

    def mock_load_config_from_file(*args):
        pass

    monkeypatch.setattr(gsrest, "load_config_from_file",
                        mock_load_config_from_file)

    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
