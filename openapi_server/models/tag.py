# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Tag(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, abuse: str=None, active: bool=None, category: str=None, currency: str=None, label: str=None, lastmod: int=None, source: str=None, tagpack_uri: str=None):
        """Tag - a model defined in OpenAPI

        :param abuse: The abuse of this Tag.
        :param active: The active of this Tag.
        :param category: The category of this Tag.
        :param currency: The currency of this Tag.
        :param label: The label of this Tag.
        :param lastmod: The lastmod of this Tag.
        :param source: The source of this Tag.
        :param tagpack_uri: The tagpack_uri of this Tag.
        """
        self.openapi_types = {
            'abuse': str,
            'active': bool,
            'category': str,
            'currency': str,
            'label': str,
            'lastmod': int,
            'source': str,
            'tagpack_uri': str
        }

        self.attribute_map = {
            'abuse': 'abuse',
            'active': 'active',
            'category': 'category',
            'currency': 'currency',
            'label': 'label',
            'lastmod': 'lastmod',
            'source': 'source',
            'tagpack_uri': 'tagpack_uri'
        }

        self._abuse = abuse
        self._active = active
        self._category = category
        self._currency = currency
        self._label = label
        self._lastmod = lastmod
        self._source = source
        self._tagpack_uri = tagpack_uri

    @classmethod
    def from_dict(cls, dikt: dict) -> 'Tag':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The tag of this Tag.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The Tag as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'abuse': self._abuse,
            'active': self._active,
            'category': self._category,
            'currency': self._currency,
            'label': self._label,
            'lastmod': self._lastmod,
            'source': self._source,
            'tagpack_uri': self._tagpack_uri }


    @property
    def abuse(self):
        """Gets the abuse of this Tag.

        Abuses

        :return: The abuse of this Tag.
        :rtype: str
        """
        return self._abuse

    @abuse.setter
    def abuse(self, abuse):
        """Sets the abuse of this Tag.

        Abuses

        :param abuse: The abuse of this Tag.
        :type abuse: str
        """

        self._abuse = abuse

    @property
    def active(self):
        """Gets the active of this Tag.

        whether the address has been ever used

        :return: The active of this Tag.
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """Sets the active of this Tag.

        whether the address has been ever used

        :param active: The active of this Tag.
        :type active: bool
        """
        if active is None:
            raise ValueError("Invalid value for `active`, must not be `None`")

        self._active = active

    @property
    def category(self):
        """Gets the category of this Tag.

        Category

        :return: The category of this Tag.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this Tag.

        Category

        :param category: The category of this Tag.
        :type category: str
        """

        self._category = category

    @property
    def currency(self):
        """Gets the currency of this Tag.

        crypto currency code

        :return: The currency of this Tag.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this Tag.

        crypto currency code

        :param currency: The currency of this Tag.
        :type currency: str
        """
        if currency is None:
            raise ValueError("Invalid value for `currency`, must not be `None`")

        self._currency = currency

    @property
    def label(self):
        """Gets the label of this Tag.

        Label

        :return: The label of this Tag.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this Tag.

        Label

        :param label: The label of this Tag.
        :type label: str
        """
        if label is None:
            raise ValueError("Invalid value for `label`, must not be `None`")

        self._label = label

    @property
    def lastmod(self):
        """Gets the lastmod of this Tag.

        Last modified

        :return: The lastmod of this Tag.
        :rtype: int
        """
        return self._lastmod

    @lastmod.setter
    def lastmod(self, lastmod):
        """Sets the lastmod of this Tag.

        Last modified

        :param lastmod: The lastmod of this Tag.
        :type lastmod: int
        """

        self._lastmod = lastmod

    @property
    def source(self):
        """Gets the source of this Tag.

        Source

        :return: The source of this Tag.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this Tag.

        Source

        :param source: The source of this Tag.
        :type source: str
        """

        self._source = source

    @property
    def tagpack_uri(self):
        """Gets the tagpack_uri of this Tag.

        Tagpack URI

        :return: The tagpack_uri of this Tag.
        :rtype: str
        """
        return self._tagpack_uri

    @tagpack_uri.setter
    def tagpack_uri(self, tagpack_uri):
        """Sets the tagpack_uri of this Tag.

        Tagpack URI

        :param tagpack_uri: The tagpack_uri of this Tag.
        :type tagpack_uri: str
        """

        self._tagpack_uri = tagpack_uri
