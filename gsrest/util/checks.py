from instance import config
from flask import abort
import re

pattern = re.compile(r"[\W_]+", re.UNICODE)  # only alphanumeric chars for label


def crypto_in_config(crypto):
    if crypto not in config.MAPPING:
        abort(404, 'Unknown currency in config: {}' .format(crypto))
    return True


def alphanumeric_lower(expression):
    return pattern.sub("", expression).lower()
