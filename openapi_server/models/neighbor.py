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

    def __init__(self, id=None, node_type=None, labels=None, balance=None, received=None, estimated_value=None, no_txs=None):  # noqa: E501
        """Neighbor - a model defined in OpenAPI

        :param id: The id of this Neighbor.  # noqa: E501
        :type id: str
        :param node_type: The node_type of this Neighbor.  # noqa: E501
        :type node_type: str
        :param labels: The labels of this Neighbor.  # noqa: E501
        :type labels: List[str]
        :param balance: The balance of this Neighbor.  # noqa: E501
        :type balance: Values
        :param received: The received of this Neighbor.  # noqa: E501
        :type received: Values
        :param estimated_value: The estimated_value of this Neighbor.  # noqa: E501
        :type estimated_value: Values
        :param no_txs: The no_txs of this Neighbor.  # noqa: E501
        :type no_txs: int
        """
        self.openapi_types = {
            'id': str,
            'node_type': str,
            'labels': List[str],
            'balance': Values,
            'received': Values,
            'estimated_value': Values,
            'no_txs': int
        }

        self.attribute_map = {
            'id': 'id',
            'node_type': 'node_type',
            'labels': 'labels',
            'balance': 'balance',
            'received': 'received',
            'estimated_value': 'estimated_value',
            'no_txs': 'no_txs'
        }

        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        self._id = id
        if node_type is None:
            raise ValueError("Invalid value for `node_type`, must not be `None`")  # noqa: E501
        self._node_type = node_type
        if labels is None:
            raise ValueError("Invalid value for `labels`, must not be `None`")  # noqa: E501
        self._labels = labels
        if balance is None:
            raise ValueError("Invalid value for `balance`, must not be `None`")  # noqa: E501
        self._balance = balance
        if received is None:
            raise ValueError("Invalid value for `received`, must not be `None`")  # noqa: E501
        self._received = received
        if estimated_value is None:
            raise ValueError("Invalid value for `estimated_value`, must not be `None`")  # noqa: E501
        self._estimated_value = estimated_value
        if no_txs is None:
            raise ValueError("Invalid value for `no_txs`, must not be `None`")  # noqa: E501
        self._no_txs = no_txs

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
        return { 'id': self._id,
            'node_type': self._node_type,
            'labels': self._labels,
            'balance': self._balance,
            'received': self._received,
            'estimated_value': self._estimated_value,
            'no_txs': self._no_txs }


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
        if labels is None:
            raise ValueError("Invalid value for `labels`, must not be `None`")  # noqa: E501

        self._labels = labels

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
    def estimated_value(self):
        """Gets the estimated_value of this Neighbor.


        :return: The estimated_value of this Neighbor.
        :rtype: Values
        """
        return self._estimated_value

    @estimated_value.setter
    def estimated_value(self, estimated_value):
        """Sets the estimated_value of this Neighbor.


        :param estimated_value: The estimated_value of this Neighbor.
        :type estimated_value: Values
        """
        if estimated_value is None:
            raise ValueError("Invalid value for `estimated_value`, must not be `None`")  # noqa: E501

        self._estimated_value = estimated_value

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
