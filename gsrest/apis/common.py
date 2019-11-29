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
value_response = api.model("value_response", value_model)


tx_summary_model = {
    "height": fields.Integer(required=True, description="Transaction height"),
    "timestamp": fields.Integer(required=True,
                                description="Transaction timestamp"),
    "tx_hash": fields.String(required=True, description="Transaction hash")
}
tx_summary_response = api.model("tx_summary_response", tx_summary_model)
