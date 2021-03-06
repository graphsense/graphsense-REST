# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.address import Address
from openapi_server import util

from openapi_server.models.address import Address  # noqa: E501

class EntityAddresses(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, next_page=None, addresses=None):  # noqa: E501
        """EntityAddresses - a model defined in OpenAPI

        :param next_page: The next_page of this EntityAddresses.  # noqa: E501
        :type next_page: str
        :param addresses: The addresses of this EntityAddresses.  # noqa: E501
        :type addresses: List[Address]
        """
        self.openapi_types = {
            'next_page': str,
            'addresses': List[Address]
        }

        self.attribute_map = {
            'next_page': 'next_page',
            'addresses': 'addresses'
        }

        self._next_page = next_page
        self._addresses = addresses

    @classmethod
    def from_dict(cls, dikt) -> 'EntityAddresses':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The entity_addresses of this EntityAddresses.  # noqa: E501
        :rtype: EntityAddresses
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The EntityAddresses as a dict
        :rtype: dict
        """
        return { 'next_page': self._next_page,
            'addresses': self._addresses }


    @property
    def next_page(self):
        """Gets the next_page of this EntityAddresses.


        :return: The next_page of this EntityAddresses.
        :rtype: str
        """
        return self._next_page

    @next_page.setter
    def next_page(self, next_page):
        """Sets the next_page of this EntityAddresses.


        :param next_page: The next_page of this EntityAddresses.
        :type next_page: str
        """

        self._next_page = next_page

    @property
    def addresses(self):
        """Gets the addresses of this EntityAddresses.


        :return: The addresses of this EntityAddresses.
        :rtype: List[Address]
        """
        return self._addresses

    @addresses.setter
    def addresses(self, addresses):
        """Sets the addresses of this EntityAddresses.


        :param addresses: The addresses of this EntityAddresses.
        :type addresses: List[Address]
        """

        self._addresses = addresses
