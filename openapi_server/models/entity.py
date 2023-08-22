# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.labeled_item_ref import LabeledItemRef
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.values import Values
from openapi_server import util


class Entity(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, currency: str=None, entity: int=None, root_address: str=None, balance: Values=None, token_balances: Dict[str, Values]=None, first_tx: TxSummary=None, last_tx: TxSummary=None, in_degree: int=None, out_degree: int=None, no_addresses: int=None, no_incoming_txs: int=None, no_outgoing_txs: int=None, total_received: Values=None, total_spent: Values=None, total_tokens_received: Dict[str, Values]=None, total_tokens_spent: Dict[str, Values]=None, actors: List[LabeledItemRef]=None, best_address_tag: AddressTag=None, no_address_tags: int=None):
        """Entity - a model defined in OpenAPI

        :param currency: The currency of this Entity.
        :param entity: The entity of this Entity.
        :param root_address: The root_address of this Entity.
        :param balance: The balance of this Entity.
        :param token_balances: The token_balances of this Entity.
        :param first_tx: The first_tx of this Entity.
        :param last_tx: The last_tx of this Entity.
        :param in_degree: The in_degree of this Entity.
        :param out_degree: The out_degree of this Entity.
        :param no_addresses: The no_addresses of this Entity.
        :param no_incoming_txs: The no_incoming_txs of this Entity.
        :param no_outgoing_txs: The no_outgoing_txs of this Entity.
        :param total_received: The total_received of this Entity.
        :param total_spent: The total_spent of this Entity.
        :param total_tokens_received: The total_tokens_received of this Entity.
        :param total_tokens_spent: The total_tokens_spent of this Entity.
        :param actors: The actors of this Entity.
        :param best_address_tag: The best_address_tag of this Entity.
        :param no_address_tags: The no_address_tags of this Entity.
        """
        self.openapi_types = {
            'currency': str,
            'entity': int,
            'root_address': str,
            'balance': Values,
            'token_balances': Dict[str, Values],
            'first_tx': TxSummary,
            'last_tx': TxSummary,
            'in_degree': int,
            'out_degree': int,
            'no_addresses': int,
            'no_incoming_txs': int,
            'no_outgoing_txs': int,
            'total_received': Values,
            'total_spent': Values,
            'total_tokens_received': Dict[str, Values],
            'total_tokens_spent': Dict[str, Values],
            'actors': List[LabeledItemRef],
            'best_address_tag': AddressTag,
            'no_address_tags': int
        }

        self.attribute_map = {
            'currency': 'currency',
            'entity': 'entity',
            'root_address': 'root_address',
            'balance': 'balance',
            'token_balances': 'token_balances',
            'first_tx': 'first_tx',
            'last_tx': 'last_tx',
            'in_degree': 'in_degree',
            'out_degree': 'out_degree',
            'no_addresses': 'no_addresses',
            'no_incoming_txs': 'no_incoming_txs',
            'no_outgoing_txs': 'no_outgoing_txs',
            'total_received': 'total_received',
            'total_spent': 'total_spent',
            'total_tokens_received': 'total_tokens_received',
            'total_tokens_spent': 'total_tokens_spent',
            'actors': 'actors',
            'best_address_tag': 'best_address_tag',
            'no_address_tags': 'no_address_tags'
        }

        self._currency = currency
        self._entity = entity
        self._root_address = root_address
        self._balance = balance
        self._token_balances = token_balances
        self._first_tx = first_tx
        self._last_tx = last_tx
        self._in_degree = in_degree
        self._out_degree = out_degree
        self._no_addresses = no_addresses
        self._no_incoming_txs = no_incoming_txs
        self._no_outgoing_txs = no_outgoing_txs
        self._total_received = total_received
        self._total_spent = total_spent
        self._total_tokens_received = total_tokens_received
        self._total_tokens_spent = total_tokens_spent
        self._actors = actors
        self._best_address_tag = best_address_tag
        self._no_address_tags = no_address_tags

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
        return { 'currency': self._currency,
            'entity': self._entity,
            'root_address': self._root_address,
            'balance': self._balance,
            'token_balances': self._token_balances,
            'first_tx': self._first_tx,
            'last_tx': self._last_tx,
            'in_degree': self._in_degree,
            'out_degree': self._out_degree,
            'no_addresses': self._no_addresses,
            'no_incoming_txs': self._no_incoming_txs,
            'no_outgoing_txs': self._no_outgoing_txs,
            'total_received': self._total_received,
            'total_spent': self._total_spent,
            'total_tokens_received': self._total_tokens_received,
            'total_tokens_spent': self._total_tokens_spent,
            'actors': self._actors,
            'best_address_tag': self._best_address_tag,
            'no_address_tags': self._no_address_tags }


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
    def token_balances(self):
        """Gets the token_balances of this Entity.

        Per token value-flow

        :return: The token_balances of this Entity.
        :rtype: Dict[str, Values]
        """
        return self._token_balances

    @token_balances.setter
    def token_balances(self, token_balances):
        """Sets the token_balances of this Entity.

        Per token value-flow

        :param token_balances: The token_balances of this Entity.
        :type token_balances: Dict[str, Values]
        """

        self._token_balances = token_balances

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

    @property
    def total_tokens_received(self):
        """Gets the total_tokens_received of this Entity.

        Per token value-flow

        :return: The total_tokens_received of this Entity.
        :rtype: Dict[str, Values]
        """
        return self._total_tokens_received

    @total_tokens_received.setter
    def total_tokens_received(self, total_tokens_received):
        """Sets the total_tokens_received of this Entity.

        Per token value-flow

        :param total_tokens_received: The total_tokens_received of this Entity.
        :type total_tokens_received: Dict[str, Values]
        """

        self._total_tokens_received = total_tokens_received

    @property
    def total_tokens_spent(self):
        """Gets the total_tokens_spent of this Entity.

        Per token value-flow

        :return: The total_tokens_spent of this Entity.
        :rtype: Dict[str, Values]
        """
        return self._total_tokens_spent

    @total_tokens_spent.setter
    def total_tokens_spent(self, total_tokens_spent):
        """Sets the total_tokens_spent of this Entity.

        Per token value-flow

        :param total_tokens_spent: The total_tokens_spent of this Entity.
        :type total_tokens_spent: Dict[str, Values]
        """

        self._total_tokens_spent = total_tokens_spent

    @property
    def actors(self):
        """Gets the actors of this Entity.

        The list of matching actors

        :return: The actors of this Entity.
        :rtype: List[LabeledItemRef]
        """
        return self._actors

    @actors.setter
    def actors(self, actors):
        """Sets the actors of this Entity.

        The list of matching actors

        :param actors: The actors of this Entity.
        :type actors: List[LabeledItemRef]
        """

        self._actors = actors

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
    def no_address_tags(self):
        """Gets the no_address_tags of this Entity.

        number of address tags

        :return: The no_address_tags of this Entity.
        :rtype: int
        """
        return self._no_address_tags

    @no_address_tags.setter
    def no_address_tags(self, no_address_tags):
        """Sets the no_address_tags of this Entity.

        number of address tags

        :param no_address_tags: The no_address_tags of this Entity.
        :type no_address_tags: int
        """
        if no_address_tags is None:
            raise ValueError("Invalid value for `no_address_tags`, must not be `None`")

        self._no_address_tags = no_address_tags
