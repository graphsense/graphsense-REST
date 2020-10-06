import logging
import os

import connexion
from flask_testing import TestCase

from openapi_server.encoder import JSONEncoder
from openapi_server import main


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        return main(os.path.join(os.getcwd(), 'tests/instance')).app
