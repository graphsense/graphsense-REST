from flask import abort
from flask_restplus import Namespace, Resource

import gsrest.service.labels_service as labelsDAO
import gsrest.service.general_services as generalDAO
from gsrest.apis.common import label_response, tag_response
from gsrest.util.decorator import token_required
from gsrest.apis.common import category_response

api = Namespace('labels',
                path='/labels',
                description='Operations related to labels')


@api.route("/<label>")
class Label(Resource):
    @token_required
    @api.marshal_with(label_response)
    def get(self, label):
        """
        Returns a JSON with the details of the label
        """
        if not label:
            abort(404, "Label not provided")
        result = labelsDAO.get_label(label)
        if not result:
            abort(404, "Label not found")

        return result


@api.route("/<label>/tags")
class LabelTags(Resource):
    @token_required
    @api.marshal_list_with(tag_response)
    def get(self, label):
        """
        Returns a JSON with the tags of a label
        """
        if not label:
            abort(404, "Label not provided")
        result = labelsDAO.list_tags(label)
        if not result:
            abort(404, "Label not found")
        return result


@api.route("/categories")
class Categories(Resource):
    @token_required
    @api.marshal_list_with(category_response)
    def get(self):
        """
        Returns a JSON with the categories
        """
        return generalDAO.list_categories()


# TODO: add call: from category to list of labels and #addresses
