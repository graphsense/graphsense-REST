# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Taxonomy(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, taxonomy: str=None, uri: str=None):
        """Taxonomy - a model defined in OpenAPI

        :param taxonomy: The taxonomy of this Taxonomy.
        :param uri: The uri of this Taxonomy.
        """
        self.openapi_types = {
            'taxonomy': str,
            'uri': str
        }

        self.attribute_map = {
            'taxonomy': 'taxonomy',
            'uri': 'uri'
        }

        self._taxonomy = taxonomy
        self._uri = uri

    @classmethod
    def from_dict(cls, dikt: dict) -> 'Taxonomy':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The taxonomy of this Taxonomy.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The Taxonomy as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'taxonomy': self._taxonomy,
            'uri': self._uri }


    @property
    def taxonomy(self):
        """Gets the taxonomy of this Taxonomy.

        Taxonomy

        :return: The taxonomy of this Taxonomy.
        :rtype: str
        """
        return self._taxonomy

    @taxonomy.setter
    def taxonomy(self, taxonomy):
        """Sets the taxonomy of this Taxonomy.

        Taxonomy

        :param taxonomy: The taxonomy of this Taxonomy.
        :type taxonomy: str
        """
        if taxonomy is None:
            raise ValueError("Invalid value for `taxonomy`, must not be `None`")

        self._taxonomy = taxonomy

    @property
    def uri(self):
        """Gets the uri of this Taxonomy.

        URI

        :return: The uri of this Taxonomy.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this Taxonomy.

        URI

        :param uri: The uri of this Taxonomy.
        :type uri: str
        """
        if uri is None:
            raise ValueError("Invalid value for `uri`, must not be `None`")

        self._uri = uri
