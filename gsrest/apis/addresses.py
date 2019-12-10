from flask import request, abort, Response
from flask_restplus import Namespace, Resource
from functools import wraps

from gsrest.apis.common import page_parser, tags_parser, neighbors_parser, \
    entity_response, address_txs_response, address_response, \
    address_tags_response, entity_tags_response, tag_response, \
    neighbors_response
import gsrest.service.addresses_service as addressesDAO
import gsrest.service.entities_service as entitiesDAO
import gsrest.service.common_service as commondDAO
from gsrest.util.decorator import token_required
from gsrest.util.csvify import tags_to_csv, create_download_header, \
    flatten_rows


api = Namespace('addresses',
                path='/<currency>/addresses',
                description='Operations related to addresses')


def selective_marshal_with(default_response, args_response, arg):
    """ Selective response marshalling """
    # args_response is selected if arg is in request.args
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if arg in request.args:
                model = args_response
            else:
                model = default_response
            func2 = api.marshal_with(model)(func)
            return func2(*args, **kwargs)
        return wrapper
    return decorator


@api.route("/<address>")
@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('address', 'The cryptocurrency address')
class Address(Resource):
    @token_required
    @api.doc(parser=tags_parser)
    @selective_marshal_with(address_response, address_tags_response, 'tags')
    def get(self, currency, address):
        """
        Returns details of a specific address
        """
        args = tags_parser.parse_args()
        addr = commondDAO.get_address(currency, address)
        if not addr:
            abort(404, "Address {} not found in currency {}"
                  .format(address, currency))
        if 'tags' in args:  # TODO: wait for dashboard's API specifications
            addr['tags'] = commondDAO.list_address_tags(currency, address)
        return addr


@api.param('currency', 'The cryptocurrency (e.g., btc)')
@api.param('address', 'The cryptocurrency address')
@api.route("/<address>/txs")
class AddressTxs(Resource):
    @token_required
    @api.doc(parser=page_parser)
    @api.marshal_with(address_txs_response)
    def get(self, currency, address):
        """
        Returns all transactions an address has been involved in
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

        address_tags = commondDAO.list_address_tags(currency, address)
        return address_tags


@api.route("/<address>/tags.csv")
class AddressTagsCSV(Resource):
    @token_required
    def get(self, currency, address):
        """ Returns a JSON with the tags of the address """
        tags = commondDAO.list_address_tags(currency, address)
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
        args = neighbors_parser.parse_args()
        direction = args.get("direction")
        if not direction:
            abort(400, "Direction value missing")
        if "in" in direction:
            is_outgoing = False
        elif "out" in direction:
            is_outgoing = True
        else:
            abort(400, "Invalid direction value - has to be either in or out")

        page = args.get("page")
        pagesize = args.get("pagesize")
        paging_state = bytes.fromhex(page) if page else None

        if pagesize is not None:
            try:
                pagesize = int(pagesize)
            except Exception:
                abort(400, "Invalid pagesize value")

        if is_outgoing:
            paging_state, relations = addressesDAO\
                .list_address_outgoing_relations(currency, address,
                                                 paging_state, pagesize)
        else:
            paging_state, relations = addressesDAO\
                .list_address_incoming_relations(currency, address,
                                                 paging_state, pagesize)
        return {"next_page": paging_state.hex() if paging_state else None,
                "neighbors": relations}


@api.route("/<address>/neighbors.csv")
class AddressNeighborsCSV(Resource):
    @token_required
    @api.doc(parser=neighbors_parser)
    def get(self, currency, address):
        """
        Returns a JSON with edges and nodes of the address
        """
        args = neighbors_parser.parse_args()
        direction = args.get("direction")
        page = args.get("page")
        pagesize = args.get("pagesize")
        paging_state = bytes.fromhex(page) if page else None
        if not direction:
            abort(400, "Direction value missing")
        if "in" in direction:
            query_function = addressesDAO.list_address_incoming_relations
        elif "out" in direction:
            query_function = addressesDAO.list_address_outgoing_relations
        else:
            abort(400, "Invalid direction value - has to be either in or out")

        if pagesize is not None:
            try:
                pagesize = int(pagesize)
            except Exception:
                abort(400, "Invalid pagesize value")

        columns = []
        data = ''
        while True:
            paging_state, neighbors = query_function(currency, address,
                                                     paging_state, pagesize)
            for row in flatten_rows(neighbors, columns):
                data += row
            if not paging_state:
                break
        return Response(data,
                        mimetype="text/csv",
                        headers=create_download_header(
                            'neighbors of address {} ({}).csv'
                            .format(address, currency.upper())))


@api.route("/<address>/entity")
class AddressEntity(Resource):
    @token_required
    @selective_marshal_with(entity_response, entity_tags_response, 'tags')
    def get(self, currency, address):
        """
        Returns a JSON with the details of the entity
        """
        if not address:
            abort(400, "Address not provided")

        entity = addressesDAO.get_address_entity(currency, address)

        if not entity:
            abort(404, "Address not found")

        if 'tags' in request.args:
            entity['tags'] = entitiesDAO.list_entity_tags(currency,
                                                          entity['entity'])

        return entity
