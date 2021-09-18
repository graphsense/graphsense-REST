# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Tag(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, label=None, category=None, abuse=None, tagpack_uri=None, source=None, lastmod=None, active=None, currency=None):  # noqa: E501
        """Tag - a model defined in OpenAPI

        :param label: The label of this Tag.  # noqa: E501
        :type label: str
        :param category: The category of this Tag.  # noqa: E501
        :type category: str
        :param abuse: The abuse of this Tag.  # noqa: E501
        :type abuse: str
        :param tagpack_uri: The tagpack_uri of this Tag.  # noqa: E501
        :type tagpack_uri: str
        :param source: The source of this Tag.  # noqa: E501
        :type source: str
        :param lastmod: The lastmod of this Tag.  # noqa: E501
        :type lastmod: int
        :param active: The active of this Tag.  # noqa: E501
        :type active: bool
        :param currency: The currency of this Tag.  # noqa: E501
        :type currency: str
        """
        self.openapi_types = {
            'label': str,
            'category': str,
            'abuse': str,
            'tagpack_uri': str,
            'source': str,
            'lastmod': int,
            'active': bool,
            'currency': str
        }

        self.attribute_map = {
            'label': 'label',
            'category': 'category',
            'abuse': 'abuse',
            'tagpack_uri': 'tagpack_uri',
            'source': 'source',
            'lastmod': 'lastmod',
            'active': 'active',
            'currency': 'currency'
        }

        if label is None:
            raise ValueError("Invalid value for `label`, must not be `None`")  # noqa: E501
        self._label = label
        self._category = category
        self._abuse = abuse
        self._tagpack_uri = tagpack_uri
        self._source = source
        self._lastmod = lastmod
        if active is None:
            raise ValueError("Invalid value for `active`, must not be `None`")  # noqa: E501
        self._active = active
        if currency is None:
            raise ValueError("Invalid value for `currency`, must not be `None`")  # noqa: E501
        self._currency = currency

    @classmethod
    def from_dict(cls, dikt) -> 'Tag':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The tag of this Tag.  # noqa: E501
        :rtype: Tag
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The Tag as a dict
        :rtype: dict
        """
        return { 'label': self._label,
            'category': self._category,
            'abuse': self._abuse,
            'tagpack_uri': self._tagpack_uri,
            'source': self._source,
            'lastmod': self._lastmod,
            'active': self._active,
            'currency': self._currency }


    @property
    def label(self):
        """Gets the label of this Tag.

        Label  # noqa: E501

        :return: The label of this Tag.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this Tag.

        Label  # noqa: E501

        :param label: The label of this Tag.
        :type label: str
        """
        if label is None:
            raise ValueError("Invalid value for `label`, must not be `None`")  # noqa: E501

        self._label = label

    @property
    def category(self):
        """Gets the category of this Tag.

        Category  # noqa: E501

        :return: The category of this Tag.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this Tag.

        Category  # noqa: E501

        :param category: The category of this Tag.
        :type category: str
        """

        self._category = category

    @property
    def abuse(self):
        """Gets the abuse of this Tag.

        Abuses  # noqa: E501

        :return: The abuse of this Tag.
        :rtype: str
        """
        return self._abuse

    @abuse.setter
    def abuse(self, abuse):
        """Sets the abuse of this Tag.

        Abuses  # noqa: E501

        :param abuse: The abuse of this Tag.
        :type abuse: str
        """

        self._abuse = abuse

    @property
    def tagpack_uri(self):
        """Gets the tagpack_uri of this Tag.

        Tagpack URI  # noqa: E501

        :return: The tagpack_uri of this Tag.
        :rtype: str
        """
        return self._tagpack_uri

    @tagpack_uri.setter
    def tagpack_uri(self, tagpack_uri):
        """Sets the tagpack_uri of this Tag.

        Tagpack URI  # noqa: E501

        :param tagpack_uri: The tagpack_uri of this Tag.
        :type tagpack_uri: str
        """

        self._tagpack_uri = tagpack_uri

    @property
    def source(self):
        """Gets the source of this Tag.

        Source  # noqa: E501

        :return: The source of this Tag.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this Tag.

        Source  # noqa: E501

        :param source: The source of this Tag.
        :type source: str
        """

        self._source = source

    @property
    def lastmod(self):
        """Gets the lastmod of this Tag.

        Last modified  # noqa: E501

        :return: The lastmod of this Tag.
        :rtype: int
        """
        return self._lastmod

    @lastmod.setter
    def lastmod(self, lastmod):
        """Sets the lastmod of this Tag.

        Last modified  # noqa: E501

        :param lastmod: The lastmod of this Tag.
        :type lastmod: int
        """

        self._lastmod = lastmod

    @property
    def active(self):
        """Gets the active of this Tag.

        whether the address has been ever used  # noqa: E501

        :return: The active of this Tag.
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """Sets the active of this Tag.

        whether the address has been ever used  # noqa: E501

        :param active: The active of this Tag.
        :type active: bool
        """
        if active is None:
            raise ValueError("Invalid value for `active`, must not be `None`")  # noqa: E501

        self._active = active

    @property
    def currency(self):
        """Gets the currency of this Tag.

        Currency  # noqa: E501

        :return: The currency of this Tag.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this Tag.

        Currency  # noqa: E501

        :param currency: The currency of this Tag.
        :type currency: str
        """
        if currency is None:
            raise ValueError("Invalid value for `currency`, must not be `None`")  # noqa: E501

        self._currency = currency
