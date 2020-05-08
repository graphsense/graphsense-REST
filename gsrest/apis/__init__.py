from flask_restplus import Api

from gsrest._version import __version__ as version
from gsrest.apis.auth import api as auth_api
from gsrest.apis.addresses import api as addresses_api
from gsrest.apis.blocks import api as blocks_api
from gsrest.apis.common import api as common_api
from gsrest.apis.entities import api as entities_api
from gsrest.apis.general import api as general_api
from gsrest.apis.tags import api as tags_api
from gsrest.apis.rates import api as rates_api
from gsrest.apis.txs import api as txs_api


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

api.add_namespace(common_api)
api.add_namespace(auth_api)
api.add_namespace(auth_api)
api.add_namespace(blocks_api)
api.add_namespace(rates_api)
api.add_namespace(txs_api)
api.add_namespace(addresses_api)
api.add_namespace(entities_api)
api.add_namespace(tags_api)
api.add_namespace(general_api)
