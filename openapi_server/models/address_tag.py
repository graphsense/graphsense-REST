# coding: utf-8
from gsrest.errors import BadUserInputException
from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.address_tag_all_of import AddressTagAllOf
from openapi_server.models.tag import Tag
from openapi_server import util


class AddressTag(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(
        self,
        label: str = None,
        category: str = None,
        concepts: List[str] = None,
        actor: str = None,
        abuse: str = None,
        tagpack_uri: str = None,
        source: str = None,
        lastmod: int = None,
        tagpack_title: str = None,
        tagpack_is_public: bool = None,
        tagpack_creator: str = None,
        is_cluster_definer: bool = None,
        confidence: str = None,
        confidence_level: int = None,
        inherited_from: str = None,
        currency: str = None,
        address: str = None,
    ):
        """AddressTag - a model defined in OpenAPI

        :param label: The label of this AddressTag.
        :param category: The category of this AddressTag.
        :param concepts: The concepts of this AddressTag.
        :param actor: The actor of this AddressTag.
        :param abuse: The abuse of this AddressTag.
        :param tagpack_uri: The tagpack_uri of this AddressTag.
        :param source: The source of this AddressTag.
        :param lastmod: The lastmod of this AddressTag.
        :param tagpack_title: The tagpack_title of this AddressTag.
        :param tagpack_is_public: The tagpack_is_public of this AddressTag.
        :param tagpack_creator: The tagpack_creator of this AddressTag.
        :param is_cluster_definer: The is_cluster_definer of this AddressTag.
        :param confidence: The confidence of this AddressTag.
        :param confidence_level: The confidence_level of this AddressTag.
        :param inherited_from: The inherited_from of this AddressTag.
        :param currency: The currency of this AddressTag.
        :param address: The address of this AddressTag.
        """
        self.openapi_types = {
            "label": str,
            "category": str,
            "concepts": List[str],
            "actor": str,
            "abuse": str,
            "tagpack_uri": str,
            "source": str,
            "lastmod": int,
            "tagpack_title": str,
            "tagpack_is_public": bool,
            "tagpack_creator": str,
            "is_cluster_definer": bool,
            "confidence": str,
            "confidence_level": int,
            "inherited_from": str,
            "currency": str,
            "address": str,
        }

        self.attribute_map = {
            "label": "label",
            "category": "category",
            "concepts": "concepts",
            "actor": "actor",
            "abuse": "abuse",
            "tagpack_uri": "tagpack_uri",
            "source": "source",
            "lastmod": "lastmod",
            "tagpack_title": "tagpack_title",
            "tagpack_is_public": "tagpack_is_public",
            "tagpack_creator": "tagpack_creator",
            "is_cluster_definer": "is_cluster_definer",
            "confidence": "confidence",
            "confidence_level": "confidence_level",
            "inherited_from": "inherited_from",
            "currency": "currency",
            "address": "address",
        }

        self._label = label
        self._category = category
        self._concepts = concepts
        self._actor = actor
        self._abuse = abuse
        self._tagpack_uri = tagpack_uri
        self._source = source
        self._lastmod = lastmod
        self._tagpack_title = tagpack_title
        self._tagpack_is_public = tagpack_is_public
        self._tagpack_creator = tagpack_creator
        self._is_cluster_definer = is_cluster_definer
        self._confidence = confidence
        self._confidence_level = confidence_level
        self._inherited_from = inherited_from
        self._currency = currency
        self._address = address

    @classmethod
    def from_dict(cls, dikt: dict) -> "AddressTag":
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The address_tag of this AddressTag.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The AddressTag as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return {
            "label": self._label,
            "category": self._category,
            "concepts": self._concepts,
            "actor": self._actor,
            "abuse": self._abuse,
            "tagpack_uri": self._tagpack_uri,
            "source": self._source,
            "lastmod": self._lastmod,
            "tagpack_title": self._tagpack_title,
            "tagpack_is_public": self._tagpack_is_public,
            "tagpack_creator": self._tagpack_creator,
            "is_cluster_definer": self._is_cluster_definer,
            "confidence": self._confidence,
            "confidence_level": self._confidence_level,
            "inherited_from": self._inherited_from,
            "currency": self._currency,
            "address": self._address,
        }

    @property
    def label(self):
        """Gets the label of this AddressTag.

        Label

        :return: The label of this AddressTag.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this AddressTag.

        Label

        :param label: The label of this AddressTag.
        :type label: str
        """
        if label is None:
            raise BadUserInputException("Invalid value for `label`, must not be `None`")

        self._label = label

    @property
    def category(self):
        """Gets the category of this AddressTag.

        Category

        :return: The category of this AddressTag.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this AddressTag.

        Category

        :param category: The category of this AddressTag.
        :type category: str
        """

        self._category = category

    @property
    def concepts(self):
        """Gets the concepts of this AddressTag.

        A list additional concepts/categories

        :return: The concepts of this AddressTag.
        :rtype: List[str]
        """
        return self._concepts

    @concepts.setter
    def concepts(self, concepts):
        """Sets the concepts of this AddressTag.

        A list additional concepts/categories

        :param concepts: The concepts of this AddressTag.
        :type concepts: List[str]
        """

        self._concepts = concepts

    @property
    def actor(self):
        """Gets the actor of this AddressTag.

        id of the actor that controlls the address

        :return: The actor of this AddressTag.
        :rtype: str
        """
        return self._actor

    @actor.setter
    def actor(self, actor):
        """Sets the actor of this AddressTag.

        id of the actor that controlls the address

        :param actor: The actor of this AddressTag.
        :type actor: str
        """

        self._actor = actor

    @property
    def abuse(self):
        """Gets the abuse of this AddressTag.

        Abuses

        :return: The abuse of this AddressTag.
        :rtype: str
        """
        return self._abuse

    @abuse.setter
    def abuse(self, abuse):
        """Sets the abuse of this AddressTag.

        Abuses

        :param abuse: The abuse of this AddressTag.
        :type abuse: str
        """

        self._abuse = abuse

    @property
    def tagpack_uri(self):
        """Gets the tagpack_uri of this AddressTag.

        Tagpack URI

        :return: The tagpack_uri of this AddressTag.
        :rtype: str
        """
        return self._tagpack_uri

    @tagpack_uri.setter
    def tagpack_uri(self, tagpack_uri):
        """Sets the tagpack_uri of this AddressTag.

        Tagpack URI

        :param tagpack_uri: The tagpack_uri of this AddressTag.
        :type tagpack_uri: str
        """

        self._tagpack_uri = tagpack_uri

    @property
    def source(self):
        """Gets the source of this AddressTag.

        Source

        :return: The source of this AddressTag.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this AddressTag.

        Source

        :param source: The source of this AddressTag.
        :type source: str
        """

        self._source = source

    @property
    def lastmod(self):
        """Gets the lastmod of this AddressTag.

        Last modified

        :return: The lastmod of this AddressTag.
        :rtype: int
        """
        return self._lastmod

    @lastmod.setter
    def lastmod(self, lastmod):
        """Sets the lastmod of this AddressTag.

        Last modified

        :param lastmod: The lastmod of this AddressTag.
        :type lastmod: int
        """

        self._lastmod = lastmod

    @property
    def tagpack_title(self):
        """Gets the tagpack_title of this AddressTag.

        Tagpack title

        :return: The tagpack_title of this AddressTag.
        :rtype: str
        """
        return self._tagpack_title

    @tagpack_title.setter
    def tagpack_title(self, tagpack_title):
        """Sets the tagpack_title of this AddressTag.

        Tagpack title

        :param tagpack_title: The tagpack_title of this AddressTag.
        :type tagpack_title: str
        """
        if tagpack_title is None:
            raise BadUserInputException(
                "Invalid value for `tagpack_title`, must not be `None`"
            )

        self._tagpack_title = tagpack_title

    @property
    def tagpack_is_public(self):
        """Gets the tagpack_is_public of this AddressTag.

        whether the address is public

        :return: The tagpack_is_public of this AddressTag.
        :rtype: bool
        """
        return self._tagpack_is_public

    @tagpack_is_public.setter
    def tagpack_is_public(self, tagpack_is_public):
        """Sets the tagpack_is_public of this AddressTag.

        whether the address is public

        :param tagpack_is_public: The tagpack_is_public of this AddressTag.
        :type tagpack_is_public: bool
        """
        if tagpack_is_public is None:
            raise BadUserInputException(
                "Invalid value for `tagpack_is_public`, must not be `None`"
            )

        self._tagpack_is_public = tagpack_is_public

    @property
    def tagpack_creator(self):
        """Gets the tagpack_creator of this AddressTag.

        Tagpack creator

        :return: The tagpack_creator of this AddressTag.
        :rtype: str
        """
        return self._tagpack_creator

    @tagpack_creator.setter
    def tagpack_creator(self, tagpack_creator):
        """Sets the tagpack_creator of this AddressTag.

        Tagpack creator

        :param tagpack_creator: The tagpack_creator of this AddressTag.
        :type tagpack_creator: str
        """
        if tagpack_creator is None:
            raise BadUserInputException(
                "Invalid value for `tagpack_creator`, must not be `None`"
            )

        self._tagpack_creator = tagpack_creator

    @property
    def is_cluster_definer(self):
        """Gets the is_cluster_definer of this AddressTag.

        whether the address tag applies to the entity level

        :return: The is_cluster_definer of this AddressTag.
        :rtype: bool
        """
        return self._is_cluster_definer

    @is_cluster_definer.setter
    def is_cluster_definer(self, is_cluster_definer):
        """Sets the is_cluster_definer of this AddressTag.

        whether the address tag applies to the entity level

        :param is_cluster_definer: The is_cluster_definer of this AddressTag.
        :type is_cluster_definer: bool
        """
        if is_cluster_definer is None:
            raise BadUserInputException(
                "Invalid value for `is_cluster_definer`, must not be `None`"
            )

        self._is_cluster_definer = is_cluster_definer

    @property
    def confidence(self):
        """Gets the confidence of this AddressTag.

        Confidence name

        :return: The confidence of this AddressTag.
        :rtype: str
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        """Sets the confidence of this AddressTag.

        Confidence name

        :param confidence: The confidence of this AddressTag.
        :type confidence: str
        """

        self._confidence = confidence

    @property
    def confidence_level(self):
        """Gets the confidence_level of this AddressTag.

        Confidence level

        :return: The confidence_level of this AddressTag.
        :rtype: int
        """
        return self._confidence_level

    @confidence_level.setter
    def confidence_level(self, confidence_level):
        """Sets the confidence_level of this AddressTag.

        Confidence level

        :param confidence_level: The confidence_level of this AddressTag.
        :type confidence_level: int
        """

        self._confidence_level = confidence_level

    @property
    def inherited_from(self):
        """Gets the inherited_from of this AddressTag.

        if the tag was inherited from cluster

        :return: The inherited_from of this AddressTag.
        :rtype: str
        """
        return self._inherited_from

    @inherited_from.setter
    def inherited_from(self, inherited_from):
        """Sets the inherited_from of this AddressTag.

        if the tag was inherited from cluster

        :param inherited_from: The inherited_from of this AddressTag.
        :type inherited_from: str
        """
        allowed_values = ["cluster"]  # noqa: E501
        if inherited_from not in allowed_values:
            raise BadUserInputException(
                "Invalid value for `inherited_from` ({0}), must be one of {1}".format(
                    inherited_from, allowed_values
                )
            )

        self._inherited_from = inherited_from

    @property
    def currency(self):
        """Gets the currency of this AddressTag.

        crypto currency code

        :return: The currency of this AddressTag.
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this AddressTag.

        crypto currency code

        :param currency: The currency of this AddressTag.
        :type currency: str
        """
        if currency is None:
            raise BadUserInputException(
                "Invalid value for `currency`, must not be `None`"
            )

        self._currency = currency

    @property
    def address(self):
        """Gets the address of this AddressTag.

        Address

        :return: The address of this AddressTag.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this AddressTag.

        Address

        :param address: The address of this AddressTag.
        :type address: str
        """
        if address is None:
            raise BadUserInputException(
                "Invalid value for `address`, must not be `None`"
            )

        self._address = address
