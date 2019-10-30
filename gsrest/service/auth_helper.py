from flask import current_app

from gsrest.model.user import User
from gsrest.service.user_service import find_user
from gsrest.service.blacklist_service import save_token


class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = find_user(data['username'])
            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token()
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Error: email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            current_app.logger.error('User login error: %s', e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if data:
            resp = User.decode_auth_token(data)
            if isinstance(resp, str):
                # mark the token as blacklisted
                save_token(token=data)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
            # get the auth token
            auth_token = new_request.headers.get('Authorization')
            if auth_token:
                resp = User.decode_auth_token(auth_token)
                user = find_user(resp)
                if user:
                    response_object = {
                        'status': 'success',
                        'data': {
                            'user_id': user.username
                        }
                    }
                    return response_object, 200
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return response_object, 401
