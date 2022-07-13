# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.link_utxo import LinkUtxo
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.values import Values
from openapi_server import util


class Link(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, currency: str=None, height: int=None, input_value: Values=None, output_value: Values=None, timestamp: int=None, tx_hash: str=None, tx_type: str='account', from_address: str=None, to_address: str=None, value: Values=None):
        """Link - a model defined in OpenAPI

        :param currency: The currency of this Link.
        :param height: The height of this Link.
        :param input_value: The input_value of this Link.
        :param output_value: The output_value of this Link.
        :param timestamp: The timestamp of this Link.
        :param tx_hash: The tx_hash of this Link.
        :param tx_type: The tx_type of this Link.
        :param from_address: The from_address of this Link.
        :param to_address: The to_address of this Link.
        :param value: The value of this Link.
        """
        self.openapi_types = {
            'currency': str,
            'height': int,
            'input_value': Values,
            'output_value': Values,
            'timestamp': int,
            'tx_hash': str,
            'tx_type': str,
            'from_address': str,
            'to_address': str,
            'value': Values
        }

        self.attribute_map = {
            'currency': 'currency',
            'height': 'height',
            'input_value': 'input_value',
            'output_value': 'output_value',
            'timestamp': 'timestamp',
            'tx_hash': 'tx_hash',
            'tx_type': 'tx_type',
            'from_address': 'from_address',
            'to_address': 'to_address',
            'value': 'value'
        }

        self._currency = currency
        self._height = height
        self._input_value = input_value
        self._output_value = output_value
        self._timestamp = timestamp
        self._tx_hash = tx_hash
        self._tx_type = tx_type
        self._from_address = from_address
        self._to_address = to_address
        self._value = value

    @classmethod
    def from_dict(cls, dikt: dict) -> 'Link':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The link of this Link.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The Link as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'currency': self._currency,
            'height': self._height,
            'input_value': self._input_value,
            'output_value': self._output_value,
            'timestamp': self._timestamp,
            'tx_hash': self._tx_hash,
            'tx_type': self._tx_type,
            'from_address': self._from_address,
            'to_address': self._to_address,
            'value': self._value }


    @property
    def currency(self):
        """Gets the currency of this Link.

        crypto currency code

        :return: The currency of this Link.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this Link.

        crypto currency code

        :param currency: The currency of this Link.
        :type currency: str
        """
        if currency is None:
            raise ValueError("Invalid value for `currency`, must not be `None`")

        self._currency = currency

    @property
    def height(self):
        """Gets the height of this Link.

        Height

        :return: The height of this Link.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this Link.

        Height

        :param height: The height of this Link.
        :type height: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")
        if height is not None and height < 0:
            raise ValueError("Invalid value for `height`, must be a value greater than or equal to `0`")

        self._height = height

    @property
    def input_value(self):
        """Gets the input_value of this Link.


        :return: The input_value of this Link.
        :rtype: Values
        """
        return self._input_value

    @input_value.setter
    def input_value(self, input_value):
        """Sets the input_value of this Link.


        :param input_value: The input_value of this Link.
        :type input_value: Values
        """
        if input_value is None:
            raise ValueError("Invalid value for `input_value`, must not be `None`")

        self._input_value = input_value

    @property
    def output_value(self):
        """Gets the output_value of this Link.


        :return: The output_value of this Link.
        :rtype: Values
        """
        return self._output_value

    @output_value.setter
    def output_value(self, output_value):
        """Sets the output_value of this Link.


        :param output_value: The output_value of this Link.
        :type output_value: Values
        """
        if output_value is None:
            raise ValueError("Invalid value for `output_value`, must not be `None`")

        self._output_value = output_value

    @property
    def timestamp(self):
        """Gets the timestamp of this Link.

        Timestamp

        :return: The timestamp of this Link.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this Link.

        Timestamp

        :param timestamp: The timestamp of this Link.
        :type timestamp: int
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")

        self._timestamp = timestamp

    @property
    def tx_hash(self):
        """Gets the tx_hash of this Link.

        Transaction hash

        :return: The tx_hash of this Link.
        :rtype: str
        """
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        """Sets the tx_hash of this Link.

        Transaction hash

        :param tx_hash: The tx_hash of this Link.
        :type tx_hash: str
        """
        if tx_hash is None:
            raise ValueError("Invalid value for `tx_hash`, must not be `None`")

        self._tx_hash = tx_hash

    @property
    def tx_type(self):
        """Gets the tx_type of this Link.


        :return: The tx_type of this Link.
        :rtype: str
        """
        return self._tx_type

    @tx_type.setter
    def tx_type(self, tx_type):
        """Sets the tx_type of this Link.


        :param tx_type: The tx_type of this Link.
        :type tx_type: str
        """
        if tx_type is None:
            raise ValueError("Invalid value for `tx_type`, must not be `None`")

        self._tx_type = tx_type

    @property
    def from_address(self):
        """Gets the from_address of this Link.

        Address

        :return: The from_address of this Link.
        :rtype: str
        """
        return self._from_address

    @from_address.setter
    def from_address(self, from_address):
        """Sets the from_address of this Link.

        Address

        :param from_address: The from_address of this Link.
        :type from_address: str
        """
        if from_address is None:
            raise ValueError("Invalid value for `from_address`, must not be `None`")

        self._from_address = from_address

    @property
    def to_address(self):
        """Gets the to_address of this Link.

        Address

        :return: The to_address of this Link.
        :rtype: str
        """
        return self._to_address

    @to_address.setter
    def to_address(self, to_address):
        """Sets the to_address of this Link.

        Address

        :param to_address: The to_address of this Link.
        :type to_address: str
        """
        if to_address is None:
            raise ValueError("Invalid value for `to_address`, must not be `None`")

        self._to_address = to_address

    @property
    def value(self):
        """Gets the value of this Link.


        :return: The value of this Link.
        :rtype: Values
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this Link.


        :param value: The value of this Link.
        :type value: Values
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")

        self._value = value
