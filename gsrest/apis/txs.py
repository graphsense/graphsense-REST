from flask import request, abort
from flask_restplus import Namespace, Resource, fields

from gsrest.util.decorator import token_required
from gsrest.apis.blocks import value_response
import gsrest.service.txs_service as txsDAO

api = Namespace('txs',
                path='/<currency>/txs',
                description='Operations related to transactions')


input_output_response = api.model("input_output_response", {
    "address": fields.String(required=True, description="Address"),
    "value": fields.Nested(value_response, required=True,
                           description="Input/Output value")
})


tx_response = api.model("tx_response", {
    "txHash": fields.String(required=True, description="Transaction hash"),
    "coinbase": fields.Boolean(required=True,
                               description="Coinbase transaction flag"),
    "height": fields.Integer(required=True, description="Transaction height"),
    "inputs": fields.List(fields.Nested(input_output_response), required=True,
                          description="Transaction inputs"),
    "outputs": fields.List(fields.Nested(input_output_response), required=True,
                           description="Transaction inputs"),
    "timestamp": fields.Integer(required=True,
                                description="Transaction timestamp"),
    "totalInput": fields.Nested(value_response, required=True),
    "totalOutput": fields.Nested(value_response, required=True),
})


@api.route("/<txHash>")
class Tx(Resource):
    @token_required
    @api.marshal_with(tx_response)
    def get(self, currency, txHash):
        """
        Returns details of a specific transaction identified by its hash.
        """
        tx = txsDAO.get_tx(currency, txHash)
        if not tx:
            abort(404, "Tx %s not found in currency %s"
                  % (txHash, currency))
        return tx


tx_list_response = api.model("tx_list_response", {
    "txs": fields.List(fields.Nested(tx_response),
                       required=True, description="Transaction list"),
    "nextPage": fields.String(required=True, description="The next page")
})


page_parser = api.parser()
page_parser.add_argument("page", location="args")


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
        return {"nextPage": paging_state.hex() if paging_state else None,
                "txs": txs}

