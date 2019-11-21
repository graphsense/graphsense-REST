from flask import abort
from flask_restplus import Namespace, Resource

from gsrest.util.decorator import token_required

import gsrest.service.rates_service as ratesDAO

api = Namespace('exchange_rates',
                path='/<currency>/exchange_rates',
                description='Operations related to exchange rates')


@api.route("/<int:height>")
class ExchangeRate(Resource):
    @token_required
    def get(self, currency, height):
        """
        Returns exchange rate for a given height
        """
        rate = ratesDAO.get_exchange_rate(currency, height)
        if not rate:
            abort(404, "Exchange rate for height {} not found in currency {}"
                  .format(height, currency))
        return rate
