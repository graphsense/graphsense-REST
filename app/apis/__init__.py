from flask_restplus import Api

from .auth import api as auth_api
from .blocks import api as blocks_api

api = Api(
    title='GraphSense REST API',
    version='0.4.2-dev',
    description='GraphSense REST API'
)

api.add_namespace(auth_api)
api.add_namespace(blocks_api)
