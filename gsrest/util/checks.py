from instance import config
from flask import abort


def crypto_in_config(crypto):
    if crypto not in config.MAPPING:
        abort(404, 'Unknown currency in config: {}' .format(crypto))
    return True


def check_input(expression, type):
    if type in ['address', 'tx']:
        if not isinstance(expression, str) or not expression.isalnum():
            abort(400, 'Invalid {}'.format(type))
    # elif: add other cases if needed
