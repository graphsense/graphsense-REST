# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.values import Values
from openapi_server import util

from openapi_server.models.values import Values  # noqa: E501

class Neighbor(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, balance=None, id=None, labels=None, no_txs=None, node_type=None, received=None, value=None):  # noqa: E501
        """Neighbor - a model defined in OpenAPI

        :param balance: The balance of this Neighbor.  # noqa: E501
        :type balance: Values
        :param id: The id of this Neighbor.  # noqa: E501
        :type id: str
        :param labels: The labels of this Neighbor.  # noqa: E501
        :type labels: List[str]
        :param no_txs: The no_txs of this Neighbor.  # noqa: E501
        :type no_txs: int
        :param node_type: The node_type of this Neighbor.  # noqa: E501
        :type node_type: str
        :param received: The received of this Neighbor.  # noqa: E501
        :type received: Values
        :param value: The value of this Neighbor.  # noqa: E501
        :type value: Values
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

        #if balance is None:
            #raise ValueError("Invalid value for `balance`, must not be `None`")  # noqa: E501
        self._balance = balance
        #if id is None:
            #raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        self._id = id
        self._labels = labels
        #if no_txs is None:
            #raise ValueError("Invalid value for `no_txs`, must not be `None`")  # noqa: E501
        self._no_txs = no_txs
        #if node_type is None:
            #raise ValueError("Invalid value for `node_type`, must not be `None`")  # noqa: E501
        self._node_type = node_type
        #if received is None:
            #raise ValueError("Invalid value for `received`, must not be `None`")  # noqa: E501
        self._received = received
        #if value is None:
            #raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501
        self._value = value

    @classmethod
    def from_dict(cls, dikt) -> 'Neighbor':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The neighbor of this Neighbor.  # noqa: E501
        :rtype: Neighbor
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The Neighbor as a dict
        :rtype: dict
        """
        return { 'balance': self._balance,
            'id': self._id,
            'labels': self._labels,
            'no_txs': self._no_txs,
            'node_type': self._node_type,
            'received': self._received,
            'value': self._value }


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
            raise ValueError("Invalid value for `balance`, must not be `None`")  # noqa: E501

        self._balance = balance

    @property
    def id(self):
        """Gets the id of this Neighbor.

        address or entity id  # noqa: E501

        :return: The id of this Neighbor.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Neighbor.

        address or entity id  # noqa: E501

        :param id: The id of this Neighbor.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def labels(self):
        """Gets the labels of this Neighbor.

        labels  # noqa: E501

        :return: The labels of this Neighbor.
        :rtype: List[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this Neighbor.

        labels  # noqa: E501

        :param labels: The labels of this Neighbor.
        :type labels: List[str]
        """

        self._labels = labels

    @property
    def no_txs(self):
        """Gets the no_txs of this Neighbor.

        number of transactions  # noqa: E501

        :return: The no_txs of this Neighbor.
        :rtype: int
        """
        return self._no_txs

    @no_txs.setter
    def no_txs(self, no_txs):
        """Sets the no_txs of this Neighbor.

        number of transactions  # noqa: E501

        :param no_txs: The no_txs of this Neighbor.
        :type no_txs: int
        """
        if no_txs is None:
            raise ValueError("Invalid value for `no_txs`, must not be `None`")  # noqa: E501

        self._no_txs = no_txs

    @property
    def node_type(self):
        """Gets the node_type of this Neighbor.

        address or entity  # noqa: E501

        :return: The node_type of this Neighbor.
        :rtype: str
        """
        return self._node_type

    @node_type.setter
    def node_type(self, node_type):
        """Sets the node_type of this Neighbor.

        address or entity  # noqa: E501

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
            raise ValueError("Invalid value for `received`, must not be `None`")  # noqa: E501

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
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value
