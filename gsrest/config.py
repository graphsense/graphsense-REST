import os


class Config:
    """
    This class defines default configuration parameters for the GraphSense
    REST interface.

    Other required parameters (DB config, keyspaces) MUST be configurated in
    a separate config file and deployed in the ./instance folder.
    """

    USER_DB_FILE = 'users.sqlite'
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES_DAYS = 1
    USE_PROXY = False

    def __init__(self, instance_path):
        self.instance_path = instance_path

    @property
    def DATABASE(self):
        return os.path.join(self.instance_path, self.USER_DB_FILE)
