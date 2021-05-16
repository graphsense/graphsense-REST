import connexion
import six

from openapi_server.models.address_tag import AddressTag  # noqa: E501
from openapi_server.models.address_txs import AddressTxs  # noqa: E501
from openapi_server.models.address_with_tags import AddressWithTags  # noqa: E501
from openapi_server.models.entity_with_tags import EntityWithTags  # noqa: E501
from openapi_server.models.link import Link  # noqa: E501
from openapi_server.models.neighbors import Neighbors  # noqa: E501
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
        return service.get_address_entity(
            currency=currency,
            address=address)
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
        return service.get_address_with_tags(
            currency=currency,
            address=address)
    except RuntimeError as e:
        return notfound(str(e))


def list_address_links(currency, address, neighbor):  # noqa: E501
    """Get transactions between two addresses

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
        return service.list_address_links(
            currency=currency,
            address=address,
            neighbor=neighbor)
    except RuntimeError as e:
        return notfound(str(e))


def list_address_links_csv(currency, address, neighbor):  # noqa: E501
    """Get transactions between two addresses as CSV

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param neighbor: Neighbor address
    :type neighbor: str

    :rtype: str
    """
    try:
        return service.list_address_links_csv(
            currency=currency,
            address=address,
            neighbor=neighbor)
    except RuntimeError as e:
        return notfound(str(e))


def list_address_links_csv_eth(address, neighbor):  # noqa: E501
    """Get transactions between two addresses as CSV

     # noqa: E501

    :param address: The cryptocurrency address in hexadecimal representation
    :type address: str
    :param neighbor: Neighbor address in hexadecimal representation
    :type neighbor: str

    :rtype: str
    """
    try:
        return service.list_address_links_csv_eth(
            address=address,
            neighbor=neighbor)
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
        return service.list_address_neighbors(
            currency=currency,
            address=address,
            direction=direction,
            page=page,
            pagesize=pagesize)
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
        return service.list_address_neighbors_csv(
            currency=currency,
            address=address,
            direction=direction)
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
        return service.list_address_txs(
            currency=currency,
            address=address,
            page=page,
            pagesize=pagesize)
    except RuntimeError as e:
        return notfound(str(e))


def list_address_txs_csv(currency, address):  # noqa: E501
    """Get all transactions an address has been involved in as CSV

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

    :rtype: str
    """
    try:
        return service.list_address_txs_csv(
            currency=currency,
            address=address)
    except RuntimeError as e:
        return notfound(str(e))


def list_tags_by_address(currency, address):  # noqa: E501
    """Get attribution tags for a given address

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

    :rtype: List[AddressTag]
    """
    try:
        return service.list_tags_by_address(
            currency=currency,
            address=address)
    except RuntimeError as e:
        return notfound(str(e))


def list_tags_by_address_csv(currency, address):  # noqa: E501
    """Get attribution tags for a given address

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

    :rtype: str
    """
    try:
        return service.list_tags_by_address_csv(
            currency=currency,
            address=address)
    except RuntimeError as e:
        return notfound(str(e))
