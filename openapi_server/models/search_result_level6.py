# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.address import Address
from openapi_server.models.entity import Entity
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.search_result_leaf import SearchResultLeaf
from openapi_server.models.search_result_level6_all_of import SearchResultLevel6AllOf
from openapi_server import util


class SearchResultLevel6(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, matching_addresses: List[Address]=None, node: Entity=None, relation: Neighbor=None, paths: List[SearchResultLeaf]=None):
        """SearchResultLevel6 - a model defined in OpenAPI

        :param matching_addresses: The matching_addresses of this SearchResultLevel6.
        :param node: The node of this SearchResultLevel6.
        :param relation: The relation of this SearchResultLevel6.
        :param paths: The paths of this SearchResultLevel6.
        """
        self.openapi_types = {
            'matching_addresses': List[Address],
            'node': Entity,
            'relation': Neighbor,
            'paths': List[SearchResultLeaf]
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
    def from_dict(cls, dikt: dict) -> 'SearchResultLevel6':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The search_result_level6 of this SearchResultLevel6.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The SearchResultLevel6 as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'matching_addresses': self._matching_addresses,
            'node': self._node,
            'relation': self._relation,
            'paths': self._paths }


    @property
    def matching_addresses(self):
        """Gets the matching_addresses of this SearchResultLevel6.


        :return: The matching_addresses of this SearchResultLevel6.
        :rtype: List[Address]
        """
        return self._matching_addresses

    @matching_addresses.setter
    def matching_addresses(self, matching_addresses):
        """Sets the matching_addresses of this SearchResultLevel6.


        :param matching_addresses: The matching_addresses of this SearchResultLevel6.
        :type matching_addresses: List[Address]
        """

        self._matching_addresses = matching_addresses

    @property
    def node(self):
        """Gets the node of this SearchResultLevel6.


        :return: The node of this SearchResultLevel6.
        :rtype: Entity
        """
        return self._node

    @node.setter
    def node(self, node):
        """Sets the node of this SearchResultLevel6.


        :param node: The node of this SearchResultLevel6.
        :type node: Entity
        """

        self._node = node

    @property
    def relation(self):
        """Gets the relation of this SearchResultLevel6.


        :return: The relation of this SearchResultLevel6.
        :rtype: Neighbor
        """
        return self._relation

    @relation.setter
    def relation(self, relation):
        """Sets the relation of this SearchResultLevel6.


        :param relation: The relation of this SearchResultLevel6.
        :type relation: Neighbor
        """

        self._relation = relation

    @property
    def paths(self):
        """Gets the paths of this SearchResultLevel6.

        Branches to matching entities

        :return: The paths of this SearchResultLevel6.
        :rtype: List[SearchResultLeaf]
        """
        return self._paths

    @paths.setter
    def paths(self, paths):
        """Sets the paths of this SearchResultLevel6.

        Branches to matching entities

        :param paths: The paths of this SearchResultLevel6.
        :type paths: List[SearchResultLeaf]
        """

        self._paths = paths
