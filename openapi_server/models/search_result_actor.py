# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class SearchResultActor(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id: str=None, label: str=None):
        """SearchResultActor - a model defined in OpenAPI

        :param id: The id of this SearchResultActor.
        :param label: The label of this SearchResultActor.
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
    def from_dict(cls, dikt: dict) -> 'SearchResultActor':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The search_result_actor of this SearchResultActor.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The SearchResultActor as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'id': self._id,
            'label': self._label }


    @property
    def id(self):
        """Gets the id of this SearchResultActor.

        id of the actor

        :return: The id of this SearchResultActor.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SearchResultActor.

        id of the actor

        :param id: The id of this SearchResultActor.
        :type id: str
        """

        self._id = id

    @property
    def label(self):
        """Gets the label of this SearchResultActor.

        Label

        :return: The label of this SearchResultActor.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this SearchResultActor.

        Label

        :param label: The label of this SearchResultActor.
        :type label: str
        """

        self._label = label