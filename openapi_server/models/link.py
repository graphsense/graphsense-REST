# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.link_utxo import LinkUtxo
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.values import Values
from openapi_server import util

from openapi_server.models.link_utxo import LinkUtxo  # noqa: E501
from openapi_server.models.tx_account import TxAccount  # noqa: E501
from openapi_server.models.values import Values  # noqa: E501

class Link(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, currency_type='account', tx_hash=None, height=None, timestamp=None, input_value=None, output_value=None, values=None):  # noqa: E501
        """Link - a model defined in OpenAPI

        :param currency_type: The currency_type of this Link.  # noqa: E501
        :type currency_type: str
        :param tx_hash: The tx_hash of this Link.  # noqa: E501
        :type tx_hash: str
        :param height: The height of this Link.  # noqa: E501
        :type height: int
        :param timestamp: The timestamp of this Link.  # noqa: E501
        :type timestamp: int
        :param input_value: The input_value of this Link.  # noqa: E501
        :type input_value: Values
        :param output_value: The output_value of this Link.  # noqa: E501
        :type output_value: Values
        :param values: The values of this Link.  # noqa: E501
        :type values: Values
        """
        self.openapi_types = {
            'currency_type': str,
            'tx_hash': str,
            'height': int,
            'timestamp': int,
            'input_value': Values,
            'output_value': Values,
            'values': Values
        }

        self.attribute_map = {
            'currency_type': 'currency_type',
            'tx_hash': 'tx_hash',
            'height': 'height',
            'timestamp': 'timestamp',
            'input_value': 'input_value',
            'output_value': 'output_value',
            'values': 'values'
        }

        if currency_type is None:
            raise ValueError("Invalid value for `currency_type`, must not be `None`")  # noqa: E501
        self._currency_type = currency_type
        if tx_hash is None:
            raise ValueError("Invalid value for `tx_hash`, must not be `None`")  # noqa: E501
        self._tx_hash = tx_hash
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501
        self._height = height
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501
        self._timestamp = timestamp
        if input_value is None:
            raise ValueError("Invalid value for `input_value`, must not be `None`")  # noqa: E501
        self._input_value = input_value
        if output_value is None:
            raise ValueError("Invalid value for `output_value`, must not be `None`")  # noqa: E501
        self._output_value = output_value
        if values is None:
            raise ValueError("Invalid value for `values`, must not be `None`")  # noqa: E501
        self._values = values

    @classmethod
    def from_dict(cls, dikt) -> 'Link':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The link of this Link.  # noqa: E501
        :rtype: Link
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The Link as a dict
        :rtype: dict
        """
        return { 'currency_type': self._currency_type,
            'tx_hash': self._tx_hash,
            'height': self._height,
            'timestamp': self._timestamp,
            'input_value': self._input_value,
            'output_value': self._output_value,
            'values': self._values }


    @property
    def currency_type(self):
        """Gets the currency_type of this Link.


        :return: The currency_type of this Link.
        :rtype: str
        """
        return self._currency_type

    @currency_type.setter
    def currency_type(self, currency_type):
        """Sets the currency_type of this Link.


        :param currency_type: The currency_type of this Link.
        :type currency_type: str
        """
        if currency_type is None:
            raise ValueError("Invalid value for `currency_type`, must not be `None`")  # noqa: E501

        self._currency_type = currency_type

    @property
    def tx_hash(self):
        """Gets the tx_hash of this Link.

        Transaction hash  # noqa: E501

        :return: The tx_hash of this Link.
        :rtype: str
        """
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        """Sets the tx_hash of this Link.

        Transaction hash  # noqa: E501

        :param tx_hash: The tx_hash of this Link.
        :type tx_hash: str
        """
        if tx_hash is None:
            raise ValueError("Invalid value for `tx_hash`, must not be `None`")  # noqa: E501

        self._tx_hash = tx_hash

    @property
    def height(self):
        """Gets the height of this Link.

        Height  # noqa: E501

        :return: The height of this Link.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this Link.

        Height  # noqa: E501

        :param height: The height of this Link.
        :type height: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501
        if height is not None and height < 1:  # noqa: E501
            raise ValueError("Invalid value for `height`, must be a value greater than or equal to `1`")  # noqa: E501

        self._height = height

    @property
    def timestamp(self):
        """Gets the timestamp of this Link.

        Timestamp  # noqa: E501

        :return: The timestamp of this Link.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this Link.

        Timestamp  # noqa: E501

        :param timestamp: The timestamp of this Link.
        :type timestamp: int
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

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
            raise ValueError("Invalid value for `input_value`, must not be `None`")  # noqa: E501

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
            raise ValueError("Invalid value for `output_value`, must not be `None`")  # noqa: E501

        self._output_value = output_value

    @property
    def values(self):
        """Gets the values of this Link.


        :return: The values of this Link.
        :rtype: Values
        """
        return self._values

    @values.setter
    def values(self, values):
        """Sets the values of this Link.


        :param values: The values of this Link.
        :type values: Values
        """
        if values is None:
            raise ValueError("Invalid value for `values`, must not be `None`")  # noqa: E501

        self._values = values
