# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.tx_value import TxValue
from openapi_server.models.values import Values
from openapi_server import util


class TxUtxo(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, coinbase: bool=None, height: int=None, inputs: List[TxValue]=None, outputs: List[TxValue]=None, timestamp: int=None, total_input: Values=None, total_output: Values=None, tx_hash: str=None, tx_type: str='utxo'):
        """TxUtxo - a model defined in OpenAPI

        :param coinbase: The coinbase of this TxUtxo.
        :param height: The height of this TxUtxo.
        :param inputs: The inputs of this TxUtxo.
        :param outputs: The outputs of this TxUtxo.
        :param timestamp: The timestamp of this TxUtxo.
        :param total_input: The total_input of this TxUtxo.
        :param total_output: The total_output of this TxUtxo.
        :param tx_hash: The tx_hash of this TxUtxo.
        :param tx_type: The tx_type of this TxUtxo.
        """
        self.openapi_types = {
            'coinbase': bool,
            'height': int,
            'inputs': List[TxValue],
            'outputs': List[TxValue],
            'timestamp': int,
            'total_input': Values,
            'total_output': Values,
            'tx_hash': str,
            'tx_type': str
        }

        self.attribute_map = {
            'coinbase': 'coinbase',
            'height': 'height',
            'inputs': 'inputs',
            'outputs': 'outputs',
            'timestamp': 'timestamp',
            'total_input': 'total_input',
            'total_output': 'total_output',
            'tx_hash': 'tx_hash',
            'tx_type': 'tx_type'
        }

        self._coinbase = coinbase
        self._height = height
        self._inputs = inputs
        self._outputs = outputs
        self._timestamp = timestamp
        self._total_input = total_input
        self._total_output = total_output
        self._tx_hash = tx_hash
        self._tx_type = tx_type

    @classmethod
    def from_dict(cls, dikt: dict) -> 'TxUtxo':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The tx_utxo of this TxUtxo.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The TxUtxo as a dict
        :rtype: dict
        """
        return { 'coinbase': self._coinbase,
            'height': self._height,
            'inputs': self._inputs,
            'outputs': self._outputs,
            'timestamp': self._timestamp,
            'total_input': self._total_input,
            'total_output': self._total_output,
            'tx_hash': self._tx_hash,
            'tx_type': self._tx_type }


    @property
    def coinbase(self):
        """Gets the coinbase of this TxUtxo.

        Coinbase transaction flag

        :return: The coinbase of this TxUtxo.
        :rtype: bool
        """
        return self._coinbase

    @coinbase.setter
    def coinbase(self, coinbase):
        """Sets the coinbase of this TxUtxo.

        Coinbase transaction flag

        :param coinbase: The coinbase of this TxUtxo.
        :type coinbase: bool
        """
        if coinbase is None:
            raise ValueError("Invalid value for `coinbase`, must not be `None`")

        self._coinbase = coinbase

    @property
    def height(self):
        """Gets the height of this TxUtxo.

        Height

        :return: The height of this TxUtxo.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this TxUtxo.

        Height

        :param height: The height of this TxUtxo.
        :type height: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")
        if height is not None and height < 0:
            raise ValueError("Invalid value for `height`, must be a value greater than or equal to `0`")

        self._height = height

    @property
    def inputs(self):
        """Gets the inputs of this TxUtxo.

        Transaction inputs/outputs

        :return: The inputs of this TxUtxo.
        :rtype: List[TxValue]
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this TxUtxo.

        Transaction inputs/outputs

        :param inputs: The inputs of this TxUtxo.
        :type inputs: List[TxValue]
        """

        self._inputs = inputs

    @property
    def outputs(self):
        """Gets the outputs of this TxUtxo.

        Transaction inputs/outputs

        :return: The outputs of this TxUtxo.
        :rtype: List[TxValue]
        """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        """Sets the outputs of this TxUtxo.

        Transaction inputs/outputs

        :param outputs: The outputs of this TxUtxo.
        :type outputs: List[TxValue]
        """

        self._outputs = outputs

    @property
    def timestamp(self):
        """Gets the timestamp of this TxUtxo.

        Timestamp

        :return: The timestamp of this TxUtxo.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this TxUtxo.

        Timestamp

        :param timestamp: The timestamp of this TxUtxo.
        :type timestamp: int
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")

        self._timestamp = timestamp

    @property
    def total_input(self):
        """Gets the total_input of this TxUtxo.


        :return: The total_input of this TxUtxo.
        :rtype: Values
        """
        return self._total_input

    @total_input.setter
    def total_input(self, total_input):
        """Sets the total_input of this TxUtxo.


        :param total_input: The total_input of this TxUtxo.
        :type total_input: Values
        """
        if total_input is None:
            raise ValueError("Invalid value for `total_input`, must not be `None`")

        self._total_input = total_input

    @property
    def total_output(self):
        """Gets the total_output of this TxUtxo.


        :return: The total_output of this TxUtxo.
        :rtype: Values
        """
        return self._total_output

    @total_output.setter
    def total_output(self, total_output):
        """Sets the total_output of this TxUtxo.


        :param total_output: The total_output of this TxUtxo.
        :type total_output: Values
        """
        if total_output is None:
            raise ValueError("Invalid value for `total_output`, must not be `None`")

        self._total_output = total_output

    @property
    def tx_hash(self):
        """Gets the tx_hash of this TxUtxo.

        Transaction hash

        :return: The tx_hash of this TxUtxo.
        :rtype: str
        """
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        """Sets the tx_hash of this TxUtxo.

        Transaction hash

        :param tx_hash: The tx_hash of this TxUtxo.
        :type tx_hash: str
        """
        if tx_hash is None:
            raise ValueError("Invalid value for `tx_hash`, must not be `None`")

        self._tx_hash = tx_hash

    @property
    def tx_type(self):
        """Gets the tx_type of this TxUtxo.


        :return: The tx_type of this TxUtxo.
        :rtype: str
        """
        return self._tx_type

    @tx_type.setter
    def tx_type(self, tx_type):
        """Sets the tx_type of this TxUtxo.


        :param tx_type: The tx_type of this TxUtxo.
        :type tx_type: str
        """
        if tx_type is None:
            raise ValueError("Invalid value for `tx_type`, must not be `None`")

        self._tx_type = tx_type
