from flask_restplus import Namespace, Resource

from gsrest.util.decorator import token_required

api = Namespace('blocks',
                path='/<currency>/blocks',
                description='Operations related to blocks')


@api.route("/")
class Blocks(Resource):
    @token_required
    def get(self, currency):
        return "NOT YET IMPLEMENTED"


@api.route("/<int:height>")
class Block(Resource):
    @token_required
    def get(self, currency, height):
        return "Requested currency {}, block {}".format(currency, height)


@api.route("/<int:height>/transactions")
class BlockTransactions(Resource):
    @token_required
    def get(self, currency, height):
        return "NOT YET IMPLEMENTED"
