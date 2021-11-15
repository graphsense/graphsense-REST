# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server import util


class StatsNote(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, note: str=None):
        """StatsNote - a model defined in OpenAPI

        :param note: The note of this StatsNote.
        """
        self.openapi_types = {
            'note': str
        }

        self.attribute_map = {
            'note': 'note'
        }

        self._note = note

    @classmethod
    def from_dict(cls, dikt: dict) -> 'StatsNote':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The stats_note of this StatsNote.
        """
        return util.deserialize_model(dikt, cls)

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
