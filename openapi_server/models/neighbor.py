# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.values import Values
from openapi_server import util


class Neighbor(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, balance: Values=None, id: str=None, labels: List[str]=None, no_txs: int=None, node_type: str=None, received: Values=None, value: Values=None):
        """Neighbor - a model defined in OpenAPI

        :param balance: The balance of this Neighbor.
        :param id: The id of this Neighbor.
        :param labels: The labels of this Neighbor.
        :param no_txs: The no_txs of this Neighbor.
        :param node_type: The node_type of this Neighbor.
        :param received: The received of this Neighbor.
        :param value: The value of this Neighbor.
        """
        self.openapi_types = {
            'balance': Values,
            'id': str,
            'labels': List[str],
            'no_txs': int,
            'node_type': str,
            'received': Values,
            'value': Values
        }

        self.attribute_map = {
            'balance': 'balance',
            'id': 'id',
            'labels': 'labels',
            'no_txs': 'no_txs',
            'node_type': 'node_type',
            'received': 'received',
            'value': 'value'
        }

        self._balance = balance
        self._id = id
        self._labels = labels
        self._no_txs = no_txs
        self._node_type = node_type
        self._received = received
        self._value = value

    @classmethod
    def from_dict(cls, dikt: dict) -> 'Neighbor':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The neighbor of this Neighbor.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def balance(self):
        """Gets the balance of this Neighbor.


        :return: The balance of this Neighbor.
        :rtype: Values
        """
        return self._balance

    @balance.setter
    def balance(self, balance):
        """Sets the balance of this Neighbor.


        :param balance: The balance of this Neighbor.
        :type balance: Values
        """
        if balance is None:
            raise ValueError("Invalid value for `balance`, must not be `None`")

        self._balance = balance

    @property
    def id(self):
        """Gets the id of this Neighbor.

        address or entity id

        :return: The id of this Neighbor.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Neighbor.

        address or entity id

        :param id: The id of this Neighbor.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def labels(self):
        """Gets the labels of this Neighbor.

        labels

        :return: The labels of this Neighbor.
        :rtype: List[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this Neighbor.

        labels

        :param labels: The labels of this Neighbor.
        :type labels: List[str]
        """

        self._labels = labels

    @property
    def no_txs(self):
        """Gets the no_txs of this Neighbor.

        number of transactions

        :return: The no_txs of this Neighbor.
        :rtype: int
        """
        return self._no_txs

    @no_txs.setter
    def no_txs(self, no_txs):
        """Sets the no_txs of this Neighbor.

        number of transactions

        :param no_txs: The no_txs of this Neighbor.
        :type no_txs: int
        """
        if no_txs is None:
            raise ValueError("Invalid value for `no_txs`, must not be `None`")

        self._no_txs = no_txs

    @property
    def node_type(self):
        """Gets the node_type of this Neighbor.

        address or entity

        :return: The node_type of this Neighbor.
        :rtype: str
        """
        return self._node_type

    @node_type.setter
    def node_type(self, node_type):
        """Sets the node_type of this Neighbor.

        address or entity

        :param node_type: The node_type of this Neighbor.
        :type node_type: str
        """
        allowed_values = ["address", "entity"]  # noqa: E501
        if node_type not in allowed_values:
            raise ValueError(
                "Invalid value for `node_type` ({0}), must be one of {1}"
                .format(node_type, allowed_values)
            )

        self._node_type = node_type

    @property
    def received(self):
        """Gets the received of this Neighbor.


        :return: The received of this Neighbor.
        :rtype: Values
        """
        return self._received

    @received.setter
    def received(self, received):
        """Sets the received of this Neighbor.


        :param received: The received of this Neighbor.
        :type received: Values
        """
        if received is None:
            raise ValueError("Invalid value for `received`, must not be `None`")

        self._received = received

    @property
    def value(self):
        """Gets the value of this Neighbor.


        :return: The value of this Neighbor.
        :rtype: Values
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this Neighbor.


        :param value: The value of this Neighbor.
        :type value: Values
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")

        self._value = value
