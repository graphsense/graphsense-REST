# coding: utf-8
from gsrest.errors import BadUserInputException
from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Concept(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, label: str=None, taxonomy: str=None, uri: str=None, description: str=None, id: str=None):
        """Concept - a model defined in OpenAPI

        :param label: The label of this Concept.
        :param taxonomy: The taxonomy of this Concept.
        :param uri: The uri of this Concept.
        :param description: The description of this Concept.
        :param id: The id of this Concept.
        """
        self.openapi_types = {
            'label': str,
            'taxonomy': str,
            'uri': str,
            'description': str,
            'id': str
        }

        self.attribute_map = {
            'label': 'label',
            'taxonomy': 'taxonomy',
            'uri': 'uri',
            'description': 'description',
            'id': 'id'
        }

        self._label = label
        self._taxonomy = taxonomy
        self._uri = uri
        self._description = description
        self._id = id

    @classmethod
    def from_dict(cls, dikt: dict) -> 'Concept':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The concept of this Concept.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The Concept as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'label': self._label,
            'taxonomy': self._taxonomy,
            'uri': self._uri,
            'description': self._description,
            'id': self._id }


    @property
    def label(self):
        """Gets the label of this Concept.

        Label

        :return: The label of this Concept.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this Concept.

        Label

        :param label: The label of this Concept.
        :type label: str
        """
        if label is None:
            raise BadUserInputException("Invalid value for `label`, must not be `None`")

        self._label = label

    @property
    def taxonomy(self):
        """Gets the taxonomy of this Concept.

        Taxonomy

        :return: The taxonomy of this Concept.
        :rtype: str
        """
        return self._taxonomy

    @taxonomy.setter
    def taxonomy(self, taxonomy):
        """Sets the taxonomy of this Concept.

        Taxonomy

        :param taxonomy: The taxonomy of this Concept.
        :type taxonomy: str
        """
        if taxonomy is None:
            raise BadUserInputException("Invalid value for `taxonomy`, must not be `None`")

        self._taxonomy = taxonomy

    @property
    def uri(self):
        """Gets the uri of this Concept.

        URI

        :return: The uri of this Concept.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this Concept.

        URI

        :param uri: The uri of this Concept.
        :type uri: str
        """
        if uri is None:
            raise BadUserInputException("Invalid value for `uri`, must not be `None`")

        self._uri = uri

    @property
    def description(self):
        """Gets the description of this Concept.

        Description

        :return: The description of this Concept.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Concept.

        Description

        :param description: The description of this Concept.
        :type description: str
        """
        if description is None:
            raise BadUserInputException("Invalid value for `description`, must not be `None`")

        self._description = description

    @property
    def id(self):
        """Gets the id of this Concept.

        ID

        :return: The id of this Concept.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Concept.

        ID

        :param id: The id of this Concept.
        :type id: str
        """
        if id is None:
            raise BadUserInputException("Invalid value for `id`, must not be `None`")

        self._id = id
