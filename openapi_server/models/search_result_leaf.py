# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.address import Address
from openapi_server.models.entity import Entity
from openapi_server.models.neighbor import Neighbor
from openapi_server import util

from openapi_server.models.address import Address  # noqa: E501
from openapi_server.models.entity import Entity  # noqa: E501
from openapi_server.models.neighbor import Neighbor  # noqa: E501

class SearchResultLeaf(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, node=None, relation=None, matching_addresses=None):  # noqa: E501
        """SearchResultLeaf - a model defined in OpenAPI

        :param node: The node of this SearchResultLeaf.  # noqa: E501
        :type node: Entity
        :param relation: The relation of this SearchResultLeaf.  # noqa: E501
        :type relation: Neighbor
        :param matching_addresses: The matching_addresses of this SearchResultLeaf.  # noqa: E501
        :type matching_addresses: List[Address]
        """
        self.openapi_types = {
            'node': Entity,
            'relation': Neighbor,
            'matching_addresses': List[Address]
        }

        self.attribute_map = {
            'node': 'node',
            'relation': 'relation',
            'matching_addresses': 'matching_addresses'
        }

        self._node = node
        self._relation = relation
        self._matching_addresses = matching_addresses

    @classmethod
    def from_dict(cls, dikt) -> 'SearchResultLeaf':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The search_result_leaf of this SearchResultLeaf.  # noqa: E501
        :rtype: SearchResultLeaf
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The SearchResultLeaf as a dict
        :rtype: dict
        """
        return { 'node': self._node,
            'relation': self._relation,
            'matching_addresses': self._matching_addresses }


    @property
    def node(self):
        """Gets the node of this SearchResultLeaf.


        :return: The node of this SearchResultLeaf.
        :rtype: Entity
        """
        return self._node

    @node.setter
    def node(self, node):
        """Sets the node of this SearchResultLeaf.


        :param node: The node of this SearchResultLeaf.
        :type node: Entity
        """

        self._node = node

    @property
    def relation(self):
        """Gets the relation of this SearchResultLeaf.


        :return: The relation of this SearchResultLeaf.
        :rtype: Neighbor
        """
        return self._relation

    @relation.setter
    def relation(self, relation):
        """Sets the relation of this SearchResultLeaf.


        :param relation: The relation of this SearchResultLeaf.
        :type relation: Neighbor
        """

        self._relation = relation

    @property
    def matching_addresses(self):
        """Gets the matching_addresses of this SearchResultLeaf.


        :return: The matching_addresses of this SearchResultLeaf.
        :rtype: List[Address]
        """
        return self._matching_addresses

    @matching_addresses.setter
    def matching_addresses(self, matching_addresses):
        """Sets the matching_addresses of this SearchResultLeaf.


        :param matching_addresses: The matching_addresses of this SearchResultLeaf.
        :type matching_addresses: List[Address]
        """

        self._matching_addresses = matching_addresses