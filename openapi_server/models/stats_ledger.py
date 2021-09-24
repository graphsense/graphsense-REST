# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.stats_ledger_version import StatsLedgerVersion
from openapi_server import util

from openapi_server.models.stats_ledger_version import StatsLedgerVersion  # noqa: E501

class StatsLedger(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, report_uuid=None, version=None, visible_name=None):  # noqa: E501
        """StatsLedger - a model defined in OpenAPI

        :param id: The id of this StatsLedger.  # noqa: E501
        :type id: str
        :param report_uuid: The report_uuid of this StatsLedger.  # noqa: E501
        :type report_uuid: str
        :param version: The version of this StatsLedger.  # noqa: E501
        :type version: StatsLedgerVersion
        :param visible_name: The visible_name of this StatsLedger.  # noqa: E501
        :type visible_name: str
        """
        self.openapi_types = {
            'id': str,
            'report_uuid': str,
            'version': StatsLedgerVersion,
            'visible_name': str
        }

        self.attribute_map = {
            'id': 'id',
            'report_uuid': 'report_uuid',
            'version': 'version',
            'visible_name': 'visible_name'
        }

        self._id = id
        self._report_uuid = report_uuid
        self._version = version
        self._visible_name = visible_name

    @classmethod
    def from_dict(cls, dikt) -> 'StatsLedger':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The stats_ledger of this StatsLedger.  # noqa: E501
        :rtype: StatsLedger
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The StatsLedger as a dict
        :rtype: dict
        """
        return { 'id': self._id,
            'report_uuid': self._report_uuid,
            'version': self._version,
            'visible_name': self._visible_name }


    @property
    def id(self):
        """Gets the id of this StatsLedger.


        :return: The id of this StatsLedger.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this StatsLedger.


        :param id: The id of this StatsLedger.
        :type id: str
        """

        self._id = id

    @property
    def report_uuid(self):
        """Gets the report_uuid of this StatsLedger.


        :return: The report_uuid of this StatsLedger.
        :rtype: str
        """
        return self._report_uuid

    @report_uuid.setter
    def report_uuid(self, report_uuid):
        """Sets the report_uuid of this StatsLedger.


        :param report_uuid: The report_uuid of this StatsLedger.
        :type report_uuid: str
        """

        self._report_uuid = report_uuid

    @property
    def version(self):
        """Gets the version of this StatsLedger.


        :return: The version of this StatsLedger.
        :rtype: StatsLedgerVersion
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this StatsLedger.


        :param version: The version of this StatsLedger.
        :type version: StatsLedgerVersion
        """

        self._version = version

    @property
    def visible_name(self):
        """Gets the visible_name of this StatsLedger.


        :return: The visible_name of this StatsLedger.
        :rtype: str
        """
        return self._visible_name

    @visible_name.setter
    def visible_name(self, visible_name):
        """Sets the visible_name of this StatsLedger.


        :param visible_name: The visible_name of this StatsLedger.
        :type visible_name: str
        """

        self._visible_name = visible_name
