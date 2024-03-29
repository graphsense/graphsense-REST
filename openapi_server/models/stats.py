# coding: utf-8
from gsrest.errors import BadUserInputException
from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.currency_stats import CurrencyStats
from openapi_server import util


class Stats(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, currencies: List[CurrencyStats]=None, version: str=None, request_timestamp: str=None):
        """Stats - a model defined in OpenAPI

        :param currencies: The currencies of this Stats.
        :param version: The version of this Stats.
        :param request_timestamp: The request_timestamp of this Stats.
        """
        self.openapi_types = {
            'currencies': List[CurrencyStats],
            'version': str,
            'request_timestamp': str
        }

        self.attribute_map = {
            'currencies': 'currencies',
            'version': 'version',
            'request_timestamp': 'request_timestamp'
        }

        self._currencies = currencies
        self._version = version
        self._request_timestamp = request_timestamp

    @classmethod
    def from_dict(cls, dikt: dict) -> 'Stats':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The stats of this Stats.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The Stats as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'currencies': self._currencies,
            'version': self._version,
            'request_timestamp': self._request_timestamp }


    @property
    def currencies(self):
        """Gets the currencies of this Stats.


        :return: The currencies of this Stats.
        :rtype: List[CurrencyStats]
        """
        return self._currencies

    @currencies.setter
    def currencies(self, currencies):
        """Sets the currencies of this Stats.


        :param currencies: The currencies of this Stats.
        :type currencies: List[CurrencyStats]
        """
        if currencies is None:
            raise BadUserInputException("Invalid value for `currencies`, must not be `None`")

        self._currencies = currencies

    @property
    def version(self):
        """Gets the version of this Stats.


        :return: The version of this Stats.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Stats.


        :param version: The version of this Stats.
        :type version: str
        """
        if version is None:
            raise BadUserInputException("Invalid value for `version`, must not be `None`")

        self._version = version

    @property
    def request_timestamp(self):
        """Gets the request_timestamp of this Stats.


        :return: The request_timestamp of this Stats.
        :rtype: str
        """
        return self._request_timestamp

    @request_timestamp.setter
    def request_timestamp(self, request_timestamp):
        """Sets the request_timestamp of this Stats.


        :param request_timestamp: The request_timestamp of this Stats.
        :type request_timestamp: str
        """
        if request_timestamp is None:
            raise BadUserInputException("Invalid value for `request_timestamp`, must not be `None`")

        self._request_timestamp = request_timestamp
