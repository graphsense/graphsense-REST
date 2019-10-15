from werkzeug.security import generate_password_hash, check_password_hash


class User(object):
    """ User Model for storing user related details """

    def __init__(self, username, password):
        if not username:
            raise Exception("Username is required")
        if not password:
            raise Exception("Password is required")
        self.username = username
        self.password = password

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)
