# coding: utf-8
from gsrest.errors import BadUserInputException
from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class TagCloudEntry(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, cnt: int=None, weighted: float=None):
        """TagCloudEntry - a model defined in OpenAPI

        :param cnt: The cnt of this TagCloudEntry.
        :param weighted: The weighted of this TagCloudEntry.
        """
        self.openapi_types = {
            'cnt': int,
            'weighted': float
        }

        self.attribute_map = {
            'cnt': 'cnt',
            'weighted': 'weighted'
        }

        self._cnt = cnt
        self._weighted = weighted

    @classmethod
    def from_dict(cls, dikt: dict) -> 'TagCloudEntry':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The tag_cloud_entry of this TagCloudEntry.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The TagCloudEntry as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'cnt': self._cnt,
            'weighted': self._weighted }


    @property
    def cnt(self):
        """Gets the cnt of this TagCloudEntry.


        :return: The cnt of this TagCloudEntry.
        :rtype: int
        """
        return self._cnt

    @cnt.setter
    def cnt(self, cnt):
        """Sets the cnt of this TagCloudEntry.


        :param cnt: The cnt of this TagCloudEntry.
        :type cnt: int
        """
        if cnt is None:
            raise BadUserInputException("Invalid value for `cnt`, must not be `None`")

        self._cnt = cnt

    @property
    def weighted(self):
        """Gets the weighted of this TagCloudEntry.


        :return: The weighted of this TagCloudEntry.
        :rtype: float
        """
        return self._weighted

    @weighted.setter
    def weighted(self, weighted):
        """Sets the weighted of this TagCloudEntry.


        :param weighted: The weighted of this TagCloudEntry.
        :type weighted: float
        """
        if weighted is None:
            raise BadUserInputException("Invalid value for `weighted`, must not be `None`")

        self._weighted = weighted
