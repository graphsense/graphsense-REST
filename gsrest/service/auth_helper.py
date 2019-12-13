from flask import current_app, jsonify

from gsrest.model.user import User
from gsrest.service.user_service import find_user
from gsrest.service.blacklist_service import save_token

header_name = 'Authorization'

class Auth:

    @staticmethod
    def login_user(request):
        data = request.json
        try:
            # fetch the user data
            user = find_user(data['username'])
            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token()
                if auth_token:
                    response = jsonify({
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        header_name: auth_token.decode()
                    })
                    response.set_cookie(header_name, auth_token.decode(), httponly=True)
                    return response
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
    def logout_user(request):
        data = request.cookies.get(header_name) or request.headers.get(header_name)
        if data:
            resp = User.decode_auth_token(data)
            if isinstance(resp, str):
                # mark the token as blacklisted
                save_token(token=data)
                response = jsonify({
                    'status': 'success',
                    'message': 'Successfully logged out.'
                })
                response.set_cookie(header_name, '', httponly=True)
                return response_object
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
        auth_token = new_request.cookies.get(header_name) or new_request.headers.get(header_name)
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

    @staticmethod
    def refresh_token(request):
        auth_token = request.cookies.get(header_name) or request.headers.get(header_name)
        if not auth_token:
            return {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }, 401
        resp = User.decode_auth_token(auth_token)
        if not resp:
            return {
                'status': 'fail',
                'message': resp
            }, 401
        user = find_user(resp)
        if not user:
            return {
                'status': 'fail',
                'message': 'Invalid user'
            }, 401
        old_auth_token = auth_token
        auth_token = user.encode_auth_token()
        if not auth_token:
            return {
                'status': 'fail',
                'message': 'Could not generate auth token'
            }, 500
        # mark the old token as blacklisted
        save_token(token=old_auth_token)
        response = jsonify({
            'status': 'success',
            'message': 'Successfully refreshed auth token.',
            header_name: auth_token.decode()
        })
        response.set_cookie(header_name, auth_token.decode(), httponly=True)
        return response
        


