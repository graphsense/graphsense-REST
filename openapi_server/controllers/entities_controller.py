import connexion
import six

from openapi_server.models.entity_with_tags import EntityWithTags  # noqa: E501
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
