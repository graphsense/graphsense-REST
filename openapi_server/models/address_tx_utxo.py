# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.values import Values
from openapi_server import util


class AddressTxUtxo(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, height: int=None, timestamp: int=None, tx_hash: str=None, tx_type: str='utxo', value: Values=None):
        """AddressTxUtxo - a model defined in OpenAPI

        :param height: The height of this AddressTxUtxo.
        :param timestamp: The timestamp of this AddressTxUtxo.
        :param tx_hash: The tx_hash of this AddressTxUtxo.
        :param tx_type: The tx_type of this AddressTxUtxo.
        :param value: The value of this AddressTxUtxo.
        """
        self.openapi_types = {
            'height': int,
            'timestamp': int,
            'tx_hash': str,
            'tx_type': str,
            'value': Values
        }

        self.attribute_map = {
            'height': 'height',
            'timestamp': 'timestamp',
            'tx_hash': 'tx_hash',
            'tx_type': 'tx_type',
            'value': 'value'
        }

        self._height = height
        self._timestamp = timestamp
        self._tx_hash = tx_hash
        self._tx_type = tx_type
        self._value = value

    @classmethod
    def from_dict(cls, dikt: dict) -> 'AddressTxUtxo':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The address_tx_utxo of this AddressTxUtxo.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def height(self):
        """Gets the height of this AddressTxUtxo.

        Height

        :return: The height of this AddressTxUtxo.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this AddressTxUtxo.

        Height

        :param height: The height of this AddressTxUtxo.
        :type height: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")
        if height is not None and height < 0:
            raise ValueError("Invalid value for `height`, must be a value greater than or equal to `0`")

        self._height = height

    @property
    def timestamp(self):
        """Gets the timestamp of this AddressTxUtxo.

        Timestamp

        :return: The timestamp of this AddressTxUtxo.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this AddressTxUtxo.

        Timestamp

        :param timestamp: The timestamp of this AddressTxUtxo.
        :type timestamp: int
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")

        self._timestamp = timestamp

    @property
    def tx_hash(self):
        """Gets the tx_hash of this AddressTxUtxo.

        Transaction hash

        :return: The tx_hash of this AddressTxUtxo.
        :rtype: str
        """
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        """Sets the tx_hash of this AddressTxUtxo.

        Transaction hash

        :param tx_hash: The tx_hash of this AddressTxUtxo.
        :type tx_hash: str
        """
        if tx_hash is None:
            raise ValueError("Invalid value for `tx_hash`, must not be `None`")

        self._tx_hash = tx_hash

    @property
    def tx_type(self):
        """Gets the tx_type of this AddressTxUtxo.


        :return: The tx_type of this AddressTxUtxo.
        :rtype: str
        """
        return self._tx_type

    @tx_type.setter
    def tx_type(self, tx_type):
        """Sets the tx_type of this AddressTxUtxo.


        :param tx_type: The tx_type of this AddressTxUtxo.
        :type tx_type: str
        """
        if tx_type is None:
            raise ValueError("Invalid value for `tx_type`, must not be `None`")

        self._tx_type = tx_type

    @property
    def value(self):
        """Gets the value of this AddressTxUtxo.


        :return: The value of this AddressTxUtxo.
        :rtype: Values
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this AddressTxUtxo.


        :param value: The value of this AddressTxUtxo.
        :type value: Values
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")

        self._value = value
