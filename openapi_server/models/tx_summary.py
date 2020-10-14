# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class TxSummary(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, height=None, timestamp=None, tx_hash=None):  # noqa: E501
        """TxSummary - a model defined in OpenAPI

        :param height: The height of this TxSummary.  # noqa: E501
        :type height: int
        :param timestamp: The timestamp of this TxSummary.  # noqa: E501
        :type timestamp: int
        :param tx_hash: The tx_hash of this TxSummary.  # noqa: E501
        :type tx_hash: str
        """
        self.openapi_types = {
            'height': int,
            'timestamp': int,
            'tx_hash': str
        }

        self.attribute_map = {
            'height': 'height',
            'timestamp': 'timestamp',
            'tx_hash': 'tx_hash'
        }

        self._height = height
        self._timestamp = timestamp
        self._tx_hash = tx_hash

    @classmethod
    def from_dict(cls, dikt) -> 'TxSummary':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The tx_summary of this TxSummary.  # noqa: E501
        :rtype: TxSummary
        """
        return util.deserialize_model(dikt, cls)

    @property
    def height(self):
        """Gets the height of this TxSummary.

        Transaction height  # noqa: E501

        :return: The height of this TxSummary.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this TxSummary.

        Transaction height  # noqa: E501

        :param height: The height of this TxSummary.
        :type height: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501

        self._height = height

    @property
    def timestamp(self):
        """Gets the timestamp of this TxSummary.

        Transaction timestamp  # noqa: E501

        :return: The timestamp of this TxSummary.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this TxSummary.

        Transaction timestamp  # noqa: E501

        :param timestamp: The timestamp of this TxSummary.
        :type timestamp: int
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

        self._timestamp = timestamp

    @property
    def tx_hash(self):
        """Gets the tx_hash of this TxSummary.

        Transaction hash  # noqa: E501

        :return: The tx_hash of this TxSummary.
        :rtype: str
        """
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        """Sets the tx_hash of this TxSummary.

        Transaction hash  # noqa: E501

        :param tx_hash: The tx_hash of this TxSummary.
        :type tx_hash: str
        """
        if tx_hash is None:
            raise ValueError("Invalid value for `tx_hash`, must not be `None`")  # noqa: E501

        self._tx_hash = tx_hash
