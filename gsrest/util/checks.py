from instance import config
from flask import abort


def crypto_in_config(crypto):
    if crypto not in config.MAPPING:
        abort(404, 'Unknown currency in config: {}' .format(crypto))
    return True
