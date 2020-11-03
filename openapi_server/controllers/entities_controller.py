import connexion
import six

from openapi_server.models.entity_with_tags import EntityWithTags  # noqa: E501
from openapi_server.models.tag import Tag  # noqa: E501
from openapi_server import util
import gsrest.service.entities_service as service
from gsrest.service.problems import notfound


def get_entity_with_tags(currency, entity):  # noqa: E501
    """Get an entity with tags

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int

    :rtype: EntityWithTags
    """
    try:
      return service.get_entity_with_tags(currency, entity)
    except RuntimeError as e:
      return notfound(str(e))
from gsrest.service.problems import notfound


def list_entity_tags(currency, entity):  # noqa: E501
    """Get attribution tags for a given entity

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int

    :rtype: List[Tag]
    """
    try:
      return service.list_entity_tags(currency, entity)
    except RuntimeError as e:
      return notfound(str(e))
from gsrest.service.problems import notfound


def list_entity_tags_csv(currency, entity):  # noqa: E501
    """Get attribution tags for a given entity as CSV

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int

    :rtype: str
    """
    try:
      return service.list_entity_tags_csv(currency, entity)
    except RuntimeError as e:
      return notfound(str(e))
