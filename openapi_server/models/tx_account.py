# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.values import Values
from openapi_server import util


class TxAccount(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, tx_type: str='account', currency: str=None, tx_hash: str=None, height: int=None, timestamp: int=None, value: Values=None, token_values: Dict[str, Values]=None, from_address: str=None, to_address: str=None):
        """TxAccount - a model defined in OpenAPI

        :param tx_type: The tx_type of this TxAccount.
        :param currency: The currency of this TxAccount.
        :param tx_hash: The tx_hash of this TxAccount.
        :param height: The height of this TxAccount.
        :param timestamp: The timestamp of this TxAccount.
        :param value: The value of this TxAccount.
        :param token_values: The token_values of this TxAccount.
        :param from_address: The from_address of this TxAccount.
        :param to_address: The to_address of this TxAccount.
        """
        self.openapi_types = {
            'tx_type': str,
            'currency': str,
            'tx_hash': str,
            'height': int,
            'timestamp': int,
            'value': Values,
            'token_values': Dict[str, Values],
            'from_address': str,
            'to_address': str
        }

        self.attribute_map = {
            'tx_type': 'tx_type',
            'currency': 'currency',
            'tx_hash': 'tx_hash',
            'height': 'height',
            'timestamp': 'timestamp',
            'value': 'value',
            'token_values': 'token_values',
            'from_address': 'from_address',
            'to_address': 'to_address'
        }

        self._tx_type = tx_type
        self._currency = currency
        self._tx_hash = tx_hash
        self._height = height
        self._timestamp = timestamp
        self._value = value
        self._token_values = token_values
        self._from_address = from_address
        self._to_address = to_address

    @classmethod
    def from_dict(cls, dikt: dict) -> 'TxAccount':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The tx_account of this TxAccount.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The TxAccount as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'tx_type': self._tx_type,
            'currency': self._currency,
            'tx_hash': self._tx_hash,
            'height': self._height,
            'timestamp': self._timestamp,
            'value': self._value,
            'token_values': self._token_values,
            'from_address': self._from_address,
            'to_address': self._to_address }


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
            raise ValueError("Invalid value for `tx_type`, must not be `None`")

        self._tx_type = tx_type

    @property
    def currency(self):
        """Gets the currency of this TxAccount.

        crypto currency code

        :return: The currency of this TxAccount.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this TxAccount.

        crypto currency code

        :param currency: The currency of this TxAccount.
        :type currency: str
        """
        if currency is None:
            raise ValueError("Invalid value for `currency`, must not be `None`")

        self._currency = currency

    @property
    def tx_hash(self):
        """Gets the tx_hash of this TxAccount.

        Transaction hash

        :return: The tx_hash of this TxAccount.
        :rtype: str
        """
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        """Sets the tx_hash of this TxAccount.

        Transaction hash

        :param tx_hash: The tx_hash of this TxAccount.
        :type tx_hash: str
        """
        if tx_hash is None:
            raise ValueError("Invalid value for `tx_hash`, must not be `None`")

        self._tx_hash = tx_hash

    @property
    def height(self):
        """Gets the height of this TxAccount.

        Height

        :return: The height of this TxAccount.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this TxAccount.

        Height

        :param height: The height of this TxAccount.
        :type height: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")
        if height is not None and height < 0:
            raise ValueError("Invalid value for `height`, must be a value greater than or equal to `0`")

        self._height = height

    @property
    def timestamp(self):
        """Gets the timestamp of this TxAccount.

        Timestamp

        :return: The timestamp of this TxAccount.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this TxAccount.

        Timestamp

        :param timestamp: The timestamp of this TxAccount.
        :type timestamp: int
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")

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
            raise ValueError("Invalid value for `value`, must not be `None`")

        self._value = value

    @property
    def token_values(self):
        """Gets the token_values of this TxAccount.

        Per token value-flow

        :return: The token_values of this TxAccount.
        :rtype: Dict[str, Values]
        """
        return self._token_values

    @token_values.setter
    def token_values(self, token_values):
        """Sets the token_values of this TxAccount.

        Per token value-flow

        :param token_values: The token_values of this TxAccount.
        :type token_values: Dict[str, Values]
        """

        self._token_values = token_values

    @property
    def from_address(self):
        """Gets the from_address of this TxAccount.

        Address

        :return: The from_address of this TxAccount.
        :rtype: str
        """
        return self._from_address

    @from_address.setter
    def from_address(self, from_address):
        """Sets the from_address of this TxAccount.

        Address

        :param from_address: The from_address of this TxAccount.
        :type from_address: str
        """
        if from_address is None:
            raise ValueError("Invalid value for `from_address`, must not be `None`")

        self._from_address = from_address

    @property
    def to_address(self):
        """Gets the to_address of this TxAccount.

        Address

        :return: The to_address of this TxAccount.
        :rtype: str
        """
        return self._to_address

    @to_address.setter
    def to_address(self, to_address):
        """Sets the to_address of this TxAccount.

        Address

        :param to_address: The to_address of this TxAccount.
        :type to_address: str
        """
        if to_address is None:
            raise ValueError("Invalid value for `to_address`, must not be `None`")

        self._to_address = to_address
