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

    def __init__(self, tx_type: str='utxo', tx_hash: str=None, currency: str=None, coinbase: bool=None, height: int=None, timestamp: int=None, value: Values=None):
        """AddressTxUtxo - a model defined in OpenAPI

        :param tx_type: The tx_type of this AddressTxUtxo.
        :param tx_hash: The tx_hash of this AddressTxUtxo.
        :param currency: The currency of this AddressTxUtxo.
        :param coinbase: The coinbase of this AddressTxUtxo.
        :param height: The height of this AddressTxUtxo.
        :param timestamp: The timestamp of this AddressTxUtxo.
        :param value: The value of this AddressTxUtxo.
        """
        self.openapi_types = {
            'tx_type': str,
            'tx_hash': str,
            'currency': str,
            'coinbase': bool,
            'height': int,
            'timestamp': int,
            'value': Values
        }

        self.attribute_map = {
            'tx_type': 'tx_type',
            'tx_hash': 'tx_hash',
            'currency': 'currency',
            'coinbase': 'coinbase',
            'height': 'height',
            'timestamp': 'timestamp',
            'value': 'value'
        }

        self._tx_type = tx_type
        self._tx_hash = tx_hash
        self._currency = currency
        self._coinbase = coinbase
        self._height = height
        self._timestamp = timestamp
        self._value = value

    @classmethod
    def from_dict(cls, dikt: dict) -> 'AddressTxUtxo':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The address_tx_utxo of this AddressTxUtxo.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The AddressTxUtxo as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'tx_type': self._tx_type,
            'tx_hash': self._tx_hash,
            'currency': self._currency,
            'coinbase': self._coinbase,
            'height': self._height,
            'timestamp': self._timestamp,
            'value': self._value }


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
    def currency(self):
        """Gets the currency of this AddressTxUtxo.

        crypto currency code

        :return: The currency of this AddressTxUtxo.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this AddressTxUtxo.

        crypto currency code

        :param currency: The currency of this AddressTxUtxo.
        :type currency: str
        """
        if currency is None:
            raise ValueError("Invalid value for `currency`, must not be `None`")

        self._currency = currency

    @property
    def coinbase(self):
        """Gets the coinbase of this AddressTxUtxo.

        Coinbase transaction flag

        :return: The coinbase of this AddressTxUtxo.
        :rtype: bool
        """
        return self._coinbase

    @coinbase.setter
    def coinbase(self, coinbase):
        """Sets the coinbase of this AddressTxUtxo.

        Coinbase transaction flag

        :param coinbase: The coinbase of this AddressTxUtxo.
        :type coinbase: bool
        """
        if coinbase is None:
            raise ValueError("Invalid value for `coinbase`, must not be `None`")

        self._coinbase = coinbase

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
