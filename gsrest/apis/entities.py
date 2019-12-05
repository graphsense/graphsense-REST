from flask import request, abort, Response
from flask_restplus import Namespace, Resource, fields
from gsrest.util.decorator import token_required
from gsrest.apis.blocks import value_response
from gsrest.apis.txs import tx_summary_response
from gsrest.service import entities_service as entitiesDAO
from gsrest.service.common_service import address_model
from gsrest.util.csvify import tags_to_csv, create_download_header, \
    flatten_rows
from gsrest.apis.common import get_page_parser

api = Namespace('entities',
                path='/<currency>/entities',
                description='Operations related to entities')

tags_parser = api.parser()
tags_parser.add_argument("tags", location="args")

page_size_parser = get_page_parser(api).copy()
page_size_parser.add_argument("pagesize", location="args")

neighbors_parser = get_page_parser(api).copy()
neighbors_parser.add_argument("pagesize", location="args")
neighbors_parser.add_argument("direction", location="args")

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


entity_model = {
    "balance": fields.Nested(value_response, required=True,
                             description="Balance"),
    "entity": fields.Integer(required=True, description="Entity id"),
    "first_tx": fields.Nested(tx_summary_response, required=True),
    "last_tx": fields.Nested(tx_summary_response, required=True),
    "no_addresses": fields.Integer(required=True,
                                   description="Number of addresses"),
    "in_degree": fields.Integer(required=True, description="In-degree value"),
    "out_degree": fields.Integer(required=True,
                                 description="Out-degree value"),
    "no_incoming_txs": fields.Integer(required=True,
                                      description="Incoming transactions"),
    "no_outgoing_txs": fields.Integer(required=True,
                                      description="Outgoing transactions"),
    "total_received": fields.Nested(value_response, required=True),
    "total_spent": fields.Nested(value_response, required=True),
}
entity_response = api.model("entity_response", entity_model)

entity_tags_model = entity_model
entity_tags_model["tags"] = fields.List(fields.Nested(tag_response,
                                                      required=True))
entity_tags_response = api.model("entity_tags_response", entity_tags_model)

neighbor_model = {
    "id": fields.String(required=True, description="Node Id"),
    "node_type": fields.String(required=True, description="Node type"),
    "balance": fields.Nested(value_response, required=True,
                             description="Balance"),
    "received": fields.Nested(value_response, required=True,
                              description="Received amount"),
    "no_txs": fields.Integer(required=True,
                             description="Number of transactions"),
    "estimated_value": fields.Nested(value_response, required=True)
}
neighbor_response = api.model("neighbor_response", neighbor_model)

neighbors_model = {
    "next_page": fields.String(required=True, description="The next page"),
    "neighbors": fields.List(fields.Nested(neighbor_response), required=True,
                             description="The list of neighbors")
}
neighbors_response = api.model("neighbors_response", neighbors_model)

entity_address_model = address_model.copy()
entity_address_model['entity'] = fields.Integer(required=True,
                                                description="Entity id")

entity_address_response = api.model("entity_address_response",
                                    entity_address_model)

entity_addresses_model = {
    "next_page": fields.String(required=True, description="The next page"),
    "addresses": fields.List(fields.Nested(entity_address_response),
                             required=True,
                             description="The list of entity adresses")
}
entity_addresses_response = api.model("entity_addresses_response",
                                      entity_addresses_model)


@api.route("/<int:entity>")
@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('entity', 'The cryptocurrency entity')
class Entity(Resource):
    @token_required
    @api.marshal_with(entity_tags_response)
    def get(self, currency, entity):
        """
        Returns details and tags of a specific entity
        """
        entity_stats = entitiesDAO.get_entity(currency, int(entity))
        if not entity_stats:
            abort(404, "Entity {} not found in currency {}"
                  .format(entity_stats, currency))
        entity_stats['tags'] = entitiesDAO.\
            list_entity_tags(currency, entity_stats['entity'])
        return entity_stats


@api.route("/<int:entity>/tags")
class EntityTags(Resource):
    @token_required
    @api.marshal_list_with(tag_response)
    def get(self, currency, entity):
        """
        Returns tags of a specific entity.
        """

        tags = entitiesDAO.list_entity_tags(currency, entity)
        return tags


@api.route("/<int:entity>/tags.csv")
class EntityTagsCSV(Resource):
    @token_required
    def get(self, currency, entity):
        """ Returns a JSON with the tags of the entity """
        tags = entitiesDAO.list_entity_tags(currency, int(entity))
        return Response(tags_to_csv(tags), mimetype="text/csv",
                        headers=create_download_header('tags of entity {} '
                                                       '({}).csv'
                                                       .format(entity,
                                                               currency
                                                               .upper())))


@api.route("/<int:entity>/neighbors")
class EntityNeighbors(Resource):
    @token_required
    @api.doc(parser=neighbors_parser)
    @api.marshal_with(neighbors_response)
    def get(self, currency, entity):
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
            paging_state, relations = entitiesDAO\
                .list_entity_outgoing_relations(currency, entity,
                                                paging_state, pagesize)
        else:
            paging_state, relations = entitiesDAO\
                .list_entity_incoming_relations(currency, entity,
                                                paging_state, pagesize)
        return {"next_page": paging_state.hex() if paging_state else None,
                "neighbors": relations}


@api.route("/<int:entity>/neighbors.csv")
class EntityNeighborsCSV(Resource):
    @token_required
    @api.doc(parser=neighbors_parser)
    def get(self, currency, entity):
        """
        Returns a JSON with edges and nodes of the entity
        """
        direction = request.args.get("direction")
        page = request.args.get("page")
        pagesize = request.args.get("pagesize")
        paging_state = bytes.fromhex(page) if page else None
        if not direction:
            abort(404, "Direction value missing")
        if "in" in direction:
            query_function = entitiesDAO.list_entity_incoming_relations
        elif "out" in direction:
            query_function = entitiesDAO.list_entity_outgoing_relations
        else:
            abort(404, "Invalid direction value - has to be either in or out")

        if pagesize is not None:
            try:
                pagesize = int(pagesize)
            except Exception:
                abort(404, "Invalid pagesize value")

        columns = []
        data = ''
        while True:
            paging_state, neighbors = query_function(currency, entity,
                                                     paging_state, pagesize)
            for row in flatten_rows(neighbors, columns):
                data += row
            if not paging_state:
                break
        return Response(data,
                        mimetype="text/csv",
                        headers=create_download_header(
                            'neighbors of entity {} ({}).csv'
                            .format(entity, currency.upper())))


@api.route("/<int:entity>/addresses")
class EntityAddresses(Resource):
    @token_required
    @api.doc(parser=page_size_parser)
    @api.marshal_with(entity_addresses_response)
    def get(self, currency, entity):
        """
        Returns a JSON with the details of the addresses in the entity
        """
        if not entity:
            abort(404, "Entity not provided")
        page = request.args.get("page")
        pagesize = request.args.get("pagesize")
        if pagesize is not None:
            try:
                pagesize = int(pagesize)
            except Exception:
                abort(404, "Invalid pagesize value")

        paging_state = bytes.fromhex(page) if page else None

        paging_state, addresses = entitiesDAO\
            .list_entity_addresses(currency, entity, paging_state, pagesize)
        return {"next_page": paging_state.hex() if paging_state else None,
                "addresses": addresses}
