# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Block(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, block_hash: str=None, currency: str=None, height: int=None, no_txs: int=None, timestamp: int=None):
        """Block - a model defined in OpenAPI

        :param block_hash: The block_hash of this Block.
        :param currency: The currency of this Block.
        :param height: The height of this Block.
        :param no_txs: The no_txs of this Block.
        :param timestamp: The timestamp of this Block.
        """
        self.openapi_types = {
            'block_hash': str,
            'currency': str,
            'height': int,
            'no_txs': int,
            'timestamp': int
        }

        self.attribute_map = {
            'block_hash': 'block_hash',
            'currency': 'currency',
            'height': 'height',
            'no_txs': 'no_txs',
            'timestamp': 'timestamp'
        }

        self._block_hash = block_hash
        self._currency = currency
        self._height = height
        self._no_txs = no_txs
        self._timestamp = timestamp

    @classmethod
    def from_dict(cls, dikt: dict) -> 'Block':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The block of this Block.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The Block as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'block_hash': self._block_hash,
            'currency': self._currency,
            'height': self._height,
            'no_txs': self._no_txs,
            'timestamp': self._timestamp }


    @property
    def block_hash(self):
        """Gets the block_hash of this Block.


        :return: The block_hash of this Block.
        :rtype: str
        """
        return self._block_hash

    @block_hash.setter
    def block_hash(self, block_hash):
        """Sets the block_hash of this Block.


        :param block_hash: The block_hash of this Block.
        :type block_hash: str
        """
        if block_hash is None:
            raise ValueError("Invalid value for `block_hash`, must not be `None`")

        self._block_hash = block_hash

    @property
    def currency(self):
        """Gets the currency of this Block.

        crypto currency code

        :return: The currency of this Block.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this Block.

        crypto currency code

        :param currency: The currency of this Block.
        :type currency: str
        """
        if currency is None:
            raise ValueError("Invalid value for `currency`, must not be `None`")

        self._currency = currency

    @property
    def height(self):
        """Gets the height of this Block.

        Height

        :return: The height of this Block.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this Block.

        Height

        :param height: The height of this Block.
        :type height: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")
        if height is not None and height < 0:
            raise ValueError("Invalid value for `height`, must be a value greater than or equal to `0`")

        self._height = height

    @property
    def no_txs(self):
        """Gets the no_txs of this Block.


        :return: The no_txs of this Block.
        :rtype: int
        """
        return self._no_txs

    @no_txs.setter
    def no_txs(self, no_txs):
        """Sets the no_txs of this Block.


        :param no_txs: The no_txs of this Block.
        :type no_txs: int
        """
        if no_txs is None:
            raise ValueError("Invalid value for `no_txs`, must not be `None`")

        self._no_txs = no_txs

    @property
    def timestamp(self):
        """Gets the timestamp of this Block.

        Timestamp

        :return: The timestamp of this Block.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this Block.

        Timestamp

        :param timestamp: The timestamp of this Block.
        :type timestamp: int
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")

        self._timestamp = timestamp
