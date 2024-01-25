# coding: utf-8
from gsrest.errors import BadUserInputException
from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.entity import Entity
from openapi_server.models.values import Values
from openapi_server import util


class NeighborEntity(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, labels: List[str]=None, value: Values=None, token_values: Dict[str, Values]=None, no_txs: int=None, entity: Entity=None):
        """NeighborEntity - a model defined in OpenAPI

        :param labels: The labels of this NeighborEntity.
        :param value: The value of this NeighborEntity.
        :param token_values: The token_values of this NeighborEntity.
        :param no_txs: The no_txs of this NeighborEntity.
        :param entity: The entity of this NeighborEntity.
        """
        self.openapi_types = {
            'labels': List[str],
            'value': Values,
            'token_values': Dict[str, Values],
            'no_txs': int,
            'entity': Entity
        }

        self.attribute_map = {
            'labels': 'labels',
            'value': 'value',
            'token_values': 'token_values',
            'no_txs': 'no_txs',
            'entity': 'entity'
        }

        self._labels = labels
        self._value = value
        self._token_values = token_values
        self._no_txs = no_txs
        self._entity = entity

    @classmethod
    def from_dict(cls, dikt: dict) -> 'NeighborEntity':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The neighbor_entity of this NeighborEntity.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The NeighborEntity as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'labels': self._labels,
            'value': self._value,
            'token_values': self._token_values,
            'no_txs': self._no_txs,
            'entity': self._entity }


    @property
    def labels(self):
        """Gets the labels of this NeighborEntity.

        The neighbor's tag labels

        :return: The labels of this NeighborEntity.
        :rtype: List[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this NeighborEntity.

        The neighbor's tag labels

        :param labels: The labels of this NeighborEntity.
        :type labels: List[str]
        """

        self._labels = labels

    @property
    def value(self):
        """Gets the value of this NeighborEntity.


        :return: The value of this NeighborEntity.
        :rtype: Values
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this NeighborEntity.


        :param value: The value of this NeighborEntity.
        :type value: Values
        """
        if value is None:
            raise BadUserInputException("Invalid value for `value`, must not be `None`")

        self._value = value

    @property
    def token_values(self):
        """Gets the token_values of this NeighborEntity.

        Per token value-flow

        :return: The token_values of this NeighborEntity.
        :rtype: Dict[str, Values]
        """
        return self._token_values

    @token_values.setter
    def token_values(self, token_values):
        """Sets the token_values of this NeighborEntity.

        Per token value-flow

        :param token_values: The token_values of this NeighborEntity.
        :type token_values: Dict[str, Values]
        """

        self._token_values = token_values

    @property
    def no_txs(self):
        """Gets the no_txs of this NeighborEntity.

        number of transactions

        :return: The no_txs of this NeighborEntity.
        :rtype: int
        """
        return self._no_txs

    @no_txs.setter
    def no_txs(self, no_txs):
        """Sets the no_txs of this NeighborEntity.

        number of transactions

        :param no_txs: The no_txs of this NeighborEntity.
        :type no_txs: int
        """
        if no_txs is None:
            raise BadUserInputException("Invalid value for `no_txs`, must not be `None`")

        self._no_txs = no_txs

    @property
    def entity(self):
        """Gets the entity of this NeighborEntity.


        :return: The entity of this NeighborEntity.
        :rtype: Entity
        """
        return self._entity

    @entity.setter
    def entity(self, entity):
        """Sets the entity of this NeighborEntity.


        :param entity: The entity of this NeighborEntity.
        :type entity: Entity
        """
        if entity is None:
            raise BadUserInputException("Invalid value for `entity`, must not be `None`")

        self._entity = entity
