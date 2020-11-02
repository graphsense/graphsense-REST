import connexion
import six

from openapi_server.models.address_txs import AddressTxs  # noqa: E501
from openapi_server.models.address_with_tags import AddressWithTags  # noqa: E501
from openapi_server.models.neighbors import Neighbors  # noqa: E501
from openapi_server.models.tag import Tag  # noqa: E501
from openapi_server import util
import gsrest.service.addresses_service as service


def get_address_with_tags(currency, address):  # noqa: E501
    """Get an address with tags

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

    :rtype: AddressWithTags
    """
    return service.get_address_with_tags(currency, address)


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
    return service.list_address_neighbors(currency, address, direction, page, pagesize)


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
    return service.list_address_neighbors_csv(currency, address, direction)


def list_address_tags(currency, address):  # noqa: E501
    """Get attribution tags for a given address

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

    :rtype: List[Tag]
    """
    return service.list_address_tags(currency, address)


def list_address_tags_csv(currency, address):  # noqa: E501
    """Get attribution tags for a given address

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

    :rtype: str
    """
    return service.list_address_tags_csv(currency, address)


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
    return service.list_address_txs(currency, address, page, pagesize)
