from flask_restplus import Namespace, Resource

# from app.service.user_service import create_user

api = Namespace('auth',
                path='/',
                description='Operations related to authentication')


@api.route("/login", methods=["GET"])
class UserLogin(Resource):
    def get(self):
        return "NOT yet implemented"


@api.route("/token_refresh", methods=["GET"])
class UserTokenRefresh(Resource):
    def get(self):
        return "NOT yet implemented"


@api.route("/logout_refresh", methods=["GET"])
class UserLogoutRefresh(Resource):
    def get(self):
        return "NOT yet implemented"


@api.route("/logout_access", methods=["GET"])
class UserLogoutAccess(Resource):
    def get(self):
        return "NOT yet implemented"
