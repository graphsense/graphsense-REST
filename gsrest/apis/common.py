from flask_restplus import Namespace, fields

api = Namespace('common',
                path='/',
                description='Common models and definitions')

"""
REST interface argument parsers
"""

page_parser = api.parser()
page_parser.add_argument(
    "page", type="str", location="args",
    help="Resumption token for retrieving the next page")

"""
Type definitions reused across interfaces
"""

value_model = {
    "eur": fields.Float(required=True, description="EUR value"),
    "value": fields.Integer(required=True, description="Value"),
    "usd": fields.Float(required=True, description="USD value")
}

address_model = {
    "address": fields.String(required=True, description="Address"),
    "balance": fields.Nested(value_response, required=True,
                             description="Balance"),
    "first_tx": fields.Nested(tx_summary_response, required=True,
                              description="First transaction"),
    "last_tx": fields.Nested(tx_summary_response, required=True,
                             description="Last transaction"),
    "in_degree": fields.Integer(required=True, description="In-degree value"),
    "out_degree": fields.Integer(required=True,
                                 description="Out-degree value"),
    "no_incoming_txs": fields.Integer(required=True,
                                      description="Incoming transactions"),
    "no_outgoing_txs": fields.Integer(required=True,
                                      description="Outgoing transactions"),
    "total_received": fields.Nested(value_response, required=True,
                                    description="Total received"),
    "total_spent": fields.Nested(value_response, required=True,
                                 description="Total spent"),
}


def get_value_response(api):
    return api.model("value_response", value_model)


def get_page_parser(api):
    page_parser = api.parser()
    page_parser.add_argument(
        "page", type="str", location="args",
        help="Resumption token for retrieving the next page")
    return page_parser


value_response = api.model("value_response", value_model)

tx_summary_model = {
    "height": fields.Integer(required=True, description="Transaction height"),
    "timestamp": fields.Integer(required=True,
                                description="Transaction timestamp"),
    "tx_hash": fields.String(required=True, description="Transaction hash")
}
tx_summary_response = api.model("tx_summary_response", tx_summary_model)
