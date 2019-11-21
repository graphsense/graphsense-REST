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
    "noTxs": fields.Integer(
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
            abort(404, "Block %d not found in currency %s"
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


value_response = api.model("value_response", {
    "eur": fields.Float(required=True, description="EUR value"),
    "value": fields.Integer(required=True, description="Satoshi value"),
    "usd": fields.Float(required=True, description="USD value")
})


block_tx_response = api.model("block_tx_response", {
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


block_txs_response = api.model("block_txs_response", {
    "height": fields.Integer(required=True, description="Block height"),
    "txs": fields.List(fields.Nested(
        block_tx_response), required=True, description="Block list")
})


@api.route("/<int:height>/txs")
class BlockTxs(Resource):
    @token_required
    @api.marshal_with(block_txs_response)
    def get(self, currency, height):
        """
        Returns a list of all txs within a given block.
        """
        block_txs = blocksDAO.list_block_txs(currency, height)

        if not block_txs:
            abort(404, "Block %d not found" % height)
        return block_txs
