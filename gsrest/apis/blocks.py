from flask import request, abort
from flask_restplus import Namespace, Resource, fields

from gsrest.util.decorator import token_required

import gsrest.service.blocks_service as blocksDAO

api = Namespace('blocks',
                path='/<currency>/blocks',
                description='Operations related to blocks')


block_response = api.model("block_response", {
    "blockHash": fields.String(required=True, description="Block hash"),
    "height": fields.Integer(required=True, description="Block height"),
    "noTransactions": fields.Integer(
        required=True, description="Number of transactions"),
    "timestamp": fields.Integer(
        required=True, description="Transaction timestamp"),
})


@api.route("/<int:height>")
class Block(Resource):
    @token_required
    @api.marshal_with(block_response)
    def get(self, currency, height):
        """
        Returns details of a specific block identified by its height.
        """
        block = blocksDAO.get_block(currency, height)
        if not block:
            abort(404, "Block height %d not found in currency %s"
                  % (height, currency))
        return block


block_list_response = api.model("block_list_response", {
    "blocks": fields.List(fields.Nested(block_response),
                          required=True, description="Block list"),
    "nextPage": fields.String(required=True, description="The next page")
})


page_parser = api.parser()
page_parser.add_argument("page", location="args")


@api.route("/")
class BlockList(Resource):
    @token_required
    @api.doc(parser=page_parser)
    @api.marshal_with(block_list_response)
    def get(self, currency):
        """
        Returns a list of blocks (100 per page) and a resumption token for
        fetching the next page.
        """
        page = request.args.get("page")
        paging_state = bytes.fromhex(page) if page else None

        (paging_state, blocks) = blocksDAO.list_blocks(currency, paging_state)
        return {"nextPage": paging_state.hex() if paging_state else None,
                "blocks": blocks}
        return page


value_response = api.model("value_response", {
    "eur": fields.Float(required=True, description="EUR value"),
    "crypto": fields.Integer(required=True, description="Satoshi value"),
    "usd": fields.Float(required=True, description="USD value")
})


block_transaction_response = api.model("block_transaction_response", {
    "txHash": fields.String(required=True, description="Transaction hash"),
    "noInputs": fields.Integer(
        required=True, description="Number of inputs"),
    "noOutputs": fields.Integer(
        required=True, description="Number of outputs"),
    "totalInput": fields.Nested(
        value_response, required=True, description="Total input value"),
    "totalOutput": fields.Nested(
        value_response, required=True, description="Total output value")
})


block_transactions_response = api.model("block_transactions_response", {
    "height": fields.Integer(required=True, description="Block height"),
    "txs": fields.List(fields.Nested(
        block_transaction_response), required=True, description="Block list")
})


@api.route("/<int:height>/transactions")
class BlockTransactions(Resource):
    @token_required
    @api.marshal_with(block_transactions_response)
    def get(self, currency, height):
        """
        Returns a list of all transactions within a given block.
        """
        block_transactions = blocksDAO.list_block_transactions(currency,
                                                               height)

        if not block_transactions:
            abort(404, "Block height %d not found" % height)
        return block_transactions
