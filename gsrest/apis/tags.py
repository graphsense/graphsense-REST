from flask_restplus import Namespace, Resource
from flask import abort, current_app

from gsrest.apis.common import label_response, tag_response, label_parser, \
    concept_response
import gsrest.service.general_service as generalDAO
import gsrest.service.tags_service as labelsDAO
from gsrest.util.checks import check_inputs
from gsrest.util.decorator import token_required

api = Namespace('tags',
                path='/tags',
                description='Operations related to tags')


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
        result = None
        address_count = 0
        currency_result = dict()
        for currency in current_app.config['MAPPING']:
            if currency != "tagpacks":
                currency_result[currency] = labelsDAO.get_label(label,
                                                                currency)
                if currency_result[currency] and \
                        'address_count' in currency_result[currency]:
                    result = currency_result[currency]
                    address_count += result['address_count']
        if address_count:
            result['address_count'] = address_count
            return result
        abort(404, "Label not found")


@api.route("")
class LabelTags(Resource):
    @token_required
    @api.doc(parser=label_parser)
    @api.marshal_list_with(tag_response)
    def get(self):
        """
        Returns the tags associated with a given label
        """
        currency = label_parser.parse_args()['currency']
        label = label_parser.parse_args()['label']
        check_inputs(label=label, currency_optional=currency)
        if currency:
            result = labelsDAO.list_tags(label, currency)
        else:
            result = []
            for currency in current_app.config['MAPPING']:
                if currency != "tagpacks":
                    tags = labelsDAO.list_tags(label, currency)
                    if tags:
                        result += tags
        if result:
            return result
        abort(404, "Label not found")


@api.param('taxonomy', 'The taxonomy (e.g., entity, abuse)')
@api.route("/taxonomies/<taxonomy>")
class Taxonomies(Resource):
    @token_required
    @api.marshal_list_with(concept_response)
    def get(self, taxonomy):
        """
        Returns the supported concepts
        """
        return generalDAO.list_concepts(taxonomy)

# TODO: add call: from category to list of labels and #addresses
