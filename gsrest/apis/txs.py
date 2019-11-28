from flask import request, abort
from flask_restplus import Namespace, Resource, fields

from gsrest.util.decorator import token_required
from gsrest.apis.blocks import value_response
import gsrest.service.txs_service as txsDAO

api = Namespace('txs',
                path='/<currency>/txs',
                description='Operations related to transactions')

page_parser = api.parser()
page_parser.add_argument("page", location="args")

tx_summary_model = {
    "height": fields.Integer(required=True, description="Transaction height"),
    "timestamp": fields.Integer(required=True,
                                description="Transaction timestamp"),
    "tx_hash": fields.String(required=True, description="Transaction hash")
}
tx_summary_response = api.model("tx_summary_response", tx_summary_model)


input_output_model = {
    "address": fields.String(required=True, description="Address"),
    "value": fields.Nested(value_response, required=True,
                           description="Input/Output value")
}
input_output_response = api.model("input_output_response", input_output_model)

tx_model = {
    "tx_hash": fields.String(required=True, description="Transaction hash"),
    "coinbase": fields.Boolean(required=True,
                               description="Coinbase transaction flag"),
    "height": fields.Integer(required=True, description="Transaction height"),
    "inputs": fields.List(fields.Nested(input_output_response), required=True,
                          description="Transaction inputs"),
    "outputs": fields.List(fields.Nested(input_output_response), required=True,
                           description="Transaction inputs"),
    "timestamp": fields.Integer(required=True,
                                description="Transaction timestamp"),
    "total_input": fields.Nested(value_response, required=True),
    "total_output": fields.Nested(value_response, required=True),
}
tx_response = api.model("tx_response", tx_model)

tx_list_model = {
    "txs": fields.List(fields.Nested(tx_response),
                       required=True, description="Transaction list"),
    "next_page": fields.String(required=True, description="The next page")
}
tx_list_response = api.model("tx_list_response", tx_list_model)


@api.route("/<tx_hash>")
class Tx(Resource):
    @token_required
    @api.marshal_with(tx_response)
    def get(self, currency, tx_hash):
        """
        Returns details of a specific transaction identified by its hash.
        """
        tx = txsDAO.get_tx(currency, tx_hash)
        if not tx:
            abort(404, "Transaction {} not found in currency {}"
                  .format(tx_hash, currency))
        return tx


@api.route("/")
class TxList(Resource):
    @token_required
    @api.doc(parser=page_parser)
    @api.marshal_with(tx_list_response)
    def get(self, currency):
        """
        Returns a list of transactions (100 per page) and a resumption token
        for fetching the next page.
        """
        page = request.args.get("page")
        paging_state = bytes.fromhex(page) if page else None

        (paging_state, txs) = txsDAO.list_txs(currency, paging_state)
        return {"next_page": paging_state.hex() if paging_state else None,
                "txs": txs}

