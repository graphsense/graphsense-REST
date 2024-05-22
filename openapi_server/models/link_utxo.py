# coding: utf-8
from gsrest.errors import BadUserInputException
from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.values import Values
from openapi_server import util


class LinkUtxo(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, tx_type: str='utxo', tx_hash: str=None, currency: str=None, height: int=None, timestamp: int=None, input_value: Values=None, output_value: Values=None):
        """LinkUtxo - a model defined in OpenAPI

        :param tx_type: The tx_type of this LinkUtxo.
        :param tx_hash: The tx_hash of this LinkUtxo.
        :param currency: The currency of this LinkUtxo.
        :param height: The height of this LinkUtxo.
        :param timestamp: The timestamp of this LinkUtxo.
        :param input_value: The input_value of this LinkUtxo.
        :param output_value: The output_value of this LinkUtxo.
        """
        self.openapi_types = {
            'tx_type': str,
            'tx_hash': str,
            'currency': str,
            'height': int,
            'timestamp': int,
            'input_value': Values,
            'output_value': Values
        }

        self.attribute_map = {
            'tx_type': 'tx_type',
            'tx_hash': 'tx_hash',
            'currency': 'currency',
            'height': 'height',
            'timestamp': 'timestamp',
            'input_value': 'input_value',
            'output_value': 'output_value'
        }

        self._tx_type = tx_type
        self._tx_hash = tx_hash
        self._currency = currency
        self._height = height
        self._timestamp = timestamp
        self._input_value = input_value
        self._output_value = output_value

    @classmethod
    def from_dict(cls, dikt: dict) -> 'LinkUtxo':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The link_utxo of this LinkUtxo.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The LinkUtxo as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'tx_type': self._tx_type,
            'tx_hash': self._tx_hash,
            'currency': self._currency,
            'height': self._height,
            'timestamp': self._timestamp,
            'input_value': self._input_value,
            'output_value': self._output_value }


    @property
    def tx_type(self):
        """Gets the tx_type of this LinkUtxo.


        :return: The tx_type of this LinkUtxo.
        :rtype: str
        """
        return self._tx_type

    @tx_type.setter
    def tx_type(self, tx_type):
        """Sets the tx_type of this LinkUtxo.


        :param tx_type: The tx_type of this LinkUtxo.
        :type tx_type: str
        """
        if tx_type is None:
            raise BadUserInputException("Invalid value for `tx_type`, must not be `None`")

        self._tx_type = tx_type

    @property
    def tx_hash(self):
        """Gets the tx_hash of this LinkUtxo.

        Transaction hash

        :return: The tx_hash of this LinkUtxo.
        :rtype: str
        """
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        """Sets the tx_hash of this LinkUtxo.

        Transaction hash

        :param tx_hash: The tx_hash of this LinkUtxo.
        :type tx_hash: str
        """
        if tx_hash is None:
            raise BadUserInputException("Invalid value for `tx_hash`, must not be `None`")

        self._tx_hash = tx_hash

    @property
    def currency(self):
        """Gets the currency of this LinkUtxo.

        crypto currency code

        :return: The currency of this LinkUtxo.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this LinkUtxo.

        crypto currency code

        :param currency: The currency of this LinkUtxo.
        :type currency: str
        """
        if currency is None:
            raise BadUserInputException("Invalid value for `currency`, must not be `None`")

        self._currency = currency

    @property
    def height(self):
        """Gets the height of this LinkUtxo.

        Height

        :return: The height of this LinkUtxo.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this LinkUtxo.

        Height

        :param height: The height of this LinkUtxo.
        :type height: int
        """
        if height is None:
            raise BadUserInputException("Invalid value for `height`, must not be `None`")
        if height is not None and height < 0:
            raise BadUserInputException("Invalid value for `height`, must be a value greater than or equal to `0`")

        self._height = height

    @property
    def timestamp(self):
        """Gets the timestamp of this LinkUtxo.

        Timestamp in posix seconds format

        :return: The timestamp of this LinkUtxo.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this LinkUtxo.

        Timestamp in posix seconds format

        :param timestamp: The timestamp of this LinkUtxo.
        :type timestamp: int
        """
        if timestamp is None:
            raise BadUserInputException("Invalid value for `timestamp`, must not be `None`")

        self._timestamp = timestamp

    @property
    def input_value(self):
        """Gets the input_value of this LinkUtxo.


        :return: The input_value of this LinkUtxo.
        :rtype: Values
        """
        return self._input_value

    @input_value.setter
    def input_value(self, input_value):
        """Sets the input_value of this LinkUtxo.


        :param input_value: The input_value of this LinkUtxo.
        :type input_value: Values
        """
        if input_value is None:
            raise BadUserInputException("Invalid value for `input_value`, must not be `None`")

        self._input_value = input_value

    @property
    def output_value(self):
        """Gets the output_value of this LinkUtxo.


        :return: The output_value of this LinkUtxo.
        :rtype: Values
        """
        return self._output_value

    @output_value.setter
    def output_value(self, output_value):
        """Sets the output_value of this LinkUtxo.


        :param output_value: The output_value of this LinkUtxo.
        :type output_value: Values
        """
        if output_value is None:
            raise BadUserInputException("Invalid value for `output_value`, must not be `None`")

        self._output_value = output_value
