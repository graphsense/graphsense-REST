# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.values import Values
from openapi_server import util

from openapi_server.models.values import Values  # noqa: E501

class TxAccount(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, tx_type='account', tx_hash=None, height=None, timestamp=None, value=None):  # noqa: E501
        """TxAccount - a model defined in OpenAPI

        :param tx_type: The tx_type of this TxAccount.  # noqa: E501
        :type tx_type: str
        :param tx_hash: The tx_hash of this TxAccount.  # noqa: E501
        :type tx_hash: str
        :param height: The height of this TxAccount.  # noqa: E501
        :type height: int
        :param timestamp: The timestamp of this TxAccount.  # noqa: E501
        :type timestamp: int
        :param value: The value of this TxAccount.  # noqa: E501
        :type value: Values
        """
        self.openapi_types = {
            'tx_type': str,
            'tx_hash': str,
            'height': int,
            'timestamp': int,
            'value': Values
        }

        self.attribute_map = {
            'tx_type': 'tx_type',
            'tx_hash': 'tx_hash',
            'height': 'height',
            'timestamp': 'timestamp',
            'value': 'value'
        }

        if tx_type is None:
            raise ValueError("Invalid value for `tx_type`, must not be `None`")  # noqa: E501
        self._tx_type = tx_type
        if tx_hash is None:
            raise ValueError("Invalid value for `tx_hash`, must not be `None`")  # noqa: E501
        self._tx_hash = tx_hash
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501
        self._height = height
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501
        self._timestamp = timestamp
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501
        self._value = value

    @classmethod
    def from_dict(cls, dikt) -> 'TxAccount':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The tx_account of this TxAccount.  # noqa: E501
        :rtype: TxAccount
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The TxAccount as a dict
        :rtype: dict
        """
        return { 'tx_type': self._tx_type,
            'tx_hash': self._tx_hash,
            'height': self._height,
            'timestamp': self._timestamp,
            'value': self._value }


    @property
    def tx_type(self):
        """Gets the tx_type of this TxAccount.


        :return: The tx_type of this TxAccount.
        :rtype: str
        """
        return self._tx_type

    @tx_type.setter
    def tx_type(self, tx_type):
        """Sets the tx_type of this TxAccount.


        :param tx_type: The tx_type of this TxAccount.
        :type tx_type: str
        """
        if tx_type is None:
            raise ValueError("Invalid value for `tx_type`, must not be `None`")  # noqa: E501

        self._tx_type = tx_type

    @property
    def tx_hash(self):
        """Gets the tx_hash of this TxAccount.

        Transaction hash  # noqa: E501

        :return: The tx_hash of this TxAccount.
        :rtype: str
        """
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        """Sets the tx_hash of this TxAccount.

        Transaction hash  # noqa: E501

        :param tx_hash: The tx_hash of this TxAccount.
        :type tx_hash: str
        """
        if tx_hash is None:
            raise ValueError("Invalid value for `tx_hash`, must not be `None`")  # noqa: E501

        self._tx_hash = tx_hash

    @property
    def height(self):
        """Gets the height of this TxAccount.

        Height  # noqa: E501

        :return: The height of this TxAccount.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this TxAccount.

        Height  # noqa: E501

        :param height: The height of this TxAccount.
        :type height: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501
        if height is not None and height < 1:  # noqa: E501
            raise ValueError("Invalid value for `height`, must be a value greater than or equal to `1`")  # noqa: E501

        self._height = height

    @property
    def timestamp(self):
        """Gets the timestamp of this TxAccount.

        Timestamp  # noqa: E501

        :return: The timestamp of this TxAccount.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this TxAccount.

        Timestamp  # noqa: E501

        :param timestamp: The timestamp of this TxAccount.
        :type timestamp: int
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

        self._timestamp = timestamp

    @property
    def value(self):
        """Gets the value of this TxAccount.


        :return: The value of this TxAccount.
        :rtype: Values
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this TxAccount.


        :param value: The value of this TxAccount.
        :type value: Values
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value
