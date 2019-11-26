from flask import request, abort
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
    "tx_hash": fields.String(required=True, description="Transaction hash")
})

address_response = api.model("address_response", {
    "address": fields.String(required=True, description="Address"),
    "balance": fields.Nested(value_response, required=True),
    "first_tx": fields.Nested(tx_summary_response, required=True),
    "last_tx": fields.Nested(tx_summary_response, required=True),
    "in_degree": fields.Integer(required=True, description="in_degree value"),
    "out_degree": fields.Integer(required=True, description="outDegree value"),
    "no_incoming_txs": fields.Integer(required=True,
                                      description="Incoming transactions"),
    "no_outgoing_txs": fields.Integer(required=True,
                                      description="Outgoing transactions"),
    "total_received": fields.Nested(value_response, required=True),
    "total_spent": fields.Nested(value_response, required=True)
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


address_tx_response = api.model("address_tx_response", {
    "address": fields.String(required=True, description="Address"),
    "height": fields.Integer(required=True, description="Transaction height"),
    "timestamp": fields.Integer(required=True,
                                description="Transaction timestamp"),
    "tx_hash": fields.String(required=True, description="Transaction hash"),
    "value": fields.Nested(value_response, required=True)
})

address_txs_response = api.model("address_txs_response", {
    "next_page": fields.String(required=True, description="The next page"),
    "address_txs": fields.List(fields.Nested(address_tx_response),
                               required=True,
                               description="The list of transactions")
})

page_parser = api.parser()
page_parser.add_argument("page", location="args")


@api.route("/<address>/txs")
class AddressTxs(Resource):
    @token_required
    @api.doc(parser=page_parser)
    @api.marshal_with(address_txs_response)
    def get(self, currency, address):
        """
        Returns transactions of a specific address.
        """
        page = request.args.get("page")
        paging_state = bytes.fromhex(page) if page else None
        # TODO: check paging_state
        paging_state, address_txs = addressesDAO.list_address_txs(currency,
                                                                  address,
                                                                  paging_state)
        if not address_txs:
            abort(404, "Address {} not found in currency {}"
                  .format(address, currency))

        return {"next_page": paging_state.hex() if paging_state else None,
                "address_txs": address_txs}


# TODO: AddressTransactions, AddressIncomingRelations, AddressOutgoingRelations, AddressSummary
