# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.address import Address
from openapi_server.models.entity import Entity
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.search_result_leaf import SearchResultLeaf
from openapi_server.models.search_result_level1_all_of import SearchResultLevel1AllOf
from openapi_server.models.search_result_level2 import SearchResultLevel2
from openapi_server import util

from openapi_server.models.address import Address  # noqa: E501
from openapi_server.models.entity import Entity  # noqa: E501
from openapi_server.models.neighbor import Neighbor  # noqa: E501
from openapi_server.models.search_result_leaf import SearchResultLeaf  # noqa: E501
from openapi_server.models.search_result_level1_all_of import SearchResultLevel1AllOf  # noqa: E501
from openapi_server.models.search_result_level2 import SearchResultLevel2  # noqa: E501

class SearchResultLevel1(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, node=None, relation=None, matching_addresses=None, paths=None):  # noqa: E501
        """SearchResultLevel1 - a model defined in OpenAPI

        :param node: The node of this SearchResultLevel1.  # noqa: E501
        :type node: Entity
        :param relation: The relation of this SearchResultLevel1.  # noqa: E501
        :type relation: Neighbor
        :param matching_addresses: The matching_addresses of this SearchResultLevel1.  # noqa: E501
        :type matching_addresses: List[Address]
        :param paths: The paths of this SearchResultLevel1.  # noqa: E501
        :type paths: List[SearchResultLevel2]
        """
        self.openapi_types = {
            'node': Entity,
            'relation': Neighbor,
            'matching_addresses': List[Address],
            'paths': List[SearchResultLevel2]
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
    def from_dict(cls, dikt) -> 'SearchResultLevel1':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The search_result_level1 of this SearchResultLevel1.  # noqa: E501
        :rtype: SearchResultLevel1
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The SearchResultLevel1 as a dict
        :rtype: dict
        """
        return { 'node': self._node,
            'relation': self._relation,
            'matching_addresses': self._matching_addresses,
            'paths': self._paths }


    @property
    def node(self):
        """Gets the node of this SearchResultLevel1.


        :return: The node of this SearchResultLevel1.
        :rtype: Entity
        """
        return self._node

    @node.setter
    def node(self, node):
        """Sets the node of this SearchResultLevel1.


        :param node: The node of this SearchResultLevel1.
        :type node: Entity
        """

        self._node = node

    @property
    def relation(self):
        """Gets the relation of this SearchResultLevel1.


        :return: The relation of this SearchResultLevel1.
        :rtype: Neighbor
        """
        return self._relation

    @relation.setter
    def relation(self, relation):
        """Sets the relation of this SearchResultLevel1.


        :param relation: The relation of this SearchResultLevel1.
        :type relation: Neighbor
        """

        self._relation = relation

    @property
    def matching_addresses(self):
        """Gets the matching_addresses of this SearchResultLevel1.


        :return: The matching_addresses of this SearchResultLevel1.
        :rtype: List[Address]
        """
        return self._matching_addresses

    @matching_addresses.setter
    def matching_addresses(self, matching_addresses):
        """Sets the matching_addresses of this SearchResultLevel1.


        :param matching_addresses: The matching_addresses of this SearchResultLevel1.
        :type matching_addresses: List[Address]
        """

        self._matching_addresses = matching_addresses

    @property
    def paths(self):
        """Gets the paths of this SearchResultLevel1.

        Branches to matching entities  # noqa: E501

        :return: The paths of this SearchResultLevel1.
        :rtype: List[SearchResultLevel2]
        """
        return self._paths

    @paths.setter
    def paths(self, paths):
        """Sets the paths of this SearchResultLevel1.

        Branches to matching entities  # noqa: E501

        :param paths: The paths of this SearchResultLevel1.
        :type paths: List[SearchResultLevel2]
        """

        self._paths = paths
