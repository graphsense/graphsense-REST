# coding: utf-8

from datetime import date, datetime

from typing import List, Dict, Type

from openapi_server.models.base_model_ import Model
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.entity_tag import EntityTag
from openapi_server import util


class AddressAndEntityTags(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, address_tags: List[AddressTag]=None, entity_tags: List[EntityTag]=None):
        """AddressAndEntityTags - a model defined in OpenAPI

        :param address_tags: The address_tags of this AddressAndEntityTags.
        :param entity_tags: The entity_tags of this AddressAndEntityTags.
        """
        self.openapi_types = {
            'address_tags': List[AddressTag],
            'entity_tags': List[EntityTag]
        }

        self.attribute_map = {
            'address_tags': 'address_tags',
            'entity_tags': 'entity_tags'
        }

        self._address_tags = address_tags
        self._entity_tags = entity_tags

    @classmethod
    def from_dict(cls, dikt: dict) -> 'AddressAndEntityTags':
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The address_and_entity_tags of this AddressAndEntityTags.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def address_tags(self):
        """Gets the address_tags of this AddressAndEntityTags.

        First page of address tags of this entity

        :return: The address_tags of this AddressAndEntityTags.
        :rtype: List[AddressTag]
        """
        return self._address_tags

    @address_tags.setter
    def address_tags(self, address_tags):
        """Sets the address_tags of this AddressAndEntityTags.

        First page of address tags of this entity

        :param address_tags: The address_tags of this AddressAndEntityTags.
        :type address_tags: List[AddressTag]
        """
        if address_tags is None:
            raise ValueError("Invalid value for `address_tags`, must not be `None`")

        self._address_tags = address_tags

    @property
    def entity_tags(self):
        """Gets the entity_tags of this AddressAndEntityTags.

        First page of entity tags of this entity

        :return: The entity_tags of this AddressAndEntityTags.
        :rtype: List[EntityTag]
        """
        return self._entity_tags

    @entity_tags.setter
    def entity_tags(self, entity_tags):
        """Sets the entity_tags of this AddressAndEntityTags.

        First page of entity tags of this entity

        :param entity_tags: The entity_tags of this AddressAndEntityTags.
        :type entity_tags: List[EntityTag]
        """
        if entity_tags is None:
            raise ValueError("Invalid value for `entity_tags`, must not be `None`")

        self._entity_tags = entity_tags
