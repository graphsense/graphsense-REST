# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.address import Address
from openapi_server.models.neighbor_entity import NeighborEntity
from openapi_server.models.search_result_level5 import SearchResultLevel5
from openapi_server import util


class SearchResultLevel4(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, neighbor: NeighborEntity=None, matching_addresses: List[Address]=None, paths: List[SearchResultLevel5]=None):
        """SearchResultLevel4 - a model defined in OpenAPI

        :param neighbor: The neighbor of this SearchResultLevel4.
        :param matching_addresses: The matching_addresses of this SearchResultLevel4.
        :param paths: The paths of this SearchResultLevel4.
        """
        self.openapi_types = {
            'neighbor': NeighborEntity,
            'matching_addresses': List[Address],
            'paths': List[SearchResultLevel5]
        }

        self.attribute_map = {
            'neighbor': 'neighbor',
            'matching_addresses': 'matching_addresses',
            'paths': 'paths'
        }

        self._neighbor = neighbor
        self._matching_addresses = matching_addresses
        self._paths = paths

    @classmethod
    def from_dict(cls, dikt: dict) -> 'SearchResultLevel4':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The search_result_level4 of this SearchResultLevel4.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The SearchResultLevel4 as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'neighbor': self._neighbor,
            'matching_addresses': self._matching_addresses,
            'paths': self._paths }


    @property
    def neighbor(self):
        """Gets the neighbor of this SearchResultLevel4.


        :return: The neighbor of this SearchResultLevel4.
        :rtype: NeighborEntity
        """
        return self._neighbor

    @neighbor.setter
    def neighbor(self, neighbor):
        """Sets the neighbor of this SearchResultLevel4.


        :param neighbor: The neighbor of this SearchResultLevel4.
        :type neighbor: NeighborEntity
        """
        if neighbor is None:
            raise ValueError("Invalid value for `neighbor`, must not be `None`")

        self._neighbor = neighbor

    @property
    def matching_addresses(self):
        """Gets the matching_addresses of this SearchResultLevel4.


        :return: The matching_addresses of this SearchResultLevel4.
        :rtype: List[Address]
        """
        return self._matching_addresses

    @matching_addresses.setter
    def matching_addresses(self, matching_addresses):
        """Sets the matching_addresses of this SearchResultLevel4.


        :param matching_addresses: The matching_addresses of this SearchResultLevel4.
        :type matching_addresses: List[Address]
        """
        if matching_addresses is None:
            raise ValueError("Invalid value for `matching_addresses`, must not be `None`")

        self._matching_addresses = matching_addresses

    @property
    def paths(self):
        """Gets the paths of this SearchResultLevel4.

        Branches to matching entities

        :return: The paths of this SearchResultLevel4.
        :rtype: List[SearchResultLevel5]
        """
        return self._paths

    @paths.setter
    def paths(self, paths):
        """Sets the paths of this SearchResultLevel4.

        Branches to matching entities

        :param paths: The paths of this SearchResultLevel4.
        :type paths: List[SearchResultLevel5]
        """
        if paths is None:
            raise ValueError("Invalid value for `paths`, must not be `None`")

        self._paths = paths
