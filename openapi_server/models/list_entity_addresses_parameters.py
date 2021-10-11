# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class ListEntityAddressesParameters(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, entity=None):  # noqa: E501
        """ListEntityAddressesParameters - a model defined in OpenAPI

        :param entity: The entity of this ListEntityAddressesParameters.  # noqa: E501
        :type entity: int
        """
        self.openapi_types = {
            'entity': int
        }

        self.attribute_map = {
            'entity': 'entity'
        }

        #if entity is None:
            #raise ValueError("Invalid value for `entity`, must not be `None`")  # noqa: E501
        self._entity = entity

    @classmethod
    def from_dict(cls, dikt) -> 'ListEntityAddressesParameters':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The list_entity_addresses_parameters of this ListEntityAddressesParameters.  # noqa: E501
        :rtype: ListEntityAddressesParameters
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The ListEntityAddressesParameters as a dict
        :rtype: dict
        """
        return { 'entity': self._entity }


    @property
    def entity(self):
        """Gets the entity of this ListEntityAddressesParameters.

        Entity id  # noqa: E501

        :return: The entity of this ListEntityAddressesParameters.
        :rtype: int
        """
        return self._entity

    @entity.setter
    def entity(self, entity):
        """Sets the entity of this ListEntityAddressesParameters.

        Entity id  # noqa: E501

        :param entity: The entity of this ListEntityAddressesParameters.
        :type entity: int
        """
        if entity is None:
            raise ValueError("Invalid value for `entity`, must not be `None`")  # noqa: E501

        self._entity = entity
