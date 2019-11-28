from flask import request, abort
from flask_restplus import Namespace, Resource, fields

from gsrest.apis.common import page_parser
from gsrest.util.decorator import token_required
import gsrest.service.blocks_service as blocksDAO

api = Namespace('blocks',
                path='/<currency>/blocks',
                description='Operations related to blocks')


block_model = {
    "block_hash": fields.String(required=True, description="Block hash"),
    "height": fields.Integer(required=True, description="Block height"),
    "no_txs": fields.Integer(
        required=True, description="Number of transactions"),
    "timestamp": fields.Integer(
        required=True, description="Transaction timestamp"),
}
block_response = api.model("block_response", block_model)

block_list_model = {
    "blocks": fields.List(fields.Nested(block_response),
                          required=True, description="Block list"),
    "next_page": fields.String(required=True, description="The next page")
}
block_list_response = api.model("block_list_response", block_list_model)

value_model = {
    "eur": fields.Float(required=True, description="EUR value"),
    "value": fields.Integer(required=True, description="Value"),
    "usd": fields.Float(required=True, description="USD value")
}
value_response = api.model("value_response", value_model)

block_tx_model = {
    "tx_hash": fields.String(required=True, description="Transaction hash"),
    "no_inputs": fields.Integer(
        required=True, description="Number of inputs"),
    "no_outputs": fields.Integer(
        required=True, description="Number of outputs"),
    "total_input": fields.Nested(
        value_response, required=True, description="Total input value"),
    "total_output": fields.Nested(
        value_response, required=True, description="Total output value")
}
block_tx_response = api.model("block_tx_response", block_tx_model)

block_txs_model = {
    "height": fields.Integer(required=True, description="Block height"),
    "txs": fields.List(fields.Nested(
        block_tx_response), required=True, description="Block list")
}
block_txs_response = api.model("block_txs_response", block_txs_model)


@api.route("/<int:height>")
@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('height', 'The block height')
class Block(Resource):
    @token_required
    @api.marshal_with(block_response)
    def get(self, currency, height):
        """
        Returns details of a specific block identified by its height
        """
        block = blocksDAO.get_block(currency, height)
        if not block:
            abort(404, "Block %d not found in currency %s"
                  % (height, currency))
        return block


@api.route("/")
@api.param('currency', 'The cryptocurrency (e.g., btc)')
class BlockList(Resource):
    @token_required
    @api.doc(parser=page_parser(api))
    @api.marshal_with(block_list_response)
    def get(self, currency):
        """
        Returns a list of blocks (100 per page)
        """
        page = request.args.get("page")
        paging_state = bytes.fromhex(page) if page else None

        (paging_state, blocks) = blocksDAO.list_blocks(currency, paging_state)
        return {"next_page": paging_state.hex() if paging_state else None,
                "blocks": blocks}


@api.route("/<int:height>/txs")
@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('height', 'The block height')
class BlockTxs(Resource):
    @token_required
    @api.marshal_with(block_txs_response)
    def get(self, currency, height):
        """
        Returns a list of all transactions within a given block.
        """
        block_txs = blocksDAO.list_block_txs(currency, height)

        if not block_txs:
            abort(404, "Block %d not found" % height)
        return block_txs
