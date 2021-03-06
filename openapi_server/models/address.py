# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.values import Values
from openapi_server import util

from openapi_server.models.tx_summary import TxSummary  # noqa: E501
from openapi_server.models.values import Values  # noqa: E501

class Address(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, address=None, balance=None, first_tx=None, last_tx=None, in_degree=None, out_degree=None, no_incoming_txs=None, no_outgoing_txs=None, total_received=None, total_spent=None):  # noqa: E501
        """Address - a model defined in OpenAPI

        :param address: The address of this Address.  # noqa: E501
        :type address: str
        :param balance: The balance of this Address.  # noqa: E501
        :type balance: Values
        :param first_tx: The first_tx of this Address.  # noqa: E501
        :type first_tx: TxSummary
        :param last_tx: The last_tx of this Address.  # noqa: E501
        :type last_tx: TxSummary
        :param in_degree: The in_degree of this Address.  # noqa: E501
        :type in_degree: int
        :param out_degree: The out_degree of this Address.  # noqa: E501
        :type out_degree: int
        :param no_incoming_txs: The no_incoming_txs of this Address.  # noqa: E501
        :type no_incoming_txs: int
        :param no_outgoing_txs: The no_outgoing_txs of this Address.  # noqa: E501
        :type no_outgoing_txs: int
        :param total_received: The total_received of this Address.  # noqa: E501
        :type total_received: Values
        :param total_spent: The total_spent of this Address.  # noqa: E501
        :type total_spent: Values
        """
        self.openapi_types = {
            'address': str,
            'balance': Values,
            'first_tx': TxSummary,
            'last_tx': TxSummary,
            'in_degree': int,
            'out_degree': int,
            'no_incoming_txs': int,
            'no_outgoing_txs': int,
            'total_received': Values,
            'total_spent': Values
        }

        self.attribute_map = {
            'address': 'address',
            'balance': 'balance',
            'first_tx': 'first_tx',
            'last_tx': 'last_tx',
            'in_degree': 'in_degree',
            'out_degree': 'out_degree',
            'no_incoming_txs': 'no_incoming_txs',
            'no_outgoing_txs': 'no_outgoing_txs',
            'total_received': 'total_received',
            'total_spent': 'total_spent'
        }

        if address is None:
            raise ValueError("Invalid value for `address`, must not be `None`")  # noqa: E501
        self._address = address
        if balance is None:
            raise ValueError("Invalid value for `balance`, must not be `None`")  # noqa: E501
        self._balance = balance
        if first_tx is None:
            raise ValueError("Invalid value for `first_tx`, must not be `None`")  # noqa: E501
        self._first_tx = first_tx
        if last_tx is None:
            raise ValueError("Invalid value for `last_tx`, must not be `None`")  # noqa: E501
        self._last_tx = last_tx
        if in_degree is None:
            raise ValueError("Invalid value for `in_degree`, must not be `None`")  # noqa: E501
        self._in_degree = in_degree
        if out_degree is None:
            raise ValueError("Invalid value for `out_degree`, must not be `None`")  # noqa: E501
        self._out_degree = out_degree
        if no_incoming_txs is None:
            raise ValueError("Invalid value for `no_incoming_txs`, must not be `None`")  # noqa: E501
        self._no_incoming_txs = no_incoming_txs
        if no_outgoing_txs is None:
            raise ValueError("Invalid value for `no_outgoing_txs`, must not be `None`")  # noqa: E501
        self._no_outgoing_txs = no_outgoing_txs
        if total_received is None:
            raise ValueError("Invalid value for `total_received`, must not be `None`")  # noqa: E501
        self._total_received = total_received
        if total_spent is None:
            raise ValueError("Invalid value for `total_spent`, must not be `None`")  # noqa: E501
        self._total_spent = total_spent

    @classmethod
    def from_dict(cls, dikt) -> 'Address':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The address of this Address.  # noqa: E501
        :rtype: Address
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The Address as a dict
        :rtype: dict
        """
        return { 'address': self._address,
            'balance': self._balance,
            'first_tx': self._first_tx,
            'last_tx': self._last_tx,
            'in_degree': self._in_degree,
            'out_degree': self._out_degree,
            'no_incoming_txs': self._no_incoming_txs,
            'no_outgoing_txs': self._no_outgoing_txs,
            'total_received': self._total_received,
            'total_spent': self._total_spent }


    @property
    def address(self):
        """Gets the address of this Address.

        Address  # noqa: E501

        :return: The address of this Address.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this Address.

        Address  # noqa: E501

        :param address: The address of this Address.
        :type address: str
        """
        if address is None:
            raise ValueError("Invalid value for `address`, must not be `None`")  # noqa: E501

        self._address = address

    @property
    def balance(self):
        """Gets the balance of this Address.


        :return: The balance of this Address.
        :rtype: Values
        """
        return self._balance

    @balance.setter
    def balance(self, balance):
        """Sets the balance of this Address.


        :param balance: The balance of this Address.
        :type balance: Values
        """
        if balance is None:
            raise ValueError("Invalid value for `balance`, must not be `None`")  # noqa: E501

        self._balance = balance

    @property
    def first_tx(self):
        """Gets the first_tx of this Address.


        :return: The first_tx of this Address.
        :rtype: TxSummary
        """
        return self._first_tx

    @first_tx.setter
    def first_tx(self, first_tx):
        """Sets the first_tx of this Address.


        :param first_tx: The first_tx of this Address.
        :type first_tx: TxSummary
        """
        if first_tx is None:
            raise ValueError("Invalid value for `first_tx`, must not be `None`")  # noqa: E501

        self._first_tx = first_tx

    @property
    def last_tx(self):
        """Gets the last_tx of this Address.


        :return: The last_tx of this Address.
        :rtype: TxSummary
        """
        return self._last_tx

    @last_tx.setter
    def last_tx(self, last_tx):
        """Sets the last_tx of this Address.


        :param last_tx: The last_tx of this Address.
        :type last_tx: TxSummary
        """
        if last_tx is None:
            raise ValueError("Invalid value for `last_tx`, must not be `None`")  # noqa: E501

        self._last_tx = last_tx

    @property
    def in_degree(self):
        """Gets the in_degree of this Address.


        :return: The in_degree of this Address.
        :rtype: int
        """
        return self._in_degree

    @in_degree.setter
    def in_degree(self, in_degree):
        """Sets the in_degree of this Address.


        :param in_degree: The in_degree of this Address.
        :type in_degree: int
        """
        if in_degree is None:
            raise ValueError("Invalid value for `in_degree`, must not be `None`")  # noqa: E501

        self._in_degree = in_degree

    @property
    def out_degree(self):
        """Gets the out_degree of this Address.


        :return: The out_degree of this Address.
        :rtype: int
        """
        return self._out_degree

    @out_degree.setter
    def out_degree(self, out_degree):
        """Sets the out_degree of this Address.


        :param out_degree: The out_degree of this Address.
        :type out_degree: int
        """
        if out_degree is None:
            raise ValueError("Invalid value for `out_degree`, must not be `None`")  # noqa: E501

        self._out_degree = out_degree

    @property
    def no_incoming_txs(self):
        """Gets the no_incoming_txs of this Address.


        :return: The no_incoming_txs of this Address.
        :rtype: int
        """
        return self._no_incoming_txs

    @no_incoming_txs.setter
    def no_incoming_txs(self, no_incoming_txs):
        """Sets the no_incoming_txs of this Address.


        :param no_incoming_txs: The no_incoming_txs of this Address.
        :type no_incoming_txs: int
        """
        if no_incoming_txs is None:
            raise ValueError("Invalid value for `no_incoming_txs`, must not be `None`")  # noqa: E501

        self._no_incoming_txs = no_incoming_txs

    @property
    def no_outgoing_txs(self):
        """Gets the no_outgoing_txs of this Address.


        :return: The no_outgoing_txs of this Address.
        :rtype: int
        """
        return self._no_outgoing_txs

    @no_outgoing_txs.setter
    def no_outgoing_txs(self, no_outgoing_txs):
        """Sets the no_outgoing_txs of this Address.


        :param no_outgoing_txs: The no_outgoing_txs of this Address.
        :type no_outgoing_txs: int
        """
        if no_outgoing_txs is None:
            raise ValueError("Invalid value for `no_outgoing_txs`, must not be `None`")  # noqa: E501

        self._no_outgoing_txs = no_outgoing_txs

    @property
    def total_received(self):
        """Gets the total_received of this Address.


        :return: The total_received of this Address.
        :rtype: Values
        """
        return self._total_received

    @total_received.setter
    def total_received(self, total_received):
        """Sets the total_received of this Address.


        :param total_received: The total_received of this Address.
        :type total_received: Values
        """
        if total_received is None:
            raise ValueError("Invalid value for `total_received`, must not be `None`")  # noqa: E501

        self._total_received = total_received

    @property
    def total_spent(self):
        """Gets the total_spent of this Address.


        :return: The total_spent of this Address.
        :rtype: Values
        """
        return self._total_spent

    @total_spent.setter
    def total_spent(self, total_spent):
        """Sets the total_spent of this Address.


        :param total_spent: The total_spent of this Address.
        :type total_spent: Values
        """
        if total_spent is None:
            raise ValueError("Invalid value for `total_spent`, must not be `None`")  # noqa: E501

        self._total_spent = total_spent
