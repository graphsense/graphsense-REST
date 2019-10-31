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
            abort(404, "Block height %d not found" % height)
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


@api.route("/<int:height>/transactions")
class BlockTransactions(Resource):
    @token_required
    def get(self, currency, height):
        return "NOT YET IMPLEMENTED"
