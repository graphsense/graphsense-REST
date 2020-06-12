from flask_restplus import Api
from gsrest._version import __version__ as version

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    title='GraphSense REST API',
    version=version,
    description='GraphSense REST API',
    authorizations=authorizations,
    security='apikey'
)
