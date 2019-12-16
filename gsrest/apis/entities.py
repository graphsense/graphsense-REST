from flask import Response
from flask_restplus import Namespace, Resource

from gsrest.util.decorator import token_required
from gsrest.service import entities_service as entitiesDAO
from gsrest.service import addresses_service as addressesDAO
from gsrest.util.checks import check_inputs
from gsrest.util.csvify import tags_to_csv, create_download_header, \
    flatten_rows
from gsrest.apis.common import neighbors_parser, page_size_parser, \
    search_neighbors_parser, entity_addresses_response, neighbors_response, \
    entity_tags_response, tag_response, search_neighbors_response

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
        Returns details and tags of a specific entity
        """
        check_inputs(currency=currency, entity=entity)
        entity_stats = entitiesDAO.get_entity(currency, entity)
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
        check_inputs(currency=currency, entity=entity)
        tags = entitiesDAO.list_entity_tags(currency, entity)
        return tags


@api.route("/<int:entity>/tags.csv")
class EntityTagsCSV(Resource):
    @token_required
    def get(self, currency, entity):
        """ Returns a JSON with the tags of the entity """
        check_inputs(currency=currency, entity=entity)
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


@api.route("/<int:entity>/neighbors.csv")
class EntityNeighborsCSV(Resource):
    @token_required
    @api.doc(parser=neighbors_parser)
    def get(self, currency, entity):
        """
        Returns a JSON with edges and nodes of the entity
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
        args = page_size_parser.parse_args()
        page = args.get("page")
        pagesize = args.get("pagesize")
        check_inputs(currency=currency, entity=entity, page=page,
                     pagesize=pagesize)
        paging_state = bytes.fromhex(page) if page else None
        paging_state, addresses = entitiesDAO\
            .list_entity_addresses(currency, entity, paging_state, pagesize)
        return {"next_page": paging_state.hex() if paging_state else None,
                "addresses": addresses}


@api.route("/<int:entity>/search")
class EntitySearchNeighbors(Resource):
    @token_required
    @api.doc(search_neighbors_parser)
    @api.marshal_with(search_neighbors_response)
    def get(self, currency, entity):
        args = search_neighbors_parser.parse_args()
        direction = args['direction']
        depth = args['depth']  # default and int
        breadth = args['breadth']  # default and int
        skipNumAddresses = args['skipNumAddresses']  # default and int
        check_inputs(currency=currency, entity=entity, direction=direction,
                     category=args['category'], depth=depth)
        category = args['category']
        ids = []
        if 'addresses' in args:
            ids = args['addresses']
        if ids:
            ids = [{"address": address,
                    "entity": addressesDAO.get_address_entity_id(currency,
                                                                 address)}
                   for address in ids.split(",")]

        outgoing = True
        if "in" in direction:
            outgoing = False

        result = entitiesDAO.\
            list_entity_search_neighbors(currency, entity, category, ids,
                                         breadth, depth, skipNumAddresses,
                                         dict(), outgoing)

        return {"paths": result}
