import os


class Config(object):

    def __init__(self, instance_path):
        self.instance_path = instance_path

    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    CASSANDRA_NODES = ["localhost"]
    MAPPING = {
        "tagpacks": "tagpacks",
        "btc": ["btc_raw", "btc_transformed"],
        "bch": ["bch_raw", "bch_transformed"],
        "ltc": ["ltc_raw", "ltc_transformed"],
        "zec": ["zec_raw", "zec_transformed"]
    },
    JWT_ACCESS_TOKEN_EXPIRES_DAYS = 1

    @property
    def DATABASE(self):
        return os.path.join(self.instance_path, 'users.sqlite')
