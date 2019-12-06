from flask import request, abort
from flask_restplus import Namespace, Resource, fields

from gsrest.apis.common import page_parser, block_response, \
    block_list_response, block_txs_response
from gsrest.util.decorator import token_required
import gsrest.service.blocks_service as blocksDAO

api = Namespace('blocks',
                path='/<currency>/blocks',
                description='Operations related to blocks')


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
    @api.doc(parser=page_parser)
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
