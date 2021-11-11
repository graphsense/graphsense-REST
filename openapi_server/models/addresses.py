# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.address import Address
from openapi_server import util


class Addresses(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, next_page: str=None, addresses: List[Address]=None):
        """Addresses - a model defined in OpenAPI

        :param next_page: The next_page of this Addresses.
        :param addresses: The addresses of this Addresses.
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
    def from_dict(cls, dikt: dict) -> 'Addresses':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The addresses of this Addresses.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def next_page(self):
        """Gets the next_page of this Addresses.


        :return: The next_page of this Addresses.
        :rtype: str
        """
        return self._next_page

    @next_page.setter
    def next_page(self, next_page):
        """Sets the next_page of this Addresses.


        :param next_page: The next_page of this Addresses.
        :type next_page: str
        """

        self._next_page = next_page

    @property
    def addresses(self):
        """Gets the addresses of this Addresses.


        :return: The addresses of this Addresses.
        :rtype: List[Address]
        """
        return self._addresses

    @addresses.setter
    def addresses(self, addresses):
        """Sets the addresses of this Addresses.


        :param addresses: The addresses of this Addresses.
        :type addresses: List[Address]
        """

        self._addresses = addresses
