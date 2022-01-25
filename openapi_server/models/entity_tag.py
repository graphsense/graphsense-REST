# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.entity_tag_all_of import EntityTagAllOf
from openapi_server.models.tag import Tag
from openapi_server import util


class EntityTag(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, abuse: str=None, active: bool=None, category: str=None, currency: str=None, label: str=None, lastmod: int=None, source: str=None, tagpack_uri: str=None, entity: int=None):
        """EntityTag - a model defined in OpenAPI

        :param abuse: The abuse of this EntityTag.
        :param active: The active of this EntityTag.
        :param category: The category of this EntityTag.
        :param currency: The currency of this EntityTag.
        :param label: The label of this EntityTag.
        :param lastmod: The lastmod of this EntityTag.
        :param source: The source of this EntityTag.
        :param tagpack_uri: The tagpack_uri of this EntityTag.
        :param entity: The entity of this EntityTag.
        """
        self.openapi_types = {
            'abuse': str,
            'active': bool,
            'category': str,
            'currency': str,
            'label': str,
            'lastmod': int,
            'source': str,
            'tagpack_uri': str,
            'entity': int
        }

        self.attribute_map = {
            'abuse': 'abuse',
            'active': 'active',
            'category': 'category',
            'currency': 'currency',
            'label': 'label',
            'lastmod': 'lastmod',
            'source': 'source',
            'tagpack_uri': 'tagpack_uri',
            'entity': 'entity'
        }

        self._abuse = abuse
        self._active = active
        self._category = category
        self._currency = currency
        self._label = label
        self._lastmod = lastmod
        self._source = source
        self._tagpack_uri = tagpack_uri
        self._entity = entity

    @classmethod
    def from_dict(cls, dikt: dict) -> 'EntityTag':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The entity_tag of this EntityTag.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The EntityTag as a dict
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
            'tagpack_uri': self._tagpack_uri,
            'entity': self._entity }


    @property
    def abuse(self):
        """Gets the abuse of this EntityTag.

        Abuses

        :return: The abuse of this EntityTag.
        :rtype: str
        """
        return self._abuse

    @abuse.setter
    def abuse(self, abuse):
        """Sets the abuse of this EntityTag.

        Abuses

        :param abuse: The abuse of this EntityTag.
        :type abuse: str
        """

        self._abuse = abuse

    @property
    def active(self):
        """Gets the active of this EntityTag.

        whether the address has been ever used

        :return: The active of this EntityTag.
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """Sets the active of this EntityTag.

        whether the address has been ever used

        :param active: The active of this EntityTag.
        :type active: bool
        """
        if active is None:
            raise ValueError("Invalid value for `active`, must not be `None`")

        self._active = active

    @property
    def category(self):
        """Gets the category of this EntityTag.

        Category

        :return: The category of this EntityTag.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this EntityTag.

        Category

        :param category: The category of this EntityTag.
        :type category: str
        """

        self._category = category

    @property
    def currency(self):
        """Gets the currency of this EntityTag.

        crypto currency code

        :return: The currency of this EntityTag.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this EntityTag.

        crypto currency code

        :param currency: The currency of this EntityTag.
        :type currency: str
        """
        if currency is None:
            raise ValueError("Invalid value for `currency`, must not be `None`")

        self._currency = currency

    @property
    def label(self):
        """Gets the label of this EntityTag.

        Label

        :return: The label of this EntityTag.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this EntityTag.

        Label

        :param label: The label of this EntityTag.
        :type label: str
        """
        if label is None:
            raise ValueError("Invalid value for `label`, must not be `None`")

        self._label = label

    @property
    def lastmod(self):
        """Gets the lastmod of this EntityTag.

        Last modified

        :return: The lastmod of this EntityTag.
        :rtype: int
        """
        return self._lastmod

    @lastmod.setter
    def lastmod(self, lastmod):
        """Sets the lastmod of this EntityTag.

        Last modified

        :param lastmod: The lastmod of this EntityTag.
        :type lastmod: int
        """

        self._lastmod = lastmod

    @property
    def source(self):
        """Gets the source of this EntityTag.

        Source

        :return: The source of this EntityTag.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this EntityTag.

        Source

        :param source: The source of this EntityTag.
        :type source: str
        """

        self._source = source

    @property
    def tagpack_uri(self):
        """Gets the tagpack_uri of this EntityTag.

        Tagpack URI

        :return: The tagpack_uri of this EntityTag.
        :rtype: str
        """
        return self._tagpack_uri

    @tagpack_uri.setter
    def tagpack_uri(self, tagpack_uri):
        """Sets the tagpack_uri of this EntityTag.

        Tagpack URI

        :param tagpack_uri: The tagpack_uri of this EntityTag.
        :type tagpack_uri: str
        """

        self._tagpack_uri = tagpack_uri

    @property
    def entity(self):
        """Gets the entity of this EntityTag.

        Entity id

        :return: The entity of this EntityTag.
        :rtype: int
        """
        return self._entity

    @entity.setter
    def entity(self, entity):
        """Sets the entity of this EntityTag.

        Entity id

        :param entity: The entity of this EntityTag.
        :type entity: int
        """
        if entity is None:
            raise ValueError("Invalid value for `entity`, must not be `None`")

        self._entity = entity
