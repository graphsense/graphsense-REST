# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.address import Address
from openapi_server.models.entity import Entity
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.search_result_leaf import SearchResultLeaf
from openapi_server.models.search_result_level2_all_of import SearchResultLevel2AllOf
from openapi_server.models.search_result_level3 import SearchResultLevel3
from openapi_server import util


class SearchResultLevel2(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, node: Entity=None, relation: Neighbor=None, matching_addresses: List[Address]=None, paths: List[SearchResultLevel3]=None):
        """SearchResultLevel2 - a model defined in OpenAPI

        :param node: The node of this SearchResultLevel2.
        :param relation: The relation of this SearchResultLevel2.
        :param matching_addresses: The matching_addresses of this SearchResultLevel2.
        :param paths: The paths of this SearchResultLevel2.
        """
        self.openapi_types = {
            'node': Entity,
            'relation': Neighbor,
            'matching_addresses': List[Address],
            'paths': List[SearchResultLevel3]
        }

        self.attribute_map = {
            'node': 'node',
            'relation': 'relation',
            'matching_addresses': 'matching_addresses',
            'paths': 'paths'
        }

        self._node = node
        self._relation = relation
        self._matching_addresses = matching_addresses
        self._paths = paths

    @classmethod
    def from_dict(cls, dikt: dict) -> 'SearchResultLevel2':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The search_result_level2 of this SearchResultLevel2.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def node(self):
        """Gets the node of this SearchResultLevel2.


        :return: The node of this SearchResultLevel2.
        :rtype: Entity
        """
        return self._node

    @node.setter
    def node(self, node):
        """Sets the node of this SearchResultLevel2.


        :param node: The node of this SearchResultLevel2.
        :type node: Entity
        """

        self._node = node

    @property
    def relation(self):
        """Gets the relation of this SearchResultLevel2.


        :return: The relation of this SearchResultLevel2.
        :rtype: Neighbor
        """
        return self._relation

    @relation.setter
    def relation(self, relation):
        """Sets the relation of this SearchResultLevel2.


        :param relation: The relation of this SearchResultLevel2.
        :type relation: Neighbor
        """

        self._relation = relation

    @property
    def matching_addresses(self):
        """Gets the matching_addresses of this SearchResultLevel2.


        :return: The matching_addresses of this SearchResultLevel2.
        :rtype: List[Address]
        """
        return self._matching_addresses

    @matching_addresses.setter
    def matching_addresses(self, matching_addresses):
        """Sets the matching_addresses of this SearchResultLevel2.


        :param matching_addresses: The matching_addresses of this SearchResultLevel2.
        :type matching_addresses: List[Address]
        """

        self._matching_addresses = matching_addresses

    @property
    def paths(self):
        """Gets the paths of this SearchResultLevel2.

        Branches to matching entities

        :return: The paths of this SearchResultLevel2.
        :rtype: List[SearchResultLevel3]
        """
        return self._paths

    @paths.setter
    def paths(self, paths):
        """Sets the paths of this SearchResultLevel2.

        Branches to matching entities

        :param paths: The paths of this SearchResultLevel2.
        :type paths: List[SearchResultLevel3]
        """

        self._paths = paths
