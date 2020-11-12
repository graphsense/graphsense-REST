# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Taxonomy(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, taxonomy=None, uri=None):  # noqa: E501
        """Taxonomy - a model defined in OpenAPI

        :param taxonomy: The taxonomy of this Taxonomy.  # noqa: E501
        :type taxonomy: str
        :param uri: The uri of this Taxonomy.  # noqa: E501
        :type uri: str
        """
        self.openapi_types = {
            'taxonomy': str,
            'uri': str
        }

        self.attribute_map = {
            'taxonomy': 'taxonomy',
            'uri': 'uri'
        }

        if taxonomy is None:
            raise ValueError("Invalid value for `taxonomy`, must not be `None`")  # noqa: E501
        self._taxonomy = taxonomy
        if uri is None:
            raise ValueError("Invalid value for `uri`, must not be `None`")  # noqa: E501
        self._uri = uri

    @classmethod
    def from_dict(cls, dikt) -> 'Taxonomy':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The taxonomy of this Taxonomy.  # noqa: E501
        :rtype: Taxonomy
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The Taxonomy as a dict
        :rtype: dict
        """
        return { 'taxonomy': self._taxonomy,
            'uri': self._uri }


    @property
    def taxonomy(self):
        """Gets the taxonomy of this Taxonomy.

        Taxonomy  # noqa: E501

        :return: The taxonomy of this Taxonomy.
        :rtype: str
        """
        return self._taxonomy

    @taxonomy.setter
    def taxonomy(self, taxonomy):
        """Sets the taxonomy of this Taxonomy.

        Taxonomy  # noqa: E501

        :param taxonomy: The taxonomy of this Taxonomy.
        :type taxonomy: str
        """
        if taxonomy is None:
            raise ValueError("Invalid value for `taxonomy`, must not be `None`")  # noqa: E501

        self._taxonomy = taxonomy

    @property
    def uri(self):
        """Gets the uri of this Taxonomy.

        URI  # noqa: E501

        :return: The uri of this Taxonomy.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this Taxonomy.

        URI  # noqa: E501

        :param uri: The uri of this Taxonomy.
        :type uri: str
        """
        if uri is None:
            raise ValueError("Invalid value for `uri`, must not be `None`")  # noqa: E501

        self._uri = uri