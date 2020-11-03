import connexion
import six

from openapi_server.models.entity_addresses import EntityAddresses  # noqa: E501
from openapi_server.models.entity_with_tags import EntityWithTags  # noqa: E501
from openapi_server.models.neighbors import Neighbors  # noqa: E501
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


def list_entity_addresses(currency, entity, page=None, pagesize=None):  # noqa: E501
    """Get an entity&#39;s addresses

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

    :rtype: EntityAddresses
    """
    try:
      return service.list_entity_addresses(currency, entity, page, pagesize)
    except RuntimeError as e:
      return notfound(str(e))
from gsrest.service.problems import notfound


def list_entity_neighbors(currency, entity, direction, targets=None, page=None, pagesize=None):  # noqa: E501
    """Get an entity&#39;s neighbors in the entity graph

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param direction: Incoming or outgoing neighbors
    :type direction: str
    :param targets: Restrict result to given set of comma separated IDs
    :type targets: List[int]
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

    :rtype: Neighbors
    """
    try:
      return service.list_entity_neighbors(currency, entity, direction, targets, page, pagesize)
    except RuntimeError as e:
      return notfound(str(e))
from gsrest.service.problems import notfound


def list_entity_neighbors_csv(currency, entity, direction):  # noqa: E501
    """Get an entity&#39;s neighbors in the entity graph as CSV

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param direction: Incoming or outgoing neighbors
    :type direction: str

    :rtype: str
    """
    try:
      return service.list_entity_neighbors_csv(currency, entity, direction)
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
