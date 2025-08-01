# coding: utf-8
from gsrest.errors import BadUserInputException
from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.label_summary import LabelSummary
from openapi_server.models.tag_cloud_entry import TagCloudEntry
from openapi_server import util


class TagSummary(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, broad_category: str=None, tag_count: int=None, tag_count_indirect: int=None, best_actor: str=None, best_label: str=None, label_summary: Dict[str, LabelSummary]=None, concept_tag_cloud: Dict[str, TagCloudEntry]=None):
        """TagSummary - a model defined in OpenAPI

        :param broad_category: The broad_category of this TagSummary.
        :param tag_count: The tag_count of this TagSummary.
        :param tag_count_indirect: The tag_count_indirect of this TagSummary.
        :param best_actor: The best_actor of this TagSummary.
        :param best_label: The best_label of this TagSummary.
        :param label_summary: The label_summary of this TagSummary.
        :param concept_tag_cloud: The concept_tag_cloud of this TagSummary.
        """
        self.openapi_types = {
            'broad_category': str,
            'tag_count': int,
            'tag_count_indirect': int,
            'best_actor': str,
            'best_label': str,
            'label_summary': Dict[str, LabelSummary],
            'concept_tag_cloud': Dict[str, TagCloudEntry]
        }

        self.attribute_map = {
            'broad_category': 'broad_category',
            'tag_count': 'tag_count',
            'tag_count_indirect': 'tag_count_indirect',
            'best_actor': 'best_actor',
            'best_label': 'best_label',
            'label_summary': 'label_summary',
            'concept_tag_cloud': 'concept_tag_cloud'
        }

        self._broad_category = broad_category
        self._tag_count = tag_count
        self._tag_count_indirect = tag_count_indirect
        self._best_actor = best_actor
        self._best_label = best_label
        self._label_summary = label_summary
        self._concept_tag_cloud = concept_tag_cloud

    @classmethod
    def from_dict(cls, dikt: dict) -> 'TagSummary':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The tag_summary of this TagSummary.
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, shallow=False):
        """Returns the model as a dict:

        :return: The TagSummary as a dict
        :rtype: dict
        """
        if not shallow:
            return Model.to_dict(self)
        return { 'broad_category': self._broad_category,
            'tag_count': self._tag_count,
            'tag_count_indirect': self._tag_count_indirect,
            'best_actor': self._best_actor,
            'best_label': self._best_label,
            'label_summary': self._label_summary,
            'concept_tag_cloud': self._concept_tag_cloud }


    @property
    def broad_category(self):
        """Gets the broad_category of this TagSummary.


        :return: The broad_category of this TagSummary.
        :rtype: str
        """
        return self._broad_category

    @broad_category.setter
    def broad_category(self, broad_category):
        """Sets the broad_category of this TagSummary.


        :param broad_category: The broad_category of this TagSummary.
        :type broad_category: str
        """
        if broad_category is None:
            raise BadUserInputException("Invalid value for `broad_category`, must not be `None`")

        self._broad_category = broad_category

    @property
    def tag_count(self):
        """Gets the tag_count of this TagSummary.


        :return: The tag_count of this TagSummary.
        :rtype: int
        """
        return self._tag_count

    @tag_count.setter
    def tag_count(self, tag_count):
        """Sets the tag_count of this TagSummary.


        :param tag_count: The tag_count of this TagSummary.
        :type tag_count: int
        """
        if tag_count is None:
            raise BadUserInputException("Invalid value for `tag_count`, must not be `None`")

        self._tag_count = tag_count

    @property
    def tag_count_indirect(self):
        """Gets the tag_count_indirect of this TagSummary.


        :return: The tag_count_indirect of this TagSummary.
        :rtype: int
        """
        return self._tag_count_indirect

    @tag_count_indirect.setter
    def tag_count_indirect(self, tag_count_indirect):
        """Sets the tag_count_indirect of this TagSummary.


        :param tag_count_indirect: The tag_count_indirect of this TagSummary.
        :type tag_count_indirect: int
        """

        self._tag_count_indirect = tag_count_indirect

    @property
    def best_actor(self):
        """Gets the best_actor of this TagSummary.


        :return: The best_actor of this TagSummary.
        :rtype: str
        """
        return self._best_actor

    @best_actor.setter
    def best_actor(self, best_actor):
        """Sets the best_actor of this TagSummary.


        :param best_actor: The best_actor of this TagSummary.
        :type best_actor: str
        """

        self._best_actor = best_actor

    @property
    def best_label(self):
        """Gets the best_label of this TagSummary.


        :return: The best_label of this TagSummary.
        :rtype: str
        """
        return self._best_label

    @best_label.setter
    def best_label(self, best_label):
        """Sets the best_label of this TagSummary.


        :param best_label: The best_label of this TagSummary.
        :type best_label: str
        """

        self._best_label = best_label

    @property
    def label_summary(self):
        """Gets the label_summary of this TagSummary.


        :return: The label_summary of this TagSummary.
        :rtype: Dict[str, LabelSummary]
        """
        return self._label_summary

    @label_summary.setter
    def label_summary(self, label_summary):
        """Sets the label_summary of this TagSummary.


        :param label_summary: The label_summary of this TagSummary.
        :type label_summary: Dict[str, LabelSummary]
        """
        if label_summary is None:
            raise BadUserInputException("Invalid value for `label_summary`, must not be `None`")

        self._label_summary = label_summary

    @property
    def concept_tag_cloud(self):
        """Gets the concept_tag_cloud of this TagSummary.


        :return: The concept_tag_cloud of this TagSummary.
        :rtype: Dict[str, TagCloudEntry]
        """
        return self._concept_tag_cloud

    @concept_tag_cloud.setter
    def concept_tag_cloud(self, concept_tag_cloud):
        """Sets the concept_tag_cloud of this TagSummary.


        :param concept_tag_cloud: The concept_tag_cloud of this TagSummary.
        :type concept_tag_cloud: Dict[str, TagCloudEntry]
        """
        if concept_tag_cloud is None:
            raise BadUserInputException("Invalid value for `concept_tag_cloud`, must not be `None`")

        self._concept_tag_cloud = concept_tag_cloud
