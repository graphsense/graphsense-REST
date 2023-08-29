# coding: utf-8
from gsrest.errors import *
from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class TxRef(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, input_index: int=None, output_index: int=None, tx_hash: str=None):
        """TxRef - a model defined in OpenAPI

        :param input_index: The input_index of this TxRef.
        :param output_index: The output_index of this TxRef.
        :param tx_hash: The tx_hash of this TxRef.
        """
        self.openapi_types = {
            'input_index': int,
            'output_index': int,
            'tx_hash': str
        }

        self.attribute_map = {
            'input_index': 'input_index',
            'output_index': 'output_index',
            'tx_hash': 'tx_hash'
        }

        self._input_index = input_index
        self._output_index = output_index
        self._tx_hash = tx_hash

    @classmethod
    def from_dict(cls, dikt: dict) -> 'TxRef':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The tx_ref of this TxRef.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The TxRef as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'input_index': self._input_index,
            'output_index': self._output_index,
            'tx_hash': self._tx_hash }


    @property
    def input_index(self):
        """Gets the input_index of this TxRef.


        :return: The input_index of this TxRef.
        :rtype: int
        """
        return self._input_index

    @input_index.setter
    def input_index(self, input_index):
        """Sets the input_index of this TxRef.


        :param input_index: The input_index of this TxRef.
        :type input_index: int
        """
        if input_index is None:
            raise BadUserInputException("Invalid value for `input_index`, must not be `None`")

        self._input_index = input_index

    @property
    def output_index(self):
        """Gets the output_index of this TxRef.


        :return: The output_index of this TxRef.
        :rtype: int
        """
        return self._output_index

    @output_index.setter
    def output_index(self, output_index):
        """Sets the output_index of this TxRef.


        :param output_index: The output_index of this TxRef.
        :type output_index: int
        """
        if output_index is None:
            raise BadUserInputException("Invalid value for `output_index`, must not be `None`")

        self._output_index = output_index

    @property
    def tx_hash(self):
        """Gets the tx_hash of this TxRef.


        :return: The tx_hash of this TxRef.
        :rtype: str
        """
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        """Sets the tx_hash of this TxRef.


        :param tx_hash: The tx_hash of this TxRef.
        :type tx_hash: str
        """
        if tx_hash is None:
            raise BadUserInputException("Invalid value for `tx_hash`, must not be `None`")

        self._tx_hash = tx_hash
