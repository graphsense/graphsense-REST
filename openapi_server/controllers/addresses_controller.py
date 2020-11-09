import connexion
import six

from openapi_server.models.address_txs import AddressTxs  # noqa: E501
from openapi_server.models.address_with_tags import AddressWithTags  # noqa: E501
from openapi_server.models.entity_with_tags import EntityWithTags  # noqa: E501
from openapi_server.models.link import Link  # noqa: E501
from openapi_server.models.neighbors import Neighbors  # noqa: E501
from openapi_server.models.tag import Tag  # noqa: E501
from openapi_server import util
import gsrest.service.addresses_service as service
from gsrest.service.problems import notfound


def get_address_entity(currency, address):  # noqa: E501
    """Get an address with tags

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

    :rtype: EntityWithTags
    """
    try:
      return service.get_address_entity(currency, address)
    except RuntimeError as e:
      return notfound(str(e))


def get_address_with_tags(currency, address):  # noqa: E501
    """Get an address with tags

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

    :rtype: AddressWithTags
    """
    try:
      return service.get_address_with_tags(currency, address)
    except RuntimeError as e:
      return notfound(str(e))


def list_address_links(currency, address, neighbor):  # noqa: E501
    """Get transactions between to addresses

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param neighbor: Neighbor address
    :type neighbor: str

    :rtype: List[Link]
    """
    try:
      return service.list_address_links(currency, address, neighbor)
    except RuntimeError as e:
      return notfound(str(e))


def list_address_neighbors(currency, address, direction, page=None, pagesize=None):  # noqa: E501
    """Get an addresses&#39; neighbors in the address graph

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param direction: Incoming or outgoing neighbors
    :type direction: str
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

    :rtype: Neighbors
    """
    try:
      return service.list_address_neighbors(currency, address, direction, page, pagesize)
    except RuntimeError as e:
      return notfound(str(e))


def list_address_neighbors_csv(currency, address, direction):  # noqa: E501
    """Get an addresses&#39; neighbors in the address graph as CSV

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param direction: Incoming or outgoing neighbors
    :type direction: str

    :rtype: str
    """
    try:
      return service.list_address_neighbors_csv(currency, address, direction)
    except RuntimeError as e:
      return notfound(str(e))


def list_address_tags(currency, address):  # noqa: E501
    """Get attribution tags for a given address

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

    :rtype: List[Tag]
    """
    try:
      return service.list_address_tags(currency, address)
    except RuntimeError as e:
      return notfound(str(e))


def list_address_tags_csv(currency, address):  # noqa: E501
    """Get attribution tags for a given address

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

    :rtype: str
    """
    try:
      return service.list_address_tags_csv(currency, address)
    except RuntimeError as e:
      return notfound(str(e))


def list_address_txs(currency, address, page=None, pagesize=None):  # noqa: E501
    """Get all transactions an address has been involved in

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

    :rtype: AddressTxs
    """
    try:
      return service.list_address_txs(currency, address, page, pagesize)
    except RuntimeError as e:
      return notfound(str(e))
