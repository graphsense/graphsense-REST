# coding: utf-8
from gsrest.errors import BadUserInputException
from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class LabeledItemRef(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id: str=None, label: str=None):
        """LabeledItemRef - a model defined in OpenAPI

        :param id: The id of this LabeledItemRef.
        :param label: The label of this LabeledItemRef.
        """
        self.openapi_types = {
            'id': str,
            'label': str
        }

        self.attribute_map = {
            'id': 'id',
            'label': 'label'
        }

        self._id = id
        self._label = label

    @classmethod
    def from_dict(cls, dikt: dict) -> 'LabeledItemRef':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The labeled_item_ref of this LabeledItemRef.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The LabeledItemRef as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'id': self._id,
            'label': self._label }


    @property
    def id(self):
        """Gets the id of this LabeledItemRef.

        identifier of the item

        :return: The id of this LabeledItemRef.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this LabeledItemRef.

        identifier of the item

        :param id: The id of this LabeledItemRef.
        :type id: str
        """
        if id is None:
            raise BadUserInputException("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def label(self):
        """Gets the label of this LabeledItemRef.

        Label

        :return: The label of this LabeledItemRef.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this LabeledItemRef.

        Label

        :param label: The label of this LabeledItemRef.
        :type label: str
        """
        if label is None:
            raise BadUserInputException("Invalid value for `label`, must not be `None`")

        self._label = label
