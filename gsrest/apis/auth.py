from flask import request
from flask_restplus import Namespace, Resource, fields

from gsrest.service.auth_helper import Auth

api = Namespace('auth',
                path='/',
                description='Operations related to client authentication')

auth_model = {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The user password'),
}
user_auth = api.model('auth_details', auth_model)


@api.route('/login')
class UserLogin(Resource):
    @api.expect(user_auth, validate=True)
    @api.doc(security=[])
    def post(self):
        """
        Returns a JWT token for a given username and password
        """
        return Auth.login_user(request)


@api.route('/logout')
class LogoutAPI(Resource):
    def post(self):
        """
        Blacklists a given JWT token
        """
        return Auth.logout_user(request)


@api.route('/refresh')
class RefreshToken(Resource):
    def get(self):
        """
        Get a fresh JWT token
        """
        return Auth.refresh_token(request)
