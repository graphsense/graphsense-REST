# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class TxSummary(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, height: int=None, timestamp: int=None, tx_hash: str=None):
        """TxSummary - a model defined in OpenAPI

        :param height: The height of this TxSummary.
        :param timestamp: The timestamp of this TxSummary.
        :param tx_hash: The tx_hash of this TxSummary.
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
    def from_dict(cls, dikt: dict) -> 'TxSummary':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The tx_summary of this TxSummary.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The TxSummary as a dict
        :rtype: dict
        """
        return { 'height': self._height,
            'timestamp': self._timestamp,
            'tx_hash': self._tx_hash }


    @property
    def height(self):
        """Gets the height of this TxSummary.

        Height

        :return: The height of this TxSummary.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this TxSummary.

        Height

        :param height: The height of this TxSummary.
        :type height: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")
        if height is not None and height < 0:
            raise ValueError("Invalid value for `height`, must be a value greater than or equal to `0`")

        self._height = height

    @property
    def timestamp(self):
        """Gets the timestamp of this TxSummary.

        Timestamp

        :return: The timestamp of this TxSummary.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this TxSummary.

        Timestamp

        :param timestamp: The timestamp of this TxSummary.
        :type timestamp: int
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")

        self._timestamp = timestamp

    @property
    def tx_hash(self):
        """Gets the tx_hash of this TxSummary.

        Transaction hash

        :return: The tx_hash of this TxSummary.
        :rtype: str
        """
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        """Sets the tx_hash of this TxSummary.

        Transaction hash

        :param tx_hash: The tx_hash of this TxSummary.
        :type tx_hash: str
        """
        if tx_hash is None:
            raise ValueError("Invalid value for `tx_hash`, must not be `None`")

        self._tx_hash = tx_hash
