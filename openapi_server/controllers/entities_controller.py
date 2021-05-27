import connexion
import six
import traceback

from openapi_server.models.entities import Entities  # noqa: E501
from openapi_server.models.entity import Entity  # noqa: E501
from openapi_server.models.entity_addresses import EntityAddresses  # noqa: E501
from openapi_server.models.neighbors import Neighbors  # noqa: E501
from openapi_server.models.search_result_level1 import SearchResultLevel1  # noqa: E501
from openapi_server.models.tags import Tags  # noqa: E501
import gsrest.service.entities_service as service
from gsrest.service.problems import notfound, badrequest, internalerror


def get_entity(currency, entity, include_tags=None, tag_coherence=None):  # noqa: E501
    """Get an entity, optionally with tags

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param include_tags: Whether tags should be included
    :type include_tags: bool
    :param tag_coherence: Whether to calculate coherence of address tags
    :type tag_coherence: bool

    :rtype: Entity
    """
    try:
        return service.get_entity(
            currency=currency,
            entity=entity,
            include_tags=include_tags,
            tag_coherence=tag_coherence)
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror(str(e))


def list_entities(currency, ids=None, page=None, pagesize=None):  # noqa: E501
    """Get entities

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param ids: Restrict result to given set of comma separated IDs
    :type ids: List[str]
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

    :rtype: Entities
    """
    try:
        return service.list_entities(
            currency=currency,
            ids=ids,
            page=page,
            pagesize=pagesize)
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror(str(e))


def list_entities_csv(currency, ids):  # noqa: E501
    """Get entities as CSV

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param ids: Set of comma separated IDs
    :type ids: List[str]

    :rtype: str
    """
    try:
        return service.list_entities_csv(
            currency=currency,
            ids=ids)
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror(str(e))


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
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror(str(e))


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
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror(str(e))


def list_entity_neighbors(currency, entity, direction, ids=None, include_labels=None, page=None, pagesize=None):  # noqa: E501
    """Get an entity&#39;s neighbors in the entity graph

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param direction: Incoming or outgoing neighbors
    :type direction: str
    :param ids: Restrict result to given set of comma separated IDs
    :type ids: List[str]
    :param include_labels: Whether labels of tags should be included
    :type include_labels: bool
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
            ids=ids,
            include_labels=include_labels,
            page=page,
            pagesize=pagesize)
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror(str(e))


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
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror(str(e))


def list_tags_by_entity(currency, entity, tag_coherence=None):  # noqa: E501
    """Get tags for a given entity

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param tag_coherence: Whether to calculate coherence of address tags
    :type tag_coherence: bool

    :rtype: Tags
    """
    try:
        return service.list_tags_by_entity(
            currency=currency,
            entity=entity,
            tag_coherence=tag_coherence)
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror(str(e))


def list_tags_by_entity_by_level_csv(currency, entity, level):  # noqa: E501
    """Get address or entity tags for a given entity as CSV

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param level: Whether tags on the address or entity level are requested
    :type level: str

    :rtype: str
    """
    try:
        return service.list_tags_by_entity_by_level_csv(
            currency=currency,
            entity=entity,
            level=level)
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror(str(e))


def search_entity_neighbors(currency, entity, direction, key, value, depth, breadth=None, skip_num_addresses=None):  # noqa: E501
    """Search deeply for matching neighbors

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param direction: Incoming or outgoing neighbors
    :type direction: str
    :param key: Match neighbors against one and only one of these properties: - the category the entity belongs to - addresses the entity contains - entity ids - total_received: amount the entity received in total - balance: amount the entity holds finally
    :type key: str
    :param value: If key is - category: comma separated list of category names - addresses: comma separated list of address IDs - entities: comma separated list of entity IDs - total_received/balance: comma separated tuple of (currency, min, max)
    :type value: List[str]
    :param depth: How many hops should the transaction graph be searched
    :type depth: int
    :param breadth: How many siblings of each neighbor should be tried
    :type breadth: int
    :param skip_num_addresses: Skip entities containing more addresses
    :type skip_num_addresses: int

    :rtype: List[SearchResultLevel1]
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
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror(str(e))
