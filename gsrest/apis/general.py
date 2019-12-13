from flask_restplus import Namespace, Resource
from flask import current_app

import gsrest.service.general_service as generalDAO
from gsrest.util.decorator import token_required
from gsrest.apis.common import search_response
from gsrest.apis.common import label_search_response
from gsrest.util.checks import check_inputs
import gsrest.service.addresses_service as addressesDAO
import gsrest.service.labels_service as labelsDAO
import gsrest.service.txs_service as txsDAO
from gsrest.service.addresses_service import ADDRESS_PREFIX_LENGTH
from gsrest.service.txs_service import TX_PREFIX_LENGTH

api = Namespace('general',
                path='/',
                description='General operations like stats and search')


# TODO: is a response model needed here?
@api.route("/stats")
class Statistics(Resource):
    def get(self):
        """
        Returns a JSON with statistics of all the available currencies
        """
        statistics = dict()
        for currency in current_app.config['MAPPING']:
            if currency != "tagpacks":
                statistics[currency] = generalDAO.get_statistics(currency)
        return statistics


@api.route("/<currency>/search/<expression>")
class Search(Resource):
    @token_required
    @api.marshal_with(search_response)
    def get(self, currency, expression):
        """
        Returns a JSON with a list of matching addresses and a list of
        matching transactions
        """
        check_inputs(currency=currency, address=expression, tx=expression)
        leading_zeros = 0
        pos = 0
        # leading zeros will be lost when casting to int
        while expression[pos] == "0":
            pos += 1
            leading_zeros += 1

        result = {"addresses": [], "txs": []}

        # Look for addresses and transactions
        if len(expression) >= TX_PREFIX_LENGTH:
            txs = txsDAO.list_matching_txs(currency, expression, leading_zeros)
            result["txs"] = txs

        if len(expression) >= ADDRESS_PREFIX_LENGTH:
            addresses = addressesDAO.list_matching_addresses(currency,
                                                             expression)
            result["addresses"] = addresses

        return result


@api.route("/search/labels/<label>")
class LabelSearch(Resource):
    @token_required
    @api.marshal_with(label_search_response)
    def get(self, label):
        """
        Returns a JSON with a list of matching labels
        """
        check_inputs(label=label)
        # TODO: capitalize all first letters of first word in error message
        return {'labels': labelsDAO.list_labels(label)}
