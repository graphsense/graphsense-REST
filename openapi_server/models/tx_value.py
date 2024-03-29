# coding: utf-8
from gsrest.errors import BadUserInputException
from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.values import Values
from openapi_server import util


class TxValue(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, address: List[str]=None, value: Values=None):
        """TxValue - a model defined in OpenAPI

        :param address: The address of this TxValue.
        :param value: The value of this TxValue.
        """
        self.openapi_types = {
            'address': List[str],
            'value': Values
        }

        self.attribute_map = {
            'address': 'address',
            'value': 'value'
        }

        self._address = address
        self._value = value

    @classmethod
    def from_dict(cls, dikt: dict) -> 'TxValue':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The tx_value of this TxValue.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The TxValue as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'address': self._address,
            'value': self._value }


    @property
    def address(self):
        """Gets the address of this TxValue.


        :return: The address of this TxValue.
        :rtype: List[str]
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this TxValue.


        :param address: The address of this TxValue.
        :type address: List[str]
        """
        if address is None:
            raise BadUserInputException("Invalid value for `address`, must not be `None`")

        self._address = address

    @property
    def value(self):
        """Gets the value of this TxValue.


        :return: The value of this TxValue.
        :rtype: Values
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this TxValue.


        :param value: The value of this TxValue.
        :type value: Values
        """
        if value is None:
            raise BadUserInputException("Invalid value for `value`, must not be `None`")

        self._value = value
