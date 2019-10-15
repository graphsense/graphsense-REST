from flask_restplus import Namespace, Resource

api = Namespace('blocks',
                path='/<currency>/blocks',
                description='Operations related to blocks')


@api.route("/")
class Blocks(Resource):
    def get(self, currency):
        return "NOT YET IMPLEMENTED"


@api.route("/<int:height>")
class Block(Resource):
    def get(self, currency, height):
        return "Requested currency {}, block {}".format(currency, height)


@api.route("/<int:height>/transactions")
class BlockTransactions(Resource):
    def get(self, currency, height):
        return "NOT YET IMPLEMENTED"
