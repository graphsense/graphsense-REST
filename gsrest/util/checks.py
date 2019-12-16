from flask import abort, current_app
MAX_DEPTH = 7
LABEL_PREFIX_LENGTH = 3


def check_inputs(**kwargs):
    for key, value in kwargs.items():
        if key in ['address', 'tx', 'direction']:
            if not isinstance(value, str) or not value.isalnum():
                abort(400, 'Invalid {}'.format(key))
        if key in ['page']:
            if value and not value.isalnum():
                abort(400, 'Invalid {}'.format(key))
        if key in ['pagesize'] and value:
            try:
                value = int(value)
            except:
                abort(400, 'Invalid {}'.format(key))
        if key in ['direction'] and value not in ['in', 'out']:
            abort(400, 'Invalid {}, it has to be either in or out'.format(key))
        if key in ['currency']:
            if value not in current_app.config['MAPPING']:
                abort(404, 'Unknown currency in config: {}'.format(value))
        if key in ['depth']:
            if value > MAX_DEPTH:
                abort(400, "Depth must not exceed %d".format(MAX_DEPTH))
        if key in ['category']:
            if not value:
                abort(400, "Missing {}, please specify one.".format(key))
            elif not isinstance(value, str) or not value.isalpha():
                abort(400, 'Invalid {}'.format(key))
        if key in ['label']:
            if not value:
                abort(400, "Missing {}, please specify one.".format(key))
            if len(value) < LABEL_PREFIX_LENGTH:
                abort(400, "Label parameter too short: at least {} characters"
                      .format(LABEL_PREFIX_LENGTH))
        elif key in ['height', 'entity']:
            if value is None:
                abort(400, 'Invalid {}'.format(key))

