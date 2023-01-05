# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.neighbor_address import NeighborAddress
from openapi_server import util


class NeighborAddresses(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, next_page: str=None, neighbors: List[NeighborAddress]=None):
        """NeighborAddresses - a model defined in OpenAPI

        :param next_page: The next_page of this NeighborAddresses.
        :param neighbors: The neighbors of this NeighborAddresses.
        """
        self.openapi_types = {
            'next_page': str,
            'neighbors': List[NeighborAddress]
        }

        self.attribute_map = {
            'next_page': 'next_page',
            'neighbors': 'neighbors'
        }

        self._next_page = next_page
        self._neighbors = neighbors

    @classmethod
    def from_dict(cls, dikt: dict) -> 'NeighborAddresses':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The neighbor_addresses of this NeighborAddresses.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The NeighborAddresses as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'next_page': self._next_page,
            'neighbors': self._neighbors }


    @property
    def next_page(self):
        """Gets the next_page of this NeighborAddresses.


        :return: The next_page of this NeighborAddresses.
        :rtype: str
        """
        return self._next_page

    @next_page.setter
    def next_page(self, next_page):
        """Sets the next_page of this NeighborAddresses.


        :param next_page: The next_page of this NeighborAddresses.
        :type next_page: str
        """

        self._next_page = next_page

    @property
    def neighbors(self):
        """Gets the neighbors of this NeighborAddresses.


        :return: The neighbors of this NeighborAddresses.
        :rtype: List[NeighborAddress]
        """
        return self._neighbors

    @neighbors.setter
    def neighbors(self, neighbors):
        """Sets the neighbors of this NeighborAddresses.


        :param neighbors: The neighbors of this NeighborAddresses.
        :type neighbors: List[NeighborAddress]
        """
        if neighbors is None:
            raise ValueError("Invalid value for `neighbors`, must not be `None`")

        self._neighbors = neighbors
