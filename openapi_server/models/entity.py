# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.values import Values
from openapi_server import util


class Entity(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, balance: Values=None, best_address_tag: AddressTag=None, currency: str=None, entity: int=None, first_tx: TxSummary=None, in_degree: int=None, last_tx: TxSummary=None, no_addresses: int=None, no_incoming_txs: int=None, no_outgoing_txs: int=None, out_degree: int=None, root_address: str=None, total_received: Values=None, total_spent: Values=None):
        """Entity - a model defined in OpenAPI

        :param balance: The balance of this Entity.
        :param best_address_tag: The best_address_tag of this Entity.
        :param currency: The currency of this Entity.
        :param entity: The entity of this Entity.
        :param first_tx: The first_tx of this Entity.
        :param in_degree: The in_degree of this Entity.
        :param last_tx: The last_tx of this Entity.
        :param no_addresses: The no_addresses of this Entity.
        :param no_incoming_txs: The no_incoming_txs of this Entity.
        :param no_outgoing_txs: The no_outgoing_txs of this Entity.
        :param out_degree: The out_degree of this Entity.
        :param root_address: The root_address of this Entity.
        :param total_received: The total_received of this Entity.
        :param total_spent: The total_spent of this Entity.
        """
        self.openapi_types = {
            'balance': Values,
            'best_address_tag': AddressTag,
            'currency': str,
            'entity': int,
            'first_tx': TxSummary,
            'in_degree': int,
            'last_tx': TxSummary,
            'no_addresses': int,
            'no_incoming_txs': int,
            'no_outgoing_txs': int,
            'out_degree': int,
            'root_address': str,
            'total_received': Values,
            'total_spent': Values
        }

        self.attribute_map = {
            'balance': 'balance',
            'best_address_tag': 'best_address_tag',
            'currency': 'currency',
            'entity': 'entity',
            'first_tx': 'first_tx',
            'in_degree': 'in_degree',
            'last_tx': 'last_tx',
            'no_addresses': 'no_addresses',
            'no_incoming_txs': 'no_incoming_txs',
            'no_outgoing_txs': 'no_outgoing_txs',
            'out_degree': 'out_degree',
            'root_address': 'root_address',
            'total_received': 'total_received',
            'total_spent': 'total_spent'
        }

        self._balance = balance
        self._best_address_tag = best_address_tag
        self._currency = currency
        self._entity = entity
        self._first_tx = first_tx
        self._in_degree = in_degree
        self._last_tx = last_tx
        self._no_addresses = no_addresses
        self._no_incoming_txs = no_incoming_txs
        self._no_outgoing_txs = no_outgoing_txs
        self._out_degree = out_degree
        self._root_address = root_address
        self._total_received = total_received
        self._total_spent = total_spent

    @classmethod
    def from_dict(cls, dikt: dict) -> 'Entity':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The entity of this Entity.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The Entity as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'balance': self._balance,
            'best_address_tag': self._best_address_tag,
            'currency': self._currency,
            'entity': self._entity,
            'first_tx': self._first_tx,
            'in_degree': self._in_degree,
            'last_tx': self._last_tx,
            'no_addresses': self._no_addresses,
            'no_incoming_txs': self._no_incoming_txs,
            'no_outgoing_txs': self._no_outgoing_txs,
            'out_degree': self._out_degree,
            'root_address': self._root_address,
            'total_received': self._total_received,
            'total_spent': self._total_spent }


    @property
    def balance(self):
        """Gets the balance of this Entity.


        :return: The balance of this Entity.
        :rtype: Values
        """
        return self._balance

    @balance.setter
    def balance(self, balance):
        """Sets the balance of this Entity.


        :param balance: The balance of this Entity.
        :type balance: Values
        """
        if balance is None:
            raise ValueError("Invalid value for `balance`, must not be `None`")

        self._balance = balance

    @property
    def best_address_tag(self):
        """Gets the best_address_tag of this Entity.


        :return: The best_address_tag of this Entity.
        :rtype: AddressTag
        """
        return self._best_address_tag

    @best_address_tag.setter
    def best_address_tag(self, best_address_tag):
        """Sets the best_address_tag of this Entity.


        :param best_address_tag: The best_address_tag of this Entity.
        :type best_address_tag: AddressTag
        """

        self._best_address_tag = best_address_tag

    @property
    def currency(self):
        """Gets the currency of this Entity.

        crypto currency code

        :return: The currency of this Entity.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this Entity.

        crypto currency code

        :param currency: The currency of this Entity.
        :type currency: str
        """
        if currency is None:
            raise ValueError("Invalid value for `currency`, must not be `None`")

        self._currency = currency

    @property
    def entity(self):
        """Gets the entity of this Entity.

        Entity id

        :return: The entity of this Entity.
        :rtype: int
        """
        return self._entity

    @entity.setter
    def entity(self, entity):
        """Sets the entity of this Entity.

        Entity id

        :param entity: The entity of this Entity.
        :type entity: int
        """
        if entity is None:
            raise ValueError("Invalid value for `entity`, must not be `None`")

        self._entity = entity

    @property
    def first_tx(self):
        """Gets the first_tx of this Entity.


        :return: The first_tx of this Entity.
        :rtype: TxSummary
        """
        return self._first_tx

    @first_tx.setter
    def first_tx(self, first_tx):
        """Sets the first_tx of this Entity.


        :param first_tx: The first_tx of this Entity.
        :type first_tx: TxSummary
        """
        if first_tx is None:
            raise ValueError("Invalid value for `first_tx`, must not be `None`")

        self._first_tx = first_tx

    @property
    def in_degree(self):
        """Gets the in_degree of this Entity.


        :return: The in_degree of this Entity.
        :rtype: int
        """
        return self._in_degree

    @in_degree.setter
    def in_degree(self, in_degree):
        """Sets the in_degree of this Entity.


        :param in_degree: The in_degree of this Entity.
        :type in_degree: int
        """
        if in_degree is None:
            raise ValueError("Invalid value for `in_degree`, must not be `None`")

        self._in_degree = in_degree

    @property
    def last_tx(self):
        """Gets the last_tx of this Entity.


        :return: The last_tx of this Entity.
        :rtype: TxSummary
        """
        return self._last_tx

    @last_tx.setter
    def last_tx(self, last_tx):
        """Sets the last_tx of this Entity.


        :param last_tx: The last_tx of this Entity.
        :type last_tx: TxSummary
        """
        if last_tx is None:
            raise ValueError("Invalid value for `last_tx`, must not be `None`")

        self._last_tx = last_tx

    @property
    def no_addresses(self):
        """Gets the no_addresses of this Entity.

        number of contained addresses

        :return: The no_addresses of this Entity.
        :rtype: int
        """
        return self._no_addresses

    @no_addresses.setter
    def no_addresses(self, no_addresses):
        """Sets the no_addresses of this Entity.

        number of contained addresses

        :param no_addresses: The no_addresses of this Entity.
        :type no_addresses: int
        """
        if no_addresses is None:
            raise ValueError("Invalid value for `no_addresses`, must not be `None`")

        self._no_addresses = no_addresses

    @property
    def no_incoming_txs(self):
        """Gets the no_incoming_txs of this Entity.


        :return: The no_incoming_txs of this Entity.
        :rtype: int
        """
        return self._no_incoming_txs

    @no_incoming_txs.setter
    def no_incoming_txs(self, no_incoming_txs):
        """Sets the no_incoming_txs of this Entity.


        :param no_incoming_txs: The no_incoming_txs of this Entity.
        :type no_incoming_txs: int
        """
        if no_incoming_txs is None:
            raise ValueError("Invalid value for `no_incoming_txs`, must not be `None`")

        self._no_incoming_txs = no_incoming_txs

    @property
    def no_outgoing_txs(self):
        """Gets the no_outgoing_txs of this Entity.


        :return: The no_outgoing_txs of this Entity.
        :rtype: int
        """
        return self._no_outgoing_txs

    @no_outgoing_txs.setter
    def no_outgoing_txs(self, no_outgoing_txs):
        """Sets the no_outgoing_txs of this Entity.


        :param no_outgoing_txs: The no_outgoing_txs of this Entity.
        :type no_outgoing_txs: int
        """
        if no_outgoing_txs is None:
            raise ValueError("Invalid value for `no_outgoing_txs`, must not be `None`")

        self._no_outgoing_txs = no_outgoing_txs

    @property
    def out_degree(self):
        """Gets the out_degree of this Entity.


        :return: The out_degree of this Entity.
        :rtype: int
        """
        return self._out_degree

    @out_degree.setter
    def out_degree(self, out_degree):
        """Sets the out_degree of this Entity.


        :param out_degree: The out_degree of this Entity.
        :type out_degree: int
        """
        if out_degree is None:
            raise ValueError("Invalid value for `out_degree`, must not be `None`")

        self._out_degree = out_degree

    @property
    def root_address(self):
        """Gets the root_address of this Entity.

        Address

        :return: The root_address of this Entity.
        :rtype: str
        """
        return self._root_address

    @root_address.setter
    def root_address(self, root_address):
        """Sets the root_address of this Entity.

        Address

        :param root_address: The root_address of this Entity.
        :type root_address: str
        """
        if root_address is None:
            raise ValueError("Invalid value for `root_address`, must not be `None`")

        self._root_address = root_address

    @property
    def total_received(self):
        """Gets the total_received of this Entity.


        :return: The total_received of this Entity.
        :rtype: Values
        """
        return self._total_received

    @total_received.setter
    def total_received(self, total_received):
        """Sets the total_received of this Entity.


        :param total_received: The total_received of this Entity.
        :type total_received: Values
        """
        if total_received is None:
            raise ValueError("Invalid value for `total_received`, must not be `None`")

        self._total_received = total_received

    @property
    def total_spent(self):
        """Gets the total_spent of this Entity.


        :return: The total_spent of this Entity.
        :rtype: Values
        """
        return self._total_spent

    @total_spent.setter
    def total_spent(self, total_spent):
        """Sets the total_spent of this Entity.


        :param total_spent: The total_spent of this Entity.
        :type total_spent: Values
        """
        if total_spent is None:
            raise ValueError("Invalid value for `total_spent`, must not be `None`")

        self._total_spent = total_spent
