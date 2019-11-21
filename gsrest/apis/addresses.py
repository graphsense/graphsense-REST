from flask import abort
from flask_restplus import Namespace, Resource, fields

from gsrest.util.decorator import token_required
from gsrest.apis.blocks import value_response
import gsrest.service.addresses_service as addressesDAO

api = Namespace('addresses',
                path='/<currency>/addresses',
                description='Operations related to addresses')

tx_summary_response = api.model("tx_summary_response", {
    "height": fields.Integer(required=True, description="Transaction height"),
    "timestamp": fields.Integer(required=True,
                                description="Transaction timestamp"),
    "txHash": fields.String(required=True, description="Transaction hash")
})

address_response = api.model("address_response", {
    "address": fields.String(required=True, description="Address"),
    "addressId": fields.Integer(required=True, description="Address ID"),
    # "balance": fields.Nested(value_response, required=True),
    "firstTx": fields.Nested(tx_summary_response, required=True),
    "lastTx": fields.Nested(tx_summary_response, required=True),
    "inDegree": fields.Integer(required=True, description="inDegree value"),
    "outDegree": fields.Integer(required=True, description="outDegree value"),
    "noIncomingTxs": fields.Integer(required=True,
                                    description="Incoming transactions"),
    "noOutgoingTxs": fields.Integer(required=True,
                                    description="Outgoing transactions"),
    "totalReceived": fields.Nested(value_response, required=True),
    "totalSpent": fields.Nested(value_response, required=True)
})


@api.route("/<address>")
class Address(Resource):
    @token_required
    @api.marshal_with(address_response)
    def get(self, currency, address):
        """
        Returns details of a specific address.
        """
        addr = addressesDAO.get_address(currency, address)
        if not addr:
            abort(404, "Address {} not found in currency {}"
                  .format(address, currency))
        return addr

# TODO: AddressTransactions, AddressIncomingRelations, AddressOutgoingRelations, AddressSummary
