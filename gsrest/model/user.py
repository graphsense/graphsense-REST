import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from gsrest.service.blacklist_service import check_blacklist

from flask import current_app


class User(object):
    """ User Model for storing user related details """

    def __init__(self, username, password=None):
        if not username:
            raise Exception("Username is required")
        self.username = username
        if password:
            self.password = password

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_auth_token(self):
            """
            Generates the Auth Token
            :return: string
            """
            try:
                payload = {
                    'exp': datetime.datetime.utcnow() +
                    datetime.timedelta(
                        current_app.config['JWT_ACCESS_TOKEN_EXPIRES_DAYS']),
                    'iat': datetime.datetime.utcnow(),
                    'sub': self.username
                }
                return jwt.encode(
                    payload,
                    current_app.config['SECRET_KEY'],
                    algorithm='HS256'
                )
            except Exception as e:
                return e

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config['SECRET_KEY'])
            is_blacklisted_token = check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
