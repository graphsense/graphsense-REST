# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.address_with_tags import AddressWithTags
from openapi_server.models.entity_with_tags import EntityWithTags
from openapi_server.models.neighbor import Neighbor
from openapi_server import util

from openapi_server.models.address_with_tags import AddressWithTags  # noqa: E501
from openapi_server.models.entity_with_tags import EntityWithTags  # noqa: E501
from openapi_server.models.neighbor import Neighbor  # noqa: E501

class SearchPaths(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, paths=None, node=None, relation=None, matching_addresses=None):  # noqa: E501
        """SearchPaths - a model defined in OpenAPI

        :param paths: The paths of this SearchPaths.  # noqa: E501
        :type paths: List[SearchPaths]
        :param node: The node of this SearchPaths.  # noqa: E501
        :type node: EntityWithTags
        :param relation: The relation of this SearchPaths.  # noqa: E501
        :type relation: Neighbor
        :param matching_addresses: The matching_addresses of this SearchPaths.  # noqa: E501
        :type matching_addresses: List[AddressWithTags]
        """
        self.openapi_types = {
            'paths': List[SearchPaths],
            'node': EntityWithTags,
            'relation': Neighbor,
            'matching_addresses': List[AddressWithTags]
        }

        self.attribute_map = {
            'paths': 'paths',
            'node': 'node',
            'relation': 'relation',
            'matching_addresses': 'matching_addresses'
        }

        self._paths = paths
        self._node = node
        self._relation = relation
        self._matching_addresses = matching_addresses

    @classmethod
    def from_dict(cls, dikt) -> 'SearchPaths':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The search_paths of this SearchPaths.  # noqa: E501
        :rtype: SearchPaths
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The SearchPaths as a dict
        :rtype: dict
        """
        return { 'paths': self._paths,
            'node': self._node,
            'relation': self._relation,
            'matching_addresses': self._matching_addresses }


    @property
    def paths(self):
        """Gets the paths of this SearchPaths.

        Paths to matching entities  # noqa: E501

        :return: The paths of this SearchPaths.
        :rtype: List[SearchPaths]
        """
        return self._paths

    @paths.setter
    def paths(self, paths):
        """Sets the paths of this SearchPaths.

        Paths to matching entities  # noqa: E501

        :param paths: The paths of this SearchPaths.
        :type paths: List[SearchPaths]
        """

        self._paths = paths

    @property
    def node(self):
        """Gets the node of this SearchPaths.


        :return: The node of this SearchPaths.
        :rtype: EntityWithTags
        """
        return self._node

    @node.setter
    def node(self, node):
        """Sets the node of this SearchPaths.


        :param node: The node of this SearchPaths.
        :type node: EntityWithTags
        """

        self._node = node

    @property
    def relation(self):
        """Gets the relation of this SearchPaths.


        :return: The relation of this SearchPaths.
        :rtype: Neighbor
        """
        return self._relation

    @relation.setter
    def relation(self, relation):
        """Sets the relation of this SearchPaths.


        :param relation: The relation of this SearchPaths.
        :type relation: Neighbor
        """

        self._relation = relation

    @property
    def matching_addresses(self):
        """Gets the matching_addresses of this SearchPaths.


        :return: The matching_addresses of this SearchPaths.
        :rtype: List[AddressWithTags]
        """
        return self._matching_addresses

    @matching_addresses.setter
    def matching_addresses(self, matching_addresses):
        """Sets the matching_addresses of this SearchPaths.


        :param matching_addresses: The matching_addresses of this SearchPaths.
        :type matching_addresses: List[AddressWithTags]
        """

        self._matching_addresses = matching_addresses
