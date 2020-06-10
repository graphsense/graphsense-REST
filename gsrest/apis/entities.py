from flask import Response, abort
from flask_restplus import Namespace, Resource

from gsrest.apis.common import neighbors_parser, page_size_parser, \
    search_neighbors_parser, entity_addresses_response, neighbors_response, \
    entity_tags_response, tag_response, search_neighbors_response
from gsrest.service import addresses_service as addressesDAO
from gsrest.service import entities_service as entitiesDAO
from gsrest.util.checks import check_inputs
from gsrest.util.csvify import toCSV, create_download_header
from gsrest.util.decorator import token_required
from gsrest.util.tag_coherence import calcTagCoherence

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
            entity_stats['tag_coherence'] = calcTagCoherence(entity_stats['tags'])
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
        query_function = lambda _: (None, entitiesDAO.list_entity_tags(currency, int(entity)))
        return Response(toCSV(query_function), mimetype="text/csv",
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
        targets = args.get("targets")
        if targets is not None:
            targets = targets.split(',')

        check_inputs(currency=currency, page=page, pagesize=pagesize)
        paging_state = bytes.fromhex(page) if page else None
        paging_state, relations = entitiesDAO\
            .list_entity_relations(currency, entity, "out" in direction, targets,
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
        check_inputs(currency=currency, entity=entity)
        isOutgoing = "out" in direction
        query_function = lambda page_state: entitiesDAO.list_entity_relations(currency, entity, isOutgoing, None, page_state)
        direction = "outgoing" if isOutgoing else "incoming"
        return Response(toCSV(query_function),
                        mimetype="text/csv",
                        headers=create_download_header(
                            '{} neighbors of entity {} ({}).csv'
                            .format(direction, entity, currency.upper())))


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
        field = args['field']
        minValue = args['min']
        maxValue = args['max']
        fieldcurrency = args['fieldcurrency']

        if not [category, addresses, field].count(None) == 2:
            abort(400, 'Invalid search arguments: one among category, '
                       'addresses or field must be provided')

        params = dict()

        if category:
            params['category'] = category

        if field:
            if maxValue is not None and minValue > maxValue:
                abort(400, 'Min must not be greater than max')
            elif field not in ['final_balance', 'total_received']:
                abort(400, 'Field must be "final_balance" or "total_received"')
            elif fieldcurrency not in ['value', 'eur', 'usd']:
                abort(400, 'Fieldcurrency must be one of "value", "eur" or '
                           '"usd"')
            params['field'] = (field, fieldcurrency, minValue, maxValue)

        check_inputs(currency=currency, entity=entity, category=category,
                     depth=depth, addresses=addresses)
        if addresses:
            addresses_list = []
            for address in addresses.split(","):
                e = addressesDAO.get_address_entity_id(currency, address)
                if e:
                    addresses_list.append({"address": address,
                                           "entity": e})
                else:
                    abort(404, "Entity of address {} not found in currency {}"
                          .format(address, currency))
            params['addresses'] = addresses_list

        outgoing = "out" in direction

        result = entitiesDAO.\
            list_entity_search_neighbors(currency, entity, params,
                                         breadth, depth, skipNumAddresses,
                                         outgoing)
        def addTagCoherence(paths):
            if not paths: return
            for path in paths:
                path['node']['tag_coherence'] = calcTagCoherence(path['node']['tags'])
                addTagCoherence(path['paths'])

        addTagCoherence(result)

        return {"paths": result}
