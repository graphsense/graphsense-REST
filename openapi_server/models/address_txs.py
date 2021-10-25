# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.address_tx import AddressTx
from openapi_server import util


class AddressTxs(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, address_txs: List[AddressTx]=None, next_page: str=None):
        """AddressTxs - a model defined in OpenAPI

        :param address_txs: The address_txs of this AddressTxs.
        :param next_page: The next_page of this AddressTxs.
        """
        self.openapi_types = {
            'address_txs': List[AddressTx],
            'next_page': str
        }

        self.attribute_map = {
            'address_txs': 'address_txs',
            'next_page': 'next_page'
        }

        self._address_txs = address_txs
        self._next_page = next_page

    @classmethod
    def from_dict(cls, dikt: dict) -> 'AddressTxs':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The address_txs of this AddressTxs.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def address_txs(self):
        """Gets the address_txs of this AddressTxs.


        :return: The address_txs of this AddressTxs.
        :rtype: List[AddressTx]
        """
        return self._address_txs

    @address_txs.setter
    def address_txs(self, address_txs):
        """Sets the address_txs of this AddressTxs.


        :param address_txs: The address_txs of this AddressTxs.
        :type address_txs: List[AddressTx]
        """

        self._address_txs = address_txs

    @property
    def next_page(self):
        """Gets the next_page of this AddressTxs.


        :return: The next_page of this AddressTxs.
        :rtype: str
        """
        return self._next_page

    @next_page.setter
    def next_page(self, next_page):
        """Sets the next_page of this AddressTxs.


        :param next_page: The next_page of this AddressTxs.
        :type next_page: str
        """

        self._next_page = next_page
