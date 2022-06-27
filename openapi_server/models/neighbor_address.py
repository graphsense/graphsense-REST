# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.address import Address
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.values import Values
from openapi_server import util


class NeighborAddress(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, address: Address=None, labels: List[str]=None, no_txs: int=None, value: Values=None):
        """NeighborAddress - a model defined in OpenAPI

        :param address: The address of this NeighborAddress.
        :param labels: The labels of this NeighborAddress.
        :param no_txs: The no_txs of this NeighborAddress.
        :param value: The value of this NeighborAddress.
        """
        self.openapi_types = {
            'address': Address,
            'labels': List[str],
            'no_txs': int,
            'value': Values
        }

        self.attribute_map = {
            'address': 'address',
            'labels': 'labels',
            'no_txs': 'no_txs',
            'value': 'value'
        }

        self._address = address
        self._labels = labels
        self._no_txs = no_txs
        self._value = value

    @classmethod
    def from_dict(cls, dikt: dict) -> 'NeighborAddress':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The neighbor_address of this NeighborAddress.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The NeighborAddress as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'address': self._address,
            'labels': self._labels,
            'no_txs': self._no_txs,
            'value': self._value }


    @property
    def address(self):
        """Gets the address of this NeighborAddress.


        :return: The address of this NeighborAddress.
        :rtype: Address
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this NeighborAddress.


        :param address: The address of this NeighborAddress.
        :type address: Address
        """
        if address is None:
            raise ValueError("Invalid value for `address`, must not be `None`")

        self._address = address

    @property
    def labels(self):
        """Gets the labels of this NeighborAddress.

        The neighbor's tag labels

        :return: The labels of this NeighborAddress.
        :rtype: List[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this NeighborAddress.

        The neighbor's tag labels

        :param labels: The labels of this NeighborAddress.
        :type labels: List[str]
        """

        self._labels = labels

    @property
    def no_txs(self):
        """Gets the no_txs of this NeighborAddress.

        number of transactions

        :return: The no_txs of this NeighborAddress.
        :rtype: int
        """
        return self._no_txs

    @no_txs.setter
    def no_txs(self, no_txs):
        """Sets the no_txs of this NeighborAddress.

        number of transactions

        :param no_txs: The no_txs of this NeighborAddress.
        :type no_txs: int
        """
        if no_txs is None:
            raise ValueError("Invalid value for `no_txs`, must not be `None`")

        self._no_txs = no_txs

    @property
    def value(self):
        """Gets the value of this NeighborAddress.


        :return: The value of this NeighborAddress.
        :rtype: Values
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this NeighborAddress.


        :param value: The value of this NeighborAddress.
        :type value: Values
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")

        self._value = value
