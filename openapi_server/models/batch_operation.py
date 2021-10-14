# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.get_tx import GetTx
from openapi_server.models.get_tx_io import GetTxIo
from openapi_server.models.io import Io
from openapi_server.models.list_entity_addresses import ListEntityAddresses
from openapi_server import util

from openapi_server.models.get_tx import GetTx  # noqa: E501
from openapi_server.models.get_tx_io import GetTxIo  # noqa: E501
from openapi_server.models.io import Io  # noqa: E501
from openapi_server.models.list_entity_addresses import ListEntityAddresses  # noqa: E501

class BatchOperation(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, api='entities', operation='list_entity_addresses', tx_hash=None, io=None, entity=None):  # noqa: E501
        """BatchOperation - a model defined in OpenAPI

        :param api: The api of this BatchOperation.  # noqa: E501
        :type api: str
        :param operation: The operation of this BatchOperation.  # noqa: E501
        :type operation: str
        :param tx_hash: The tx_hash of this BatchOperation.  # noqa: E501
        :type tx_hash: List[str]
        :param io: The io of this BatchOperation.  # noqa: E501
        :type io: Io
        :param entity: The entity of this BatchOperation.  # noqa: E501
        :type entity: List[int]
        """
        self.openapi_types = {
            'api': str,
            'operation': str,
            'tx_hash': List[str],
            'io': Io,
            'entity': List[int]
        }

        self.attribute_map = {
            'api': 'api',
            'operation': 'operation',
            'tx_hash': 'tx_hash',
            'io': 'io',
            'entity': 'entity'
        }

        #if api is None:
            #raise ValueError("Invalid value for `api`, must not be `None`")  # noqa: E501
        self._api = api
        #if operation is None:
            #raise ValueError("Invalid value for `operation`, must not be `None`")  # noqa: E501
        self._operation = operation
        #if tx_hash is None:
            #raise ValueError("Invalid value for `tx_hash`, must not be `None`")  # noqa: E501
        self._tx_hash = tx_hash
        #if io is None:
            #raise ValueError("Invalid value for `io`, must not be `None`")  # noqa: E501
        self._io = io
        #if entity is None:
            #raise ValueError("Invalid value for `entity`, must not be `None`")  # noqa: E501
        self._entity = entity

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
        return { 'api': self._api,
            'operation': self._operation,
            'tx_hash': self._tx_hash,
            'io': self._io,
            'entity': self._entity }


    @property
    def api(self):
        """Gets the api of this BatchOperation.


        :return: The api of this BatchOperation.
        :rtype: str
        """
        return self._api

    @api.setter
    def api(self, api):
        """Sets the api of this BatchOperation.


        :param api: The api of this BatchOperation.
        :type api: str
        """
        if api is None:
            raise ValueError("Invalid value for `api`, must not be `None`")  # noqa: E501

        self._api = api

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
    def tx_hash(self):
        """Gets the tx_hash of this BatchOperation.


        :return: The tx_hash of this BatchOperation.
        :rtype: List[str]
        """
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        """Sets the tx_hash of this BatchOperation.


        :param tx_hash: The tx_hash of this BatchOperation.
        :type tx_hash: List[str]
        """
        if tx_hash is None:
            raise ValueError("Invalid value for `tx_hash`, must not be `None`")  # noqa: E501

        self._tx_hash = tx_hash

    @property
    def io(self):
        """Gets the io of this BatchOperation.


        :return: The io of this BatchOperation.
        :rtype: Io
        """
        return self._io

    @io.setter
    def io(self, io):
        """Sets the io of this BatchOperation.


        :param io: The io of this BatchOperation.
        :type io: Io
        """
        if io is None:
            raise ValueError("Invalid value for `io`, must not be `None`")  # noqa: E501

        self._io = io

    @property
    def entity(self):
        """Gets the entity of this BatchOperation.


        :return: The entity of this BatchOperation.
        :rtype: List[int]
        """
        return self._entity

    @entity.setter
    def entity(self, entity):
        """Sets the entity of this BatchOperation.


        :param entity: The entity of this BatchOperation.
        :type entity: List[int]
        """
        if entity is None:
            raise ValueError("Invalid value for `entity`, must not be `None`")  # noqa: E501

        self._entity = entity
