# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.neighbor import Neighbor
from openapi_server import util

from openapi_server.models.neighbor import Neighbor  # noqa: E501

class Neighbors(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, next_page=None, neighbors=None):  # noqa: E501
        """Neighbors - a model defined in OpenAPI

        :param next_page: The next_page of this Neighbors.  # noqa: E501
        :type next_page: str
        :param neighbors: The neighbors of this Neighbors.  # noqa: E501
        :type neighbors: List[Neighbor]
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
    def from_dict(cls, dikt) -> 'Neighbors':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The neighbors of this Neighbors.  # noqa: E501
        :rtype: Neighbors
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The Neighbors as a dict
        :rtype: dict
        """
        return { 'next_page': self._next_page,
            'neighbors': self._neighbors }


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
