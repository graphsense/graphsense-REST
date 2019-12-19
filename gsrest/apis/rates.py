from flask import abort
from flask_restplus import Namespace, Resource

from gsrest.util.decorator import token_required
from gsrest.apis.common import height_rates_response
import gsrest.service.rates_service as ratesDAO
from gsrest.util.checks import check_inputs

api = Namespace('rates',
                path='/<currency>/rates',
                description='Operations related to exchange rates')


@api.route("/<int:height>")
@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('height', 'The block height')
class ExchangeRate(Resource):
    @token_required
    @api.marshal_with(height_rates_response)
    def get(self, currency, height):
        """
        Returns exchange rate for a given height
        """
        check_inputs(currency=currency, height=height)
        rates = ratesDAO.get_rates(currency, height)
        if not rates:
            abort(404, "Exchange rate for height {} not found in currency {}"
                  .format(height, currency))
        return rates
