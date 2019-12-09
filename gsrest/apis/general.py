from flask_restplus import Namespace, Resource

import gsrest.service.general_services as generalDAO
from gsrest.util.checks import config
from gsrest.util.decorator import token_required


api = Namespace('general',
                path='/general',
                description='General operations')


# TODO: is a response model needed here?
@api.route("/stats")
class Statistics(Resource):
    @token_required
    def get(self):
        """
        Returns a JSON with statistics of all the available currencies
        """
        statistics = dict()
        for currency in config.MAPPING:
            if currency != "tagpacks":
                statistics[currency] = generalDAO.get_statistics(currency)
        return statistics
