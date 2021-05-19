# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.address_with_tags import AddressWithTags
from openapi_server.models.entity_with_tags import EntityWithTags
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.search_result_leaf import SearchResultLeaf
from openapi_server.models.search_result_level2_all_of import SearchResultLevel2AllOf
from openapi_server.models.search_result_level3 import SearchResultLevel3
from openapi_server import util

from openapi_server.models.address_with_tags import AddressWithTags  # noqa: E501
from openapi_server.models.entity_with_tags import EntityWithTags  # noqa: E501
from openapi_server.models.neighbor import Neighbor  # noqa: E501
from openapi_server.models.search_result_leaf import SearchResultLeaf  # noqa: E501
from openapi_server.models.search_result_level2_all_of import SearchResultLevel2AllOf  # noqa: E501
from openapi_server.models.search_result_level3 import SearchResultLevel3  # noqa: E501

class SearchResultLevel2(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, node=None, relation=None, matching_addresses=None, paths=None):  # noqa: E501
        """SearchResultLevel2 - a model defined in OpenAPI

        :param node: The node of this SearchResultLevel2.  # noqa: E501
        :type node: EntityWithTags
        :param relation: The relation of this SearchResultLevel2.  # noqa: E501
        :type relation: Neighbor
        :param matching_addresses: The matching_addresses of this SearchResultLevel2.  # noqa: E501
        :type matching_addresses: List[AddressWithTags]
        :param paths: The paths of this SearchResultLevel2.  # noqa: E501
        :type paths: List[SearchResultLevel3]
        """
        self.openapi_types = {
            'node': EntityWithTags,
            'relation': Neighbor,
            'matching_addresses': List[AddressWithTags],
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
    def from_dict(cls, dikt) -> 'SearchResultLevel2':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The search_result_level2 of this SearchResultLevel2.  # noqa: E501
        :rtype: SearchResultLevel2
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The SearchResultLevel2 as a dict
        :rtype: dict
        """
        return { 'node': self._node,
            'relation': self._relation,
            'matching_addresses': self._matching_addresses,
            'paths': self._paths }


    @property
    def node(self):
        """Gets the node of this SearchResultLevel2.


        :return: The node of this SearchResultLevel2.
        :rtype: EntityWithTags
        """
        return self._node

    @node.setter
    def node(self, node):
        """Sets the node of this SearchResultLevel2.


        :param node: The node of this SearchResultLevel2.
        :type node: EntityWithTags
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
        :rtype: List[AddressWithTags]
        """
        return self._matching_addresses

    @matching_addresses.setter
    def matching_addresses(self, matching_addresses):
        """Sets the matching_addresses of this SearchResultLevel2.


        :param matching_addresses: The matching_addresses of this SearchResultLevel2.
        :type matching_addresses: List[AddressWithTags]
        """

        self._matching_addresses = matching_addresses

    @property
    def paths(self):
        """Gets the paths of this SearchResultLevel2.

        Branches to matching entities  # noqa: E501

        :return: The paths of this SearchResultLevel2.
        :rtype: List[SearchResultLevel3]
        """
        return self._paths

    @paths.setter
    def paths(self, paths):
        """Sets the paths of this SearchResultLevel2.

        Branches to matching entities  # noqa: E501

        :param paths: The paths of this SearchResultLevel2.
        :type paths: List[SearchResultLevel3]
        """

        self._paths = paths
