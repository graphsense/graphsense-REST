from flask_restplus import Api

from gsrest.apis.auth import api as auth_api
from gsrest.apis.blocks import api as blocks_api
from gsrest.apis.rates import api as rates_api


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    title='GraphSense REST API',
    version='0.4.2-dev',
    description='GraphSense REST API',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(auth_api)
api.add_namespace(blocks_api)
api.add_namespace(rates_api)
