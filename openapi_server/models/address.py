# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.values import Values
from openapi_server import util


class Address(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, address: str=None, balance: Values=None, currency: str=None, entity: int=None, first_tx: TxSummary=None, in_degree: int=None, last_tx: TxSummary=None, no_incoming_txs: int=None, no_outgoing_txs: int=None, out_degree: int=None, status: str=None, total_received: Values=None, total_spent: Values=None):
        """Address - a model defined in OpenAPI

        :param address: The address of this Address.
        :param balance: The balance of this Address.
        :param currency: The currency of this Address.
        :param entity: The entity of this Address.
        :param first_tx: The first_tx of this Address.
        :param in_degree: The in_degree of this Address.
        :param last_tx: The last_tx of this Address.
        :param no_incoming_txs: The no_incoming_txs of this Address.
        :param no_outgoing_txs: The no_outgoing_txs of this Address.
        :param out_degree: The out_degree of this Address.
        :param status: The status of this Address.
        :param total_received: The total_received of this Address.
        :param total_spent: The total_spent of this Address.
        """
        self.openapi_types = {
            'address': str,
            'balance': Values,
            'currency': str,
            'entity': int,
            'first_tx': TxSummary,
            'in_degree': int,
            'last_tx': TxSummary,
            'no_incoming_txs': int,
            'no_outgoing_txs': int,
            'out_degree': int,
            'status': str,
            'total_received': Values,
            'total_spent': Values
        }

        self.attribute_map = {
            'address': 'address',
            'balance': 'balance',
            'currency': 'currency',
            'entity': 'entity',
            'first_tx': 'first_tx',
            'in_degree': 'in_degree',
            'last_tx': 'last_tx',
            'no_incoming_txs': 'no_incoming_txs',
            'no_outgoing_txs': 'no_outgoing_txs',
            'out_degree': 'out_degree',
            'status': 'status',
            'total_received': 'total_received',
            'total_spent': 'total_spent'
        }

        self._address = address
        self._balance = balance
        self._currency = currency
        self._entity = entity
        self._first_tx = first_tx
        self._in_degree = in_degree
        self._last_tx = last_tx
        self._no_incoming_txs = no_incoming_txs
        self._no_outgoing_txs = no_outgoing_txs
        self._out_degree = out_degree
        self._status = status
        self._total_received = total_received
        self._total_spent = total_spent

    @classmethod
    def from_dict(cls, dikt: dict) -> 'Address':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The address of this Address.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The Address as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'address': self._address,
            'balance': self._balance,
            'currency': self._currency,
            'entity': self._entity,
            'first_tx': self._first_tx,
            'in_degree': self._in_degree,
            'last_tx': self._last_tx,
            'no_incoming_txs': self._no_incoming_txs,
            'no_outgoing_txs': self._no_outgoing_txs,
            'out_degree': self._out_degree,
            'status': self._status,
            'total_received': self._total_received,
            'total_spent': self._total_spent }


    @property
    def address(self):
        """Gets the address of this Address.

        Address

        :return: The address of this Address.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this Address.

        Address

        :param address: The address of this Address.
        :type address: str
        """
        if address is None:
            raise ValueError("Invalid value for `address`, must not be `None`")

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
            raise ValueError("Invalid value for `balance`, must not be `None`")

        self._balance = balance

    @property
    def currency(self):
        """Gets the currency of this Address.

        crypto currency code

        :return: The currency of this Address.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this Address.

        crypto currency code

        :param currency: The currency of this Address.
        :type currency: str
        """
        if currency is None:
            raise ValueError("Invalid value for `currency`, must not be `None`")

        self._currency = currency

    @property
    def entity(self):
        """Gets the entity of this Address.

        Entity id

        :return: The entity of this Address.
        :rtype: int
        """
        return self._entity

    @entity.setter
    def entity(self, entity):
        """Sets the entity of this Address.

        Entity id

        :param entity: The entity of this Address.
        :type entity: int
        """
        if entity is None:
            raise ValueError("Invalid value for `entity`, must not be `None`")

        self._entity = entity

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
            raise ValueError("Invalid value for `first_tx`, must not be `None`")

        self._first_tx = first_tx

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
            raise ValueError("Invalid value for `in_degree`, must not be `None`")

        self._in_degree = in_degree

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
            raise ValueError("Invalid value for `last_tx`, must not be `None`")

        self._last_tx = last_tx

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
            raise ValueError("Invalid value for `no_incoming_txs`, must not be `None`")

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
            raise ValueError("Invalid value for `no_outgoing_txs`, must not be `None`")

        self._no_outgoing_txs = no_outgoing_txs

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
            raise ValueError("Invalid value for `out_degree`, must not be `None`")

        self._out_degree = out_degree

    @property
    def status(self):
        """Gets the status of this Address.


        :return: The status of this Address.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Address.


        :param status: The status of this Address.
        :type status: str
        """
        allowed_values = ["clean", "dirty", "new"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

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
            raise ValueError("Invalid value for `total_received`, must not be `None`")

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
            raise ValueError("Invalid value for `total_spent`, must not be `None`")

        self._total_spent = total_spent
