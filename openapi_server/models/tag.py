# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Tag(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, abuse: str=None, actor: str=None, category: str=None, confidence: str=None, confidence_level: int=None, currency: str=None, is_cluster_definer: bool=None, label: str=None, lastmod: int=None, source: str=None, tagpack_creator: str=None, tagpack_is_public: bool=None, tagpack_title: str=None, tagpack_uri: str=None):
        """Tag - a model defined in OpenAPI

        :param abuse: The abuse of this Tag.
        :param actor: The actor of this Tag.
        :param category: The category of this Tag.
        :param confidence: The confidence of this Tag.
        :param confidence_level: The confidence_level of this Tag.
        :param currency: The currency of this Tag.
        :param is_cluster_definer: The is_cluster_definer of this Tag.
        :param label: The label of this Tag.
        :param lastmod: The lastmod of this Tag.
        :param source: The source of this Tag.
        :param tagpack_creator: The tagpack_creator of this Tag.
        :param tagpack_is_public: The tagpack_is_public of this Tag.
        :param tagpack_title: The tagpack_title of this Tag.
        :param tagpack_uri: The tagpack_uri of this Tag.
        """
        self.openapi_types = {
            'abuse': str,
            'actor': str,
            'category': str,
            'confidence': str,
            'confidence_level': int,
            'currency': str,
            'is_cluster_definer': bool,
            'label': str,
            'lastmod': int,
            'source': str,
            'tagpack_creator': str,
            'tagpack_is_public': bool,
            'tagpack_title': str,
            'tagpack_uri': str
        }

        self.attribute_map = {
            'abuse': 'abuse',
            'actor': 'actor',
            'category': 'category',
            'confidence': 'confidence',
            'confidence_level': 'confidence_level',
            'currency': 'currency',
            'is_cluster_definer': 'is_cluster_definer',
            'label': 'label',
            'lastmod': 'lastmod',
            'source': 'source',
            'tagpack_creator': 'tagpack_creator',
            'tagpack_is_public': 'tagpack_is_public',
            'tagpack_title': 'tagpack_title',
            'tagpack_uri': 'tagpack_uri'
        }

        self._abuse = abuse
        self._actor = actor
        self._category = category
        self._confidence = confidence
        self._confidence_level = confidence_level
        self._currency = currency
        self._is_cluster_definer = is_cluster_definer
        self._label = label
        self._lastmod = lastmod
        self._source = source
        self._tagpack_creator = tagpack_creator
        self._tagpack_is_public = tagpack_is_public
        self._tagpack_title = tagpack_title
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
            'actor': self._actor,
            'category': self._category,
            'confidence': self._confidence,
            'confidence_level': self._confidence_level,
            'currency': self._currency,
            'is_cluster_definer': self._is_cluster_definer,
            'label': self._label,
            'lastmod': self._lastmod,
            'source': self._source,
            'tagpack_creator': self._tagpack_creator,
            'tagpack_is_public': self._tagpack_is_public,
            'tagpack_title': self._tagpack_title,
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
    def actor(self):
        """Gets the actor of this Tag.

        id of the actor that controlls the address

        :return: The actor of this Tag.
        :rtype: str
        """
        return self._actor

    @actor.setter
    def actor(self, actor):
        """Sets the actor of this Tag.

        id of the actor that controlls the address

        :param actor: The actor of this Tag.
        :type actor: str
        """

        self._actor = actor

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
    def confidence(self):
        """Gets the confidence of this Tag.

        Confidence name

        :return: The confidence of this Tag.
        :rtype: str
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        """Sets the confidence of this Tag.

        Confidence name

        :param confidence: The confidence of this Tag.
        :type confidence: str
        """

        self._confidence = confidence

    @property
    def confidence_level(self):
        """Gets the confidence_level of this Tag.

        Confidence level

        :return: The confidence_level of this Tag.
        :rtype: int
        """
        return self._confidence_level

    @confidence_level.setter
    def confidence_level(self, confidence_level):
        """Sets the confidence_level of this Tag.

        Confidence level

        :param confidence_level: The confidence_level of this Tag.
        :type confidence_level: int
        """

        self._confidence_level = confidence_level

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
    def is_cluster_definer(self):
        """Gets the is_cluster_definer of this Tag.

        whether the address tag applies to the entity level

        :return: The is_cluster_definer of this Tag.
        :rtype: bool
        """
        return self._is_cluster_definer

    @is_cluster_definer.setter
    def is_cluster_definer(self, is_cluster_definer):
        """Sets the is_cluster_definer of this Tag.

        whether the address tag applies to the entity level

        :param is_cluster_definer: The is_cluster_definer of this Tag.
        :type is_cluster_definer: bool
        """
        if is_cluster_definer is None:
            raise ValueError("Invalid value for `is_cluster_definer`, must not be `None`")

        self._is_cluster_definer = is_cluster_definer

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
    def tagpack_creator(self):
        """Gets the tagpack_creator of this Tag.

        Tagpack creator

        :return: The tagpack_creator of this Tag.
        :rtype: str
        """
        return self._tagpack_creator

    @tagpack_creator.setter
    def tagpack_creator(self, tagpack_creator):
        """Sets the tagpack_creator of this Tag.

        Tagpack creator

        :param tagpack_creator: The tagpack_creator of this Tag.
        :type tagpack_creator: str
        """
        if tagpack_creator is None:
            raise ValueError("Invalid value for `tagpack_creator`, must not be `None`")

        self._tagpack_creator = tagpack_creator

    @property
    def tagpack_is_public(self):
        """Gets the tagpack_is_public of this Tag.

        whether the address is public

        :return: The tagpack_is_public of this Tag.
        :rtype: bool
        """
        return self._tagpack_is_public

    @tagpack_is_public.setter
    def tagpack_is_public(self, tagpack_is_public):
        """Sets the tagpack_is_public of this Tag.

        whether the address is public

        :param tagpack_is_public: The tagpack_is_public of this Tag.
        :type tagpack_is_public: bool
        """
        if tagpack_is_public is None:
            raise ValueError("Invalid value for `tagpack_is_public`, must not be `None`")

        self._tagpack_is_public = tagpack_is_public

    @property
    def tagpack_title(self):
        """Gets the tagpack_title of this Tag.

        Tagpack title

        :return: The tagpack_title of this Tag.
        :rtype: str
        """
        return self._tagpack_title

    @tagpack_title.setter
    def tagpack_title(self, tagpack_title):
        """Sets the tagpack_title of this Tag.

        Tagpack title

        :param tagpack_title: The tagpack_title of this Tag.
        :type tagpack_title: str
        """
        if tagpack_title is None:
            raise ValueError("Invalid value for `tagpack_title`, must not be `None`")

        self._tagpack_title = tagpack_title

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
