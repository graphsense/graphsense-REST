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

    def __init__(self, tx_type: str='account', tx_hash: str=None, height: int=None, timestamp: int=None, input_value: Values=None, output_value: Values=None, value: Values=None, from_address: str=None, to_address: str=None):
        """Link - a model defined in OpenAPI

        :param tx_type: The tx_type of this Link.
        :param tx_hash: The tx_hash of this Link.
        :param height: The height of this Link.
        :param timestamp: The timestamp of this Link.
        :param input_value: The input_value of this Link.
        :param output_value: The output_value of this Link.
        :param value: The value of this Link.
        :param from_address: The from_address of this Link.
        :param to_address: The to_address of this Link.
        """
        self.openapi_types = {
            'tx_type': str,
            'tx_hash': str,
            'height': int,
            'timestamp': int,
            'input_value': Values,
            'output_value': Values,
            'value': Values,
            'from_address': str,
            'to_address': str
        }

        self.attribute_map = {
            'tx_type': 'tx_type',
            'tx_hash': 'tx_hash',
            'height': 'height',
            'timestamp': 'timestamp',
            'input_value': 'input_value',
            'output_value': 'output_value',
            'value': 'value',
            'from_address': 'from_address',
            'to_address': 'to_address'
        }

        self._tx_type = tx_type
        self._tx_hash = tx_hash
        self._height = height
        self._timestamp = timestamp
        self._input_value = input_value
        self._output_value = output_value
        self._value = value
        self._from_address = from_address
        self._to_address = to_address

    @classmethod
    def from_dict(cls, dikt: dict) -> 'Link':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The link of this Link.
        """
        return util.deserialize_model(dikt, cls)

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
