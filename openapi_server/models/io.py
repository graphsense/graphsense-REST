# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Io(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    INPUTS = "inputs"
    OUTPUTS = "outputs"
    def __init__(self):  # noqa: E501
        """Io - a model defined in OpenAPI

        """
        self.openapi_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'Io':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The io of this Io.  # noqa: E501
        :rtype: Io
        """
        return util.deserialize_model(dikt, cls)

    def to_dict(self, prefix=""):
        """Returns the model as a dict:

        :return: The Io as a dict
        :rtype: dict
        """
        return 
