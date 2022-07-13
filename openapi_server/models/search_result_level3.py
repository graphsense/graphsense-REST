# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.address import Address
from openapi_server.models.neighbor_entity import NeighborEntity
from openapi_server.models.search_result_leaf import SearchResultLeaf
from openapi_server.models.search_result_level3_all_of import SearchResultLevel3AllOf
from openapi_server.models.search_result_level4 import SearchResultLevel4
from openapi_server import util


class SearchResultLevel3(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, matching_addresses: List[Address]=None, neighbor: NeighborEntity=None, paths: List[SearchResultLevel4]=None):
        """SearchResultLevel3 - a model defined in OpenAPI

        :param matching_addresses: The matching_addresses of this SearchResultLevel3.
        :param neighbor: The neighbor of this SearchResultLevel3.
        :param paths: The paths of this SearchResultLevel3.
        """
        self.openapi_types = {
            'matching_addresses': List[Address],
            'neighbor': NeighborEntity,
            'paths': List[SearchResultLevel4]
        }

        self.attribute_map = {
            'matching_addresses': 'matching_addresses',
            'neighbor': 'neighbor',
            'paths': 'paths'
        }

        self._matching_addresses = matching_addresses
        self._neighbor = neighbor
        self._paths = paths

    @classmethod
    def from_dict(cls, dikt: dict) -> 'SearchResultLevel3':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The search_result_level3 of this SearchResultLevel3.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The SearchResultLevel3 as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'matching_addresses': self._matching_addresses,
            'neighbor': self._neighbor,
            'paths': self._paths }


    @property
    def matching_addresses(self):
        """Gets the matching_addresses of this SearchResultLevel3.


        :return: The matching_addresses of this SearchResultLevel3.
        :rtype: List[Address]
        """
        return self._matching_addresses

    @matching_addresses.setter
    def matching_addresses(self, matching_addresses):
        """Sets the matching_addresses of this SearchResultLevel3.


        :param matching_addresses: The matching_addresses of this SearchResultLevel3.
        :type matching_addresses: List[Address]
        """
        if matching_addresses is None:
            raise ValueError("Invalid value for `matching_addresses`, must not be `None`")

        self._matching_addresses = matching_addresses

    @property
    def neighbor(self):
        """Gets the neighbor of this SearchResultLevel3.


        :return: The neighbor of this SearchResultLevel3.
        :rtype: NeighborEntity
        """
        return self._neighbor

    @neighbor.setter
    def neighbor(self, neighbor):
        """Sets the neighbor of this SearchResultLevel3.


        :param neighbor: The neighbor of this SearchResultLevel3.
        :type neighbor: NeighborEntity
        """
        if neighbor is None:
            raise ValueError("Invalid value for `neighbor`, must not be `None`")

        self._neighbor = neighbor

    @property
    def paths(self):
        """Gets the paths of this SearchResultLevel3.

        Branches to matching entities

        :return: The paths of this SearchResultLevel3.
        :rtype: List[SearchResultLevel4]
        """
        return self._paths

    @paths.setter
    def paths(self, paths):
        """Sets the paths of this SearchResultLevel3.

        Branches to matching entities

        :param paths: The paths of this SearchResultLevel3.
        :type paths: List[SearchResultLevel4]
        """
        if paths is None:
            raise ValueError("Invalid value for `paths`, must not be `None`")

        self._paths = paths
