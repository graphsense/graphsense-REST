from flask import Response, abort
from flask_restplus import Namespace, Resource

from gsrest.apis.common import neighbors_parser, page_size_parser, \
    search_neighbors_parser, entity_addresses_response, neighbors_response, \
    entity_tags_response, tag_response, search_neighbors_response
from gsrest.service import addresses_service as addressesDAO
from gsrest.service import entities_service as entitiesDAO
from gsrest.util.checks import check_inputs
from gsrest.util.csvify import tags_to_csv, create_download_header, \
    flatten_rows
from gsrest.util.decorator import token_required

api = Namespace('entities',
                path='/<currency>/entities',
                description='Operations related to entities')


@api.route("/<int:entity>")
@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('entity', 'The cryptocurrency entity')
class Entity(Resource):
    @token_required
    @api.marshal_with(entity_tags_response)
    def get(self, currency, entity):
        """
        Returns details and optionally tags of a specific entity
        """
        check_inputs(currency=currency, entity=entity)
        entity_stats = entitiesDAO.get_entity(currency, entity)
        if entity_stats:
            entity_stats['tags'] = entitiesDAO.\
                list_entity_tags(currency, entity_stats['entity'])
            return entity_stats
        abort(404, "Entity {} not found in currency {}".format(entity,
                                                               currency))


@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('entity', 'The cryptocurrency entity')
@api.route("/<int:entity>/tags")
class EntityTags(Resource):
    @token_required
    @api.marshal_list_with(tag_response)
    def get(self, currency, entity):
        """
        Returns attribution tags for a given entity
        """
        check_inputs(currency=currency, entity=entity)
        tags = entitiesDAO.list_entity_tags(currency, entity)
        return tags


@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('entity', 'The cryptocurrency entity')
@api.route("/<int:entity>/tags.csv")
class EntityTagsCSV(Resource):
    @token_required
    def get(self, currency, entity):
        """
        Returns attribution tags for a given entity as CSV
        """
        check_inputs(currency=currency, entity=entity)
        tags = entitiesDAO.list_entity_tags(currency, int(entity))
        return Response(tags_to_csv(tags), mimetype="text/csv",
                        headers=create_download_header('tags of entity {} '
                                                       '({}).csv'
                                                       .format(entity,
                                                               currency
                                                               .upper())))


@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('entity', 'The cryptocurrency entity')
@api.route("/<int:entity>/neighbors")
class EntityNeighbors(Resource):
    @token_required
    @api.doc(parser=neighbors_parser)
    @api.marshal_with(neighbors_response)
    def get(self, currency, entity):
        """
        Returns an entities' neighbors in the entity graph
        """
        args = neighbors_parser.parse_args()
        direction = args.get("direction")
        page = args.get("page")
        pagesize = args.get("pagesize")
        check_inputs(currency=currency, direction=direction, page=page,
                     pagesize=pagesize)
        paging_state = bytes.fromhex(page) if page else None
        if "in" in direction:
            paging_state, relations = entitiesDAO\
                .list_entity_incoming_relations(currency, entity,
                                                paging_state, pagesize)
        else:
            paging_state, relations = entitiesDAO\
                .list_entity_outgoing_relations(currency, entity,
                                                paging_state, pagesize)
        return {"next_page": paging_state.hex() if paging_state else None,
                "neighbors": relations}


@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('entity', 'The cryptocurrency entity')
@api.route("/<int:entity>/neighbors.csv")
class EntityNeighborsCSV(Resource):
    @token_required
    @api.doc(parser=neighbors_parser)
    def get(self, currency, entity):
        """
        Returns an entities' neighbors in the entity graph as CSV
        """
        # TODO: rather slow with 1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s
        args = neighbors_parser.parse_args()
        direction = args.get("direction")
        page = args.get("page")
        pagesize = args.get("pagesize")
        query_function = entitiesDAO.list_entity_outgoing_relations
        if "in" in direction:
            query_function = entitiesDAO.list_entity_incoming_relations
        check_inputs(currency=currency, entity=entity, direction=direction,
                     page=page)
        paging_state = bytes.fromhex(page) if page else None
        columns = []
        data = ''
        while True:
            paging_state, neighbors = query_function(currency, entity,
                                                     paging_state, pagesize)
            if neighbors is not None:
                for row in flatten_rows(neighbors, columns):
                    data += row
                if not paging_state:
                    break
            else:
                abort(404, "Entity {} not found in currency {}"
                      .format(entity, currency))
        return Response(data,
                        mimetype="text/csv",
                        headers=create_download_header(
                            'neighbors of entity {} ({}).csv'
                            .format(entity, currency.upper())))


@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('entity', 'The cryptocurrency entity')
@api.route("/<int:entity>/addresses")
class EntityAddresses(Resource):
    @token_required
    @api.doc(parser=page_size_parser)
    @api.marshal_with(entity_addresses_response)
    def get(self, currency, entity):
        """
        Returns all addresses associated with an entity
        """
        args = page_size_parser.parse_args()
        page = args.get("page")
        pagesize = args.get("pagesize")
        check_inputs(currency=currency, entity=entity, page=page,
                     pagesize=pagesize)
        paging_state = bytes.fromhex(page) if page else None
        paging_state, addresses = entitiesDAO\
            .list_entity_addresses(currency, entity, paging_state, pagesize)
        if addresses:
            return {"next_page": paging_state.hex() if paging_state else None,
                    "addresses": addresses}
        abort(404, "Entity {} not found in currency {}".format(entity,
                                                               currency))


@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('entity', 'The cryptocurrency entity')
@api.route("/<int:entity>/search")
class EntitySearchNeighbors(Resource):
    @token_required
    @api.doc(search_neighbors_parser)
    @api.marshal_with(search_neighbors_response)
    def get(self, currency, entity):
        """
        Searches for specific types of nodes in an entities' neighborhood
        """
        args = search_neighbors_parser.parse_args()
        direction = args['direction']
        depth = args['depth']  # default and int
        breadth = args['breadth']  # default and int
        skipNumAddresses = args['skipNumAddresses']  # default and int
        category = args['category']
        addresses = args['addresses']

        if not [category, addresses].count(None) == 1:
            abort(400, 'Invalid search arguments: one among category and '
                       'addresses must be provided')
        check_inputs(currency=currency, entity=entity, direction=direction,
                     category=category, depth=depth, addresses=addresses)
        if addresses:
            addresses_list = []
            for address in addresses.split(","):
                entity = addressesDAO.get_address_entity_id(currency, address)
                if entity:
                    addresses_list.append({"address": address,
                                           "entity": entity})
                else:
                    abort(404, "Entity of address {} not found in currency {}"
                          .format(address, currency))
            addresses = addresses_list
        if not [category, addresses].count(None) == 1:
            abort(400, 'Invalid search arguments: one among category and '
                       'addresses must be provided')
        # TODO: why do we get non-empty result when category is missing?
        # (removing the if above and with addresses=None)

        outgoing = True
        if "in" in direction:
            outgoing = False

        result = entitiesDAO.\
            list_entity_search_neighbors(currency, entity, category, addresses,
                                         breadth, depth, skipNumAddresses,
                                         dict(), outgoing)

        return {"paths": result}
