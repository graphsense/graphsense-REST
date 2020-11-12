# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class StatsNote(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, note=None):  # noqa: E501
        """StatsNote - a model defined in OpenAPI

        :param note: The note of this StatsNote.  # noqa: E501
        :type note: str
        """
        self.openapi_types = {
            'note': str
        }

        self.attribute_map = {
            'note': 'note'
        }

        self._note = note

    @classmethod
    def from_dict(cls, dikt) -> 'StatsNote':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The stats_note of this StatsNote.  # noqa: E501
        :rtype: StatsNote
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The StatsNote as a dict
        :rtype: dict
        """
        return { 'note': self._note }


    @property
    def note(self):
        """Gets the note of this StatsNote.


        :return: The note of this StatsNote.
        :rtype: str
        """
        return self._note

    @note.setter
    def note(self, note):
        """Sets the note of this StatsNote.


        :param note: The note of this StatsNote.
        :type note: str
        """

        self._note = note
