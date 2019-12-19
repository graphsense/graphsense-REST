from flask_restplus import Namespace, Resource
from flask import current_app

from gsrest.apis.common import search_parser, search_response
import gsrest.service.addresses_service as addressesDAO
import gsrest.service.general_service as generalDAO
import gsrest.service.labels_service as labelsDAO
import gsrest.service.txs_service as txsDAO
from gsrest.util.checks import check_inputs
from gsrest.util.decorator import token_required

api = Namespace('general',
                path='/',
                description='General operations like stats and search')


# TODO: is a response model needed here?
@api.route("/stats")
class Statistics(Resource):
    def get(self):
        """
        Returns summary statistics on all available currencies
        """
        statistics = dict()
        for currency in current_app.config['MAPPING']:
            if currency != "tagpacks":
                statistics[currency] = generalDAO.get_statistics(currency)
        return statistics


@api.param('expression', 'It can be (the beginning of) an address, '
                         'a transaction or a label')
@api.route("/search/<expression>")
class Search(Resource):
    @token_required
    @api.doc(parser=search_parser)
    @api.marshal_with(search_response)
    def get(self, expression):
        """
        Returns matching addresses, transactions and labels
        """
        # TODO: too slow with bech32 address search
        args = search_parser.parse_args()
        currency = args['currency']
        limit = args['limit']
        currencies = [c for c in current_app.config['MAPPING']
                      if c != 'tagpacks']
        if currency:
            check_inputs(currency=currency)
            currencies = [currency]
        can_be_label, can_be_tx_address = check_inputs(expression=expression)
        leading_zeros = 0
        pos = 0
        # leading zeros will be lost when casting to int
        while expression[pos] == "0":
            pos += 1
            leading_zeros += 1

        result = dict()
        result['currencies'] = []

        if can_be_tx_address:
            for currency in currencies:
                element = dict()
                element['addresses'] = []
                element['txs'] = []
                element['currency'] = currency

                # Look for addresses and transactions
                if len(expression) >= txsDAO.TX_PREFIX_LENGTH:
                    txs = txsDAO.list_matching_txs(currency,
                                                   expression,
                                                   leading_zeros)
                    element["txs"] = txs[:limit]

                if len(expression) >= addressesDAO.ADDRESS_PREFIX_LENGTH:
                    addresses = \
                        addressesDAO.list_matching_addresses(currency,
                                                             expression)
                    element["addresses"] = addresses[:limit]

                result['currencies'].append(element)

        result['labels'] = []
        if can_be_label:
            result['labels'] = labelsDAO.list_labels(args['currency'],
                                                     expression)[:limit]

        return result
