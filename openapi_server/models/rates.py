# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.rates_rates import RatesRates
from openapi_server import util

from openapi_server.models.rates_rates import RatesRates  # noqa: E501

class Rates(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, height=None, rates=None):  # noqa: E501
        """Rates - a model defined in OpenAPI

        :param height: The height of this Rates.  # noqa: E501
        :type height: int
        :param rates: The rates of this Rates.  # noqa: E501
        :type rates: RatesRates
        """
        self.openapi_types = {
            'height': int,
            'rates': RatesRates
        }

        self.attribute_map = {
            'height': 'height',
            'rates': 'rates'
        }

        self._height = height
        self._rates = rates

    @classmethod
    def from_dict(cls, dikt) -> 'Rates':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The rates of this Rates.  # noqa: E501
        :rtype: Rates
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The Rates as a dict
        :rtype: dict
        """
        return { 'height': self._height,
            'rates': self._rates }


    @property
    def height(self):
        """Gets the height of this Rates.

        Height  # noqa: E501

        :return: The height of this Rates.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this Rates.

        Height  # noqa: E501

        :param height: The height of this Rates.
        :type height: int
        """
        if height is not None and height < 1:  # noqa: E501
            raise ValueError("Invalid value for `height`, must be a value greater than or equal to `1`")  # noqa: E501

        self._height = height

    @property
    def rates(self):
        """Gets the rates of this Rates.


        :return: The rates of this Rates.
        :rtype: RatesRates
        """
        return self._rates

    @rates.setter
    def rates(self, rates):
        """Sets the rates of this Rates.


        :param rates: The rates of this Rates.
        :type rates: RatesRates
        """

        self._rates = rates
