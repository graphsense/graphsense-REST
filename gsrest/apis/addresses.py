from flask import request, abort, Response
from flask_restplus import Namespace, Resource, fields
from functools import wraps

from gsrest.util.decorator import token_required
from gsrest.apis.blocks import value_response
from gsrest.apis.txs import tx_summary_response
from gsrest.util.csvify import tags_to_csv, create_download_header
import gsrest.service.addresses_service as addressesDAO

api = Namespace('addresses',
                path='/<currency>/addresses',
                description='Operations related to addresses')

tags_parser = api.parser()
tags_parser.add_argument("tags", location="args")

direction_parser = api.parser()
direction_parser.add_argument("direction", location="args")

page_parser = api.parser()
page_parser.add_argument("page", default=0, location="args")

neighbors_parser = page_parser.copy()
neighbors_parser.add_argument("direction", location="args")
neighbors_parser.add_argument("pagesize", location="args")


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
address_response = api.model("address_response", address_model)

address_tx_model = {
    "address": fields.String(required=True, description="Address"),
    "height": fields.Integer(required=True, description="Transaction height"),
    "timestamp": fields.Integer(required=True,
                                description="Transaction timestamp"),
    "tx_hash": fields.String(required=True, description="Transaction hash"),
    "value": fields.Nested(value_response, required=True)
}
address_tx_response = api.model("address_tx_response", address_tx_model)

address_txs_model = {
    "next_page": fields.String(required=True, description="The next page"),
    "address_txs": fields.List(fields.Nested(address_tx_response),
                               required=True,
                               description="The list of transactions")
}
address_txs_response = api.model("address_txs_response", address_txs_model)

tag_model = {
    "label": fields.String(required=True, description="Label"),
    "address": fields.String(required=True, description="Address"),
    "source": fields.String(required=True, description="Source"),
    "tagpack_uri": fields.String(required=True, description="Tagpack URI"),
    "currency": fields.String(required=True, description="Currency"),
    "lastmod": fields.Integer(required=True, description="Last modified"),
    "category": fields.String(required=False, description="Category"),
    "abuse": fields.String(required=False, description="Abuse")
}
tag_response = api.model("tag_response", tag_model)

address_tags_model = address_model
address_tags_model["tags"] = fields.List(fields.Nested(tag_response,
                                                       required=True))
address_tags_response = api.model("address_tags_response",
                                  address_tags_model)

neighbor_model = {
    "id": fields.String(required=True, description="Node Id"),
    "node_type": fields.String(required=True, description="Node type"),
    "balance": fields.Nested(value_response, required=True, description="Balance"),
    "received": fields.Nested(value_response, required=True, description="Received amount"),
    "no_txs": fields.Integer(required=True, description="Number of transactions"),
    "estimated_value": fields.Nested(value_response, required=True)
}
neighbor_response = api.model("neighbor_response", neighbor_model)

neighbors_model = {
    "next_page": fields.String(required=True, description="The next page"),
    "neighbors": fields.List(fields.Nested(neighbor_response), required=True,
                             description="The list of neighbors")
}
neighbors_response = api.model("neighbors_response", neighbors_model)


def selective_marshal_with(address_response, address_tags_response):
    """ Selective response marshalling """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.args.get("tags"):
                model = address_tags_response
            else:
                model = address_response
            func2 = api.marshal_with(model)(func)
            return func2(*args, **kwargs)
        return wrapper
    return decorator


@api.route("/<address>")
class Address(Resource):
    @token_required
    @api.doc(parser=tags_parser)
    @selective_marshal_with(address_response, address_tags_response)
    def get(self, currency, address):
        """ Returns details of a specific address """
        addr = addressesDAO.get_address(currency, address)
        if not addr:
            abort(404, "Address {} not found in currency {}"
                  .format(address, currency))
        if request.args.get("tags"):
            addr['tags'] = addressesDAO.list_address_tags(currency, address)
        return addr


@api.route("/<address>/txs")
class AddressTxs(Resource):
    @token_required
    @api.doc(parser=page_parser)
    @api.marshal_with(address_txs_response)
    def get(self, currency, address):
        """
        Returns transactions of a specific address.
        """
        # TODO: should we allow the user to specify the page size?
        page = request.args.get("page")
        paging_state = bytes.fromhex(page) if page else None
        paging_state, address_txs = addressesDAO.list_address_txs(currency,
                                                                  address,
                                                                  paging_state)
        if not address_txs:
            abort(404, "Address {} not found in currency {}"
                  .format(address, currency))

        return {"next_page": paging_state.hex() if paging_state else None,
                "address_txs": address_txs}


@api.route("/<address>/tags")
class AddressTags(Resource):
    @token_required
    @api.marshal_list_with(tag_response)
    def get(self, currency, address):
        """
        Returns tags of a specific address.
        """

        address_tags = addressesDAO.list_address_tags(currency, address)
        if not address_tags:
            abort(404, "Address {} not found in currency {}"
                  .format(address, currency))

        return address_tags


@api.route("/<address>/tags.csv")
class AddressTagsCSV(Resource):
    @token_required
    def get(self, currency, address):
        """ Returns a JSON with the tags of the address """
        tags = addressesDAO.list_address_tags(currency, address)
        return Response(tags_to_csv(tags), mimetype="text/csv",
                        headers=create_download_header('tags of address {} '
                                                       '({}).csv'
                                                       .format(address,
                                                               currency
                                                               .upper())))


@api.route("/<address>/neighbors")
class AddressNeighbors(Resource):
    @token_required
    @api.doc(parser=neighbors_parser)
    @api.marshal_with(neighbors_response)
    def get(self, currency, address):
        """
        Returns a JSON with edges and nodes of the address
        """
        direction = request.args.get("direction")
        if not direction:
            abort(404, "Direction value missing")
        if "in" in direction:
            is_outgoing = False
        elif "out" in direction:
            is_outgoing = True
        else:
            abort(404, "Invalid direction value - has to be either in or out")

        page = request.args.get("page")
        pagesize = request.args.get("pagesize")
        paging_state = bytes.fromhex(page) if page else None

        if pagesize is not None:
            try:
                pagesize = int(pagesize)
            except Exception:
                abort(404, "Invalid pagesize value")

        if is_outgoing:
            paging_state, relations = addressesDAO.\
                list_address_outgoing_relations(currency, address,
                                                paging_state, pagesize)
        # else:
        #     paging_state, relations = addressesDAO.list_address_incoming_relations(
        #         currency, paging_state, address, pagesize)
        return {"next_page": paging_state.hex() if paging_state else None,
                "neighbors": relations}

# TODO: AddressIncomingRelations, AddressOutgoingRelations, AddressSummary
