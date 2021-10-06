# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.get_tx_io import GetTxIo
from openapi_server.models.get_tx_io_parameters import GetTxIoParameters
from openapi_server import util

from openapi_server.models.get_tx_io import GetTxIo  # noqa: E501
from openapi_server.models.get_tx_io_parameters import GetTxIoParameters  # noqa: E501

class BatchOperation(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, operation='get_tx_io', parameters=None):  # noqa: E501
        """BatchOperation - a model defined in OpenAPI

        :param operation: The operation of this BatchOperation.  # noqa: E501
        :type operation: str
        :param parameters: The parameters of this BatchOperation.  # noqa: E501
        :type parameters: List[GetTxIoParameters]
        """
        self.openapi_types = {
            'operation': str,
            'parameters': List[GetTxIoParameters]
        }

        self.attribute_map = {
            'operation': 'operation',
            'parameters': 'parameters'
        }

        #if operation is None:
            #raise ValueError("Invalid value for `operation`, must not be `None`")  # noqa: E501
        self._operation = operation
        #if parameters is None:
            #raise ValueError("Invalid value for `parameters`, must not be `None`")  # noqa: E501
        self._parameters = parameters

    @classmethod
    def from_dict(cls, dikt) -> 'BatchOperation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The batch_operation of this BatchOperation.  # noqa: E501
        :rtype: BatchOperation
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The BatchOperation as a dict
        :rtype: dict
        """
        return { 'operation': self._operation,
            'parameters': self._parameters }


    @property
    def operation(self):
        """Gets the operation of this BatchOperation.


        :return: The operation of this BatchOperation.
        :rtype: str
        """
        return self._operation

    @operation.setter
    def operation(self, operation):
        """Sets the operation of this BatchOperation.


        :param operation: The operation of this BatchOperation.
        :type operation: str
        """
        if operation is None:
            raise ValueError("Invalid value for `operation`, must not be `None`")  # noqa: E501

        self._operation = operation

    @property
    def parameters(self):
        """Gets the parameters of this BatchOperation.


        :return: The parameters of this BatchOperation.
        :rtype: List[GetTxIoParameters]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this BatchOperation.


        :param parameters: The parameters of this BatchOperation.
        :type parameters: List[GetTxIoParameters]
        """
        if parameters is None:
            raise ValueError("Invalid value for `parameters`, must not be `None`")  # noqa: E501

        self._parameters = parameters
