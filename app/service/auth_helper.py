from app.model.user import User
from app.service.user_service import find_user
from app.service.blacklist_service import save_token


class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = find_user(data['username'])
            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token(user.username)
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
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if data:
            resp = User.decode_auth_token(data)
            print(resp)
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
