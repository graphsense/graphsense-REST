from flask import request
from flask_restplus import Namespace, Resource, fields

from gsrest.service.auth_helper import Auth

api = Namespace('auth',
                path='/',
                description='Operations related to client authentication')


user_auth = api.model('auth_details', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The user password'),
})


@api.route('/login')
class UserLogin(Resource):
    @api.expect(user_auth, validate=True)
    @api.doc(security=[])
    def post(self):
        """
        Returns a JWT token for a given username and password
        """
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    def post(self):
        """
        Blacklists a given JWT token
        """
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
