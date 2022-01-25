# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.address import Address
from openapi_server.models.entity import Entity
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.search_result_leaf import SearchResultLeaf
from openapi_server.models.search_result_level5_all_of import SearchResultLevel5AllOf
from openapi_server.models.search_result_level6 import SearchResultLevel6
from openapi_server import util


class SearchResultLevel5(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, matching_addresses: List[Address]=None, node: Entity=None, relation: Neighbor=None, paths: List[SearchResultLevel6]=None):
        """SearchResultLevel5 - a model defined in OpenAPI

        :param matching_addresses: The matching_addresses of this SearchResultLevel5.
        :param node: The node of this SearchResultLevel5.
        :param relation: The relation of this SearchResultLevel5.
        :param paths: The paths of this SearchResultLevel5.
        """
        self.openapi_types = {
            'matching_addresses': List[Address],
            'node': Entity,
            'relation': Neighbor,
            'paths': List[SearchResultLevel6]
        }

        self.attribute_map = {
            'matching_addresses': 'matching_addresses',
            'node': 'node',
            'relation': 'relation',
            'paths': 'paths'
        }

        self._matching_addresses = matching_addresses
        self._node = node
        self._relation = relation
        self._paths = paths

    @classmethod
    def from_dict(cls, dikt: dict) -> 'SearchResultLevel5':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The search_result_level5 of this SearchResultLevel5.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The SearchResultLevel5 as a dict
        :rtype: dict
        """
        return { 'matching_addresses': self._matching_addresses,
            'node': self._node,
            'relation': self._relation,
            'paths': self._paths }


    @property
    def matching_addresses(self):
        """Gets the matching_addresses of this SearchResultLevel5.


        :return: The matching_addresses of this SearchResultLevel5.
        :rtype: List[Address]
        """
        return self._matching_addresses

    @matching_addresses.setter
    def matching_addresses(self, matching_addresses):
        """Sets the matching_addresses of this SearchResultLevel5.


        :param matching_addresses: The matching_addresses of this SearchResultLevel5.
        :type matching_addresses: List[Address]
        """

        self._matching_addresses = matching_addresses

    @property
    def node(self):
        """Gets the node of this SearchResultLevel5.


        :return: The node of this SearchResultLevel5.
        :rtype: Entity
        """
        return self._node

    @node.setter
    def node(self, node):
        """Sets the node of this SearchResultLevel5.


        :param node: The node of this SearchResultLevel5.
        :type node: Entity
        """

        self._node = node

    @property
    def relation(self):
        """Gets the relation of this SearchResultLevel5.


        :return: The relation of this SearchResultLevel5.
        :rtype: Neighbor
        """
        return self._relation

    @relation.setter
    def relation(self, relation):
        """Sets the relation of this SearchResultLevel5.


        :param relation: The relation of this SearchResultLevel5.
        :type relation: Neighbor
        """

        self._relation = relation

    @property
    def paths(self):
        """Gets the paths of this SearchResultLevel5.

        Branches to matching entities

        :return: The paths of this SearchResultLevel5.
        :rtype: List[SearchResultLevel6]
        """
        return self._paths

    @paths.setter
    def paths(self, paths):
        """Sets the paths of this SearchResultLevel5.

        Branches to matching entities

        :param paths: The paths of this SearchResultLevel5.
        :type paths: List[SearchResultLevel6]
        """

        self._paths = paths
