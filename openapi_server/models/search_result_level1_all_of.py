# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.search_result_level2 import SearchResultLevel2
from openapi_server import util

from openapi_server.models.search_result_level2 import SearchResultLevel2  # noqa: E501

class SearchResultLevel1AllOf(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, paths=None):  # noqa: E501
        """SearchResultLevel1AllOf - a model defined in OpenAPI

        :param paths: The paths of this SearchResultLevel1AllOf.  # noqa: E501
        :type paths: List[SearchResultLevel2]
        """
        self.openapi_types = {
            'paths': List[SearchResultLevel2]
        }

        self.attribute_map = {
            'paths': 'paths'
        }

        self._paths = paths

    @classmethod
    def from_dict(cls, dikt) -> 'SearchResultLevel1AllOf':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The search_result_level1_allOf of this SearchResultLevel1AllOf.  # noqa: E501
        :rtype: SearchResultLevel1AllOf
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The SearchResultLevel1AllOf as a dict
        :rtype: dict
        """
        return { 'paths': self._paths }


    @property
    def paths(self):
        """Gets the paths of this SearchResultLevel1AllOf.

        Branches to matching entities  # noqa: E501

        :return: The paths of this SearchResultLevel1AllOf.
        :rtype: List[SearchResultLevel2]
        """
        return self._paths

    @paths.setter
    def paths(self, paths):
        """Sets the paths of this SearchResultLevel1AllOf.

        Branches to matching entities  # noqa: E501

        :param paths: The paths of this SearchResultLevel1AllOf.
        :type paths: List[SearchResultLevel2]
        """

        self._paths = paths
