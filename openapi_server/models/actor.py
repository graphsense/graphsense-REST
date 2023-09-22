# coding: utf-8
from gsrest.errors import BadUserInputException
from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.actor_context import ActorContext
from openapi_server.models.labeled_item_ref import LabeledItemRef
from openapi_server import util


class Actor(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, categories: List[LabeledItemRef]=None, context: ActorContext=None, id: str=None, jurisdictions: List[LabeledItemRef]=None, label: str=None, nr_tags: int=None, uri: str=None):
        """Actor - a model defined in OpenAPI

        :param categories: The categories of this Actor.
        :param context: The context of this Actor.
        :param id: The id of this Actor.
        :param jurisdictions: The jurisdictions of this Actor.
        :param label: The label of this Actor.
        :param nr_tags: The nr_tags of this Actor.
        :param uri: The uri of this Actor.
        """
        self.openapi_types = {
            'categories': List[LabeledItemRef],
            'context': ActorContext,
            'id': str,
            'jurisdictions': List[LabeledItemRef],
            'label': str,
            'nr_tags': int,
            'uri': str
        }

        self.attribute_map = {
            'categories': 'categories',
            'context': 'context',
            'id': 'id',
            'jurisdictions': 'jurisdictions',
            'label': 'label',
            'nr_tags': 'nr_tags',
            'uri': 'uri'
        }

        self._categories = categories
        self._context = context
        self._id = id
        self._jurisdictions = jurisdictions
        self._label = label
        self._nr_tags = nr_tags
        self._uri = uri

    @classmethod
    def from_dict(cls, dikt: dict) -> 'Actor':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The actor of this Actor.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The Actor as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'categories': self._categories,
            'context': self._context,
            'id': self._id,
            'jurisdictions': self._jurisdictions,
            'label': self._label,
            'nr_tags': self._nr_tags,
            'uri': self._uri }


    @property
    def categories(self):
        """Gets the categories of this Actor.

        A list actor categories

        :return: The categories of this Actor.
        :rtype: List[LabeledItemRef]
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """Sets the categories of this Actor.

        A list actor categories

        :param categories: The categories of this Actor.
        :type categories: List[LabeledItemRef]
        """
        if categories is None:
            raise BadUserInputException("Invalid value for `categories`, must not be `None`")

        self._categories = categories

    @property
    def context(self):
        """Gets the context of this Actor.


        :return: The context of this Actor.
        :rtype: ActorContext
        """
        return self._context

    @context.setter
    def context(self, context):
        """Sets the context of this Actor.


        :param context: The context of this Actor.
        :type context: ActorContext
        """

        self._context = context

    @property
    def id(self):
        """Gets the id of this Actor.

        Id of the actor

        :return: The id of this Actor.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Actor.

        Id of the actor

        :param id: The id of this Actor.
        :type id: str
        """
        if id is None:
            raise BadUserInputException("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def jurisdictions(self):
        """Gets the jurisdictions of this Actor.

        A list jurisdictions

        :return: The jurisdictions of this Actor.
        :rtype: List[LabeledItemRef]
        """
        return self._jurisdictions

    @jurisdictions.setter
    def jurisdictions(self, jurisdictions):
        """Sets the jurisdictions of this Actor.

        A list jurisdictions

        :param jurisdictions: The jurisdictions of this Actor.
        :type jurisdictions: List[LabeledItemRef]
        """
        if jurisdictions is None:
            raise BadUserInputException("Invalid value for `jurisdictions`, must not be `None`")

        self._jurisdictions = jurisdictions

    @property
    def label(self):
        """Gets the label of this Actor.

        Label

        :return: The label of this Actor.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this Actor.

        Label

        :param label: The label of this Actor.
        :type label: str
        """
        if label is None:
            raise BadUserInputException("Invalid value for `label`, must not be `None`")

        self._label = label

    @property
    def nr_tags(self):
        """Gets the nr_tags of this Actor.

        number of address tags of the actor

        :return: The nr_tags of this Actor.
        :rtype: int
        """
        return self._nr_tags

    @nr_tags.setter
    def nr_tags(self, nr_tags):
        """Sets the nr_tags of this Actor.

        number of address tags of the actor

        :param nr_tags: The nr_tags of this Actor.
        :type nr_tags: int
        """

        self._nr_tags = nr_tags

    @property
    def uri(self):
        """Gets the uri of this Actor.

        URI

        :return: The uri of this Actor.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this Actor.

        URI

        :param uri: The uri of this Actor.
        :type uri: str
        """
        if uri is None:
            raise BadUserInputException("Invalid value for `uri`, must not be `None`")

        self._uri = uri
