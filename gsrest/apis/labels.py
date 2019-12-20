from flask_restplus import Namespace, Resource

from gsrest.apis.common import label_response, tag_response, currency_parser, \
    category_response
import gsrest.service.general_service as generalDAO
import gsrest.service.labels_service as labelsDAO
from gsrest.util.checks import check_inputs
from gsrest.util.decorator import token_required

api = Namespace('labels',
                path='/labels',
                description='Operations related to labels')

# TODO: add /labels/ to get al list of all labels


@api.param('label', 'The label of an entity (e.g., Internet Archive)')
@api.route("/<label>")
class Label(Resource):
    @token_required
    @api.marshal_with(label_response)
    def get(self, label):
        """
        Returns details (address count) for a specific label
        """
        check_inputs(label=label)
        result = labelsDAO.get_label(label)
        return result


@api.param('label', 'The label of an entity (e.g., Internet Archive)')
@api.route("/<label>/tags")
class LabelTags(Resource):
    @token_required
    @api.doc(parser=currency_parser)
    @api.marshal_list_with(tag_response)
    def get(self, label):
        """
        Returns the tags associated with a given label
        """
        currency = currency_parser.parse_args()['currency']
        check_inputs(label=label, currency_optional=currency)
        result = labelsDAO.list_tags(label, currency)
        return result


@api.route("/categories")
class Categories(Resource):
    @token_required
    @api.marshal_list_with(category_response)
    def get(self):
        """
        Returns the supported entity categories
        """
        return generalDAO.list_categories()

# TODO: add call: from category to list of labels and #addresses
