from flask_restplus import Namespace, Resource
from flask import abort, current_app

from gsrest.apis.common import tag_response, label_parser, \
    concept_response, taxonomy_response
import gsrest.service.general_service as generalDAO
import gsrest.service.tags_service as labelsDAO
from gsrest.util.checks import check_inputs
from gsrest.util.decorator import token_required

api = Namespace('tags',
                path='/tags',
                description='Operations related to tags')


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
@api.route("/taxonomies")
class Taxonomies(Resource):
    @token_required
    @api.marshal_list_with(taxonomy_response)
    def get(self):
        """
        Returns the supported taxonomies
        """
        return generalDAO.list_taxonomies()


@api.param('taxonomy', 'The taxonomy (e.g., entity, abuse)')
@api.route("/taxonomies/<taxonomy>/concepts")
class TaxonomiesConcepts(Resource):
    @token_required
    @api.marshal_list_with(concept_response)
    def get(self, taxonomy):
        """
        Returns the supported concepts
        """
        return generalDAO.list_concepts(taxonomy)

# TODO: add call: from category to list of labels and #addresses
