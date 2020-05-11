from flask_restplus import Namespace, Resource
from flask import Response, abort

from gsrest.apis.common import page_parser, block_response, \
    block_list_response, block_txs_response
import gsrest.service.blocks_service as blocksDAO
from gsrest.util.checks import check_inputs
from gsrest.util.csvify import txs_to_csv, create_download_header
from gsrest.util.decorator import token_required

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
        check_inputs(currency=currency, height=height)
        block = blocksDAO.get_block(currency, height)
        if block:
            return block
        abort(404, "Block {} not found in currency {}".format(height,
                                                              currency))


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
        args = page_parser.parse_args()
        page = args.get("page")
        check_inputs(currency=currency, page=page)
        paging_state = bytes.fromhex(page) if page else None
        paging_state, blocks = blocksDAO.list_blocks(currency, paging_state)
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
        check_inputs(currency=currency, height=height)
        block_txs = blocksDAO.list_block_txs(currency, height)
        if block_txs:
            return block_txs
        abort(404, "Block {} not found in currency {}".format(height,
                                                              currency))


@api.route("/<int:height>/txs.csv")
@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('height', 'The block height')
class BlockTxsCSV(Resource):
    @token_required
    def get(self, currency, height):
        """
        Returns a CSV with all the transactions of the block
        """
        check_inputs(currency=currency, height=height)
        block_txs = blocksDAO.list_block_txs(currency, height)
        if block_txs:
            return Response(txs_to_csv(block_txs), mimetype="text/csv",
                            headers=create_download_header(
                                'transactions of block {} ({}).csv'
                                .format(height, currency.upper())))
        abort(404, "Block {} not found in currency {}".format(height,
                                                              currency))
