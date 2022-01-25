# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class CurrencyStats(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name: str=None, no_address_relations: int=None, no_addresses: int=None, no_blocks: int=None, no_entities: int=None, no_labels: int=None, no_txs: int=None, timestamp: int=None):
        """CurrencyStats - a model defined in OpenAPI

        :param name: The name of this CurrencyStats.
        :param no_address_relations: The no_address_relations of this CurrencyStats.
        :param no_addresses: The no_addresses of this CurrencyStats.
        :param no_blocks: The no_blocks of this CurrencyStats.
        :param no_entities: The no_entities of this CurrencyStats.
        :param no_labels: The no_labels of this CurrencyStats.
        :param no_txs: The no_txs of this CurrencyStats.
        :param timestamp: The timestamp of this CurrencyStats.
        """
        self.openapi_types = {
            'name': str,
            'no_address_relations': int,
            'no_addresses': int,
            'no_blocks': int,
            'no_entities': int,
            'no_labels': int,
            'no_txs': int,
            'timestamp': int
        }

        self.attribute_map = {
            'name': 'name',
            'no_address_relations': 'no_address_relations',
            'no_addresses': 'no_addresses',
            'no_blocks': 'no_blocks',
            'no_entities': 'no_entities',
            'no_labels': 'no_labels',
            'no_txs': 'no_txs',
            'timestamp': 'timestamp'
        }

        self._name = name
        self._no_address_relations = no_address_relations
        self._no_addresses = no_addresses
        self._no_blocks = no_blocks
        self._no_entities = no_entities
        self._no_labels = no_labels
        self._no_txs = no_txs
        self._timestamp = timestamp

    @classmethod
    def from_dict(cls, dikt: dict) -> 'CurrencyStats':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The currency_stats of this CurrencyStats.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The CurrencyStats as a dict
        :rtype: dict
        """
        return { 'name': self._name,
            'no_address_relations': self._no_address_relations,
            'no_addresses': self._no_addresses,
            'no_blocks': self._no_blocks,
            'no_entities': self._no_entities,
            'no_labels': self._no_labels,
            'no_txs': self._no_txs,
            'timestamp': self._timestamp }


    @property
    def name(self):
        """Gets the name of this CurrencyStats.


        :return: The name of this CurrencyStats.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CurrencyStats.


        :param name: The name of this CurrencyStats.
        :type name: str
        """

        self._name = name

    @property
    def no_address_relations(self):
        """Gets the no_address_relations of this CurrencyStats.


        :return: The no_address_relations of this CurrencyStats.
        :rtype: int
        """
        return self._no_address_relations

    @no_address_relations.setter
    def no_address_relations(self, no_address_relations):
        """Sets the no_address_relations of this CurrencyStats.


        :param no_address_relations: The no_address_relations of this CurrencyStats.
        :type no_address_relations: int
        """

        self._no_address_relations = no_address_relations

    @property
    def no_addresses(self):
        """Gets the no_addresses of this CurrencyStats.


        :return: The no_addresses of this CurrencyStats.
        :rtype: int
        """
        return self._no_addresses

    @no_addresses.setter
    def no_addresses(self, no_addresses):
        """Sets the no_addresses of this CurrencyStats.


        :param no_addresses: The no_addresses of this CurrencyStats.
        :type no_addresses: int
        """

        self._no_addresses = no_addresses

    @property
    def no_blocks(self):
        """Gets the no_blocks of this CurrencyStats.


        :return: The no_blocks of this CurrencyStats.
        :rtype: int
        """
        return self._no_blocks

    @no_blocks.setter
    def no_blocks(self, no_blocks):
        """Sets the no_blocks of this CurrencyStats.


        :param no_blocks: The no_blocks of this CurrencyStats.
        :type no_blocks: int
        """

        self._no_blocks = no_blocks

    @property
    def no_entities(self):
        """Gets the no_entities of this CurrencyStats.


        :return: The no_entities of this CurrencyStats.
        :rtype: int
        """
        return self._no_entities

    @no_entities.setter
    def no_entities(self, no_entities):
        """Sets the no_entities of this CurrencyStats.


        :param no_entities: The no_entities of this CurrencyStats.
        :type no_entities: int
        """

        self._no_entities = no_entities

    @property
    def no_labels(self):
        """Gets the no_labels of this CurrencyStats.


        :return: The no_labels of this CurrencyStats.
        :rtype: int
        """
        return self._no_labels

    @no_labels.setter
    def no_labels(self, no_labels):
        """Sets the no_labels of this CurrencyStats.


        :param no_labels: The no_labels of this CurrencyStats.
        :type no_labels: int
        """

        self._no_labels = no_labels

    @property
    def no_txs(self):
        """Gets the no_txs of this CurrencyStats.

        number of transactions

        :return: The no_txs of this CurrencyStats.
        :rtype: int
        """
        return self._no_txs

    @no_txs.setter
    def no_txs(self, no_txs):
        """Sets the no_txs of this CurrencyStats.

        number of transactions

        :param no_txs: The no_txs of this CurrencyStats.
        :type no_txs: int
        """

        self._no_txs = no_txs

    @property
    def timestamp(self):
        """Gets the timestamp of this CurrencyStats.

        Timestamp

        :return: The timestamp of this CurrencyStats.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this CurrencyStats.

        Timestamp

        :param timestamp: The timestamp of this CurrencyStats.
        :type timestamp: int
        """

        self._timestamp = timestamp
