# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.values import Values
from openapi_server import util

from openapi_server.models.values import Values  # noqa: E501

class BlockTxSummary(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, tx_hash=None, no_inputs=None, no_outputs=None, total_input=None, total_output=None):  # noqa: E501
        """BlockTxSummary - a model defined in OpenAPI

        :param tx_hash: The tx_hash of this BlockTxSummary.  # noqa: E501
        :type tx_hash: str
        :param no_inputs: The no_inputs of this BlockTxSummary.  # noqa: E501
        :type no_inputs: int
        :param no_outputs: The no_outputs of this BlockTxSummary.  # noqa: E501
        :type no_outputs: int
        :param total_input: The total_input of this BlockTxSummary.  # noqa: E501
        :type total_input: Values
        :param total_output: The total_output of this BlockTxSummary.  # noqa: E501
        :type total_output: Values
        """
        self.openapi_types = {
            'tx_hash': str,
            'no_inputs': int,
            'no_outputs': int,
            'total_input': Values,
            'total_output': Values
        }

        self.attribute_map = {
            'tx_hash': 'tx_hash',
            'no_inputs': 'no_inputs',
            'no_outputs': 'no_outputs',
            'total_input': 'total_input',
            'total_output': 'total_output'
        }

        self._tx_hash = tx_hash
        self._no_inputs = no_inputs
        self._no_outputs = no_outputs
        self._total_input = total_input
        self._total_output = total_output

    @classmethod
    def from_dict(cls, dikt) -> 'BlockTxSummary':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The block_tx_summary of this BlockTxSummary.  # noqa: E501
        :rtype: BlockTxSummary
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The BlockTxSummary as a dict
        :rtype: dict
        """
        return { 'tx_hash': self._tx_hash,
            'no_inputs': self._no_inputs,
            'no_outputs': self._no_outputs,
            'total_input': self._total_input,
            'total_output': self._total_output }


    @property
    def tx_hash(self):
        """Gets the tx_hash of this BlockTxSummary.


        :return: The tx_hash of this BlockTxSummary.
        :rtype: str
        """
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        """Sets the tx_hash of this BlockTxSummary.


        :param tx_hash: The tx_hash of this BlockTxSummary.
        :type tx_hash: str
        """

        self._tx_hash = tx_hash

    @property
    def no_inputs(self):
        """Gets the no_inputs of this BlockTxSummary.


        :return: The no_inputs of this BlockTxSummary.
        :rtype: int
        """
        return self._no_inputs

    @no_inputs.setter
    def no_inputs(self, no_inputs):
        """Sets the no_inputs of this BlockTxSummary.


        :param no_inputs: The no_inputs of this BlockTxSummary.
        :type no_inputs: int
        """

        self._no_inputs = no_inputs

    @property
    def no_outputs(self):
        """Gets the no_outputs of this BlockTxSummary.


        :return: The no_outputs of this BlockTxSummary.
        :rtype: int
        """
        return self._no_outputs

    @no_outputs.setter
    def no_outputs(self, no_outputs):
        """Sets the no_outputs of this BlockTxSummary.


        :param no_outputs: The no_outputs of this BlockTxSummary.
        :type no_outputs: int
        """

        self._no_outputs = no_outputs

    @property
    def total_input(self):
        """Gets the total_input of this BlockTxSummary.


        :return: The total_input of this BlockTxSummary.
        :rtype: Values
        """
        return self._total_input

    @total_input.setter
    def total_input(self, total_input):
        """Sets the total_input of this BlockTxSummary.


        :param total_input: The total_input of this BlockTxSummary.
        :type total_input: Values
        """

        self._total_input = total_input

    @property
    def total_output(self):
        """Gets the total_output of this BlockTxSummary.


        :return: The total_output of this BlockTxSummary.
        :rtype: Values
        """
        return self._total_output

    @total_output.setter
    def total_output(self, total_output):
        """Sets the total_output of this BlockTxSummary.


        :param total_output: The total_output of this BlockTxSummary.
        :type total_output: Values
        """

        self._total_output = total_output