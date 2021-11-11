# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.neighbor import Neighbor
from openapi_server import util


class Neighbors(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, next_page: str=None, neighbors: List[Neighbor]=None):
        """Neighbors - a model defined in OpenAPI

        :param next_page: The next_page of this Neighbors.
        :param neighbors: The neighbors of this Neighbors.
        """
        self.openapi_types = {
            'next_page': str,
            'neighbors': List[Neighbor]
        }

        self.attribute_map = {
            'next_page': 'next_page',
            'neighbors': 'neighbors'
        }

        self._next_page = next_page
        self._neighbors = neighbors

    @classmethod
    def from_dict(cls, dikt: dict) -> 'Neighbors':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The neighbors of this Neighbors.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def next_page(self):
        """Gets the next_page of this Neighbors.


        :return: The next_page of this Neighbors.
        :rtype: str
        """
        return self._next_page

    @next_page.setter
    def next_page(self, next_page):
        """Sets the next_page of this Neighbors.


        :param next_page: The next_page of this Neighbors.
        :type next_page: str
        """

        self._next_page = next_page

    @property
    def neighbors(self):
        """Gets the neighbors of this Neighbors.


        :return: The neighbors of this Neighbors.
        :rtype: List[Neighbor]
        """
        return self._neighbors

    @neighbors.setter
    def neighbors(self, neighbors):
        """Sets the neighbors of this Neighbors.


        :param neighbors: The neighbors of this Neighbors.
        :type neighbors: List[Neighbor]
        """

        self._neighbors = neighbors
