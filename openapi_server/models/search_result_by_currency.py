# coding: utf-8
from gsrest.errors import BadUserInputException
from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class SearchResultByCurrency(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, addresses: List[str]=None, currency: str=None, txs: List[str]=None):
        """SearchResultByCurrency - a model defined in OpenAPI

        :param addresses: The addresses of this SearchResultByCurrency.
        :param currency: The currency of this SearchResultByCurrency.
        :param txs: The txs of this SearchResultByCurrency.
        """
        self.openapi_types = {
            'addresses': List[str],
            'currency': str,
            'txs': List[str]
        }

        self.attribute_map = {
            'addresses': 'addresses',
            'currency': 'currency',
            'txs': 'txs'
        }

        self._addresses = addresses
        self._currency = currency
        self._txs = txs

    @classmethod
    def from_dict(cls, dikt: dict) -> 'SearchResultByCurrency':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The search_result_by_currency of this SearchResultByCurrency.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The SearchResultByCurrency as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'addresses': self._addresses,
            'currency': self._currency,
            'txs': self._txs }


    @property
    def addresses(self):
        """Gets the addresses of this SearchResultByCurrency.

        The list of found addresses

        :return: The addresses of this SearchResultByCurrency.
        :rtype: List[str]
        """
        return self._addresses

    @addresses.setter
    def addresses(self, addresses):
        """Sets the addresses of this SearchResultByCurrency.

        The list of found addresses

        :param addresses: The addresses of this SearchResultByCurrency.
        :type addresses: List[str]
        """
        if addresses is None:
            raise BadUserInputException("Invalid value for `addresses`, must not be `None`")

        self._addresses = addresses

    @property
    def currency(self):
        """Gets the currency of this SearchResultByCurrency.

        crypto currency code

        :return: The currency of this SearchResultByCurrency.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this SearchResultByCurrency.

        crypto currency code

        :param currency: The currency of this SearchResultByCurrency.
        :type currency: str
        """
        if currency is None:
            raise BadUserInputException("Invalid value for `currency`, must not be `None`")

        self._currency = currency

    @property
    def txs(self):
        """Gets the txs of this SearchResultByCurrency.

        The list of found transaction ids

        :return: The txs of this SearchResultByCurrency.
        :rtype: List[str]
        """
        return self._txs

    @txs.setter
    def txs(self, txs):
        """Sets the txs of this SearchResultByCurrency.

        The list of found transaction ids

        :param txs: The txs of this SearchResultByCurrency.
        :type txs: List[str]
        """
        if txs is None:
            raise BadUserInputException("Invalid value for `txs`, must not be `None`")

        self._txs = txs
