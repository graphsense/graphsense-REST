from flask import abort
from flask_restplus import Namespace, Resource

from gsrest.apis.common import page_parser, tx_response, tx_list_response
from gsrest.util.decorator import token_required
import gsrest.service.txs_service as txsDAO

api = Namespace('txs',
                path='/<currency>/txs',
                description='Operations related to transactions')


@api.route("/<tx_hash>")
@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('tx_hash', 'The transaction hash')
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
@api.param('currency', 'The cryptocurrency (e.g., btc)')
class TxList(Resource):
    @token_required
    @api.doc(parser=page_parser)
    @api.marshal_with(tx_list_response)
    def get(self, currency):
        """
        Returns a list of transactions (100 per page)
        """
        args = page_parser.parse_args()
        page = args.get("page")
        paging_state = bytes.fromhex(page) if page else None

        (paging_state, txs) = txsDAO.list_txs(currency, paging_state)
        return {"next_page": paging_state.hex() if paging_state else None,
                "txs": txs}
