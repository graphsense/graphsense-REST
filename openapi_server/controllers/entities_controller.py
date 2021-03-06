from openapi_server.models.entity_addresses import EntityAddresses  # noqa: E501
from openapi_server.models.entity_with_tags import EntityWithTags  # noqa: E501
from openapi_server.models.neighbors import Neighbors  # noqa: E501
from openapi_server.models.search_paths import SearchPaths  # noqa: E501
from openapi_server.models.tag import Tag  # noqa: E501
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
        return service.get_entity_with_tags(
            currency=currency,
            entity=entity)
    except RuntimeError as e:
        return notfound(str(e))


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
        return service.list_entity_addresses(
            currency=currency,
            entity=entity,
            page=page,
            pagesize=pagesize)
    except RuntimeError as e:
        return notfound(str(e))


def list_entity_addresses_csv(currency, entity):  # noqa: E501
    """Get an entity&#39;s addresses as CSV

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int

    :rtype: str
    """
    try:
        return service.list_entity_addresses_csv(
            currency=currency,
            entity=entity)
    except RuntimeError as e:
        return notfound(str(e))


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
        return service.list_entity_neighbors(
            currency=currency,
            entity=entity,
            direction=direction,
            targets=targets,
            page=page,
            pagesize=pagesize)
    except RuntimeError as e:
        return notfound(str(e))


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
        return service.list_entity_neighbors_csv(
            currency=currency,
            entity=entity,
            direction=direction)
    except RuntimeError as e:
        return notfound(str(e))


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
        return service.list_entity_tags(
            currency=currency,
            entity=entity)
    except RuntimeError as e:
        return notfound(str(e))


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
        return service.list_entity_tags_csv(
            currency=currency,
            entity=entity)
    except RuntimeError as e:
        return notfound(str(e))


def search_entity_neighbors(currency, entity, direction, key, value, depth, breadth=None, skip_num_addresses=None):  # noqa: E501
    """Search deeply for matching neighbors

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param direction: Incoming or outgoing neighbors
    :type direction: str
    :param key: Match neighbors against one and only one of these properties: - the category the entity belongs to - addresses the entity contains - total_received: amount the entity received in total - balance: amount the entity holds finally
    :type key: str
    :param value: If key is - category: comma separated list of category names - addresses: comma separated list of address IDs - total_received/balance: comma separated tuple of (currency, min, max)
    :type value: List[str]
    :param depth: How many hops should the transaction graph be searched
    :type depth: int
    :param breadth: How many siblings of each neighbor should be tried
    :type breadth: int
    :param skip_num_addresses: Skip entities containing more addresses
    :type skip_num_addresses: int

    :rtype: SearchPaths
    """
    try:
        return service.search_entity_neighbors(
            currency=currency,
            entity=entity,
            direction=direction,
            key=key,
            value=value,
            depth=depth,
            breadth=breadth,
            skip_num_addresses=skip_num_addresses)
    except RuntimeError as e:
        return notfound(str(e))
