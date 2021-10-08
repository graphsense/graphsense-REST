import connexion
import six
import traceback
import asyncio

from openapi_server.models.address import Address  # noqa: E501
from openapi_server.models.address_tag import AddressTag  # noqa: E501
from openapi_server.models.addresses import Addresses  # noqa: E501
from openapi_server.models.entity import Entity  # noqa: E501
from openapi_server.models.links import Links  # noqa: E501
from openapi_server.models.neighbors import Neighbors  # noqa: E501
from openapi_server.models.txs_account import TxsAccount  # noqa: E501
import gsrest.service.addresses_service as service
from gsrest.service.problems import notfound, badrequest, internalerror


def get_address(currency, address, include_tags=None):  # noqa: E501
    """Get an address, optionally with tags

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param include_tags: Whether to include tags
    :type include_tags: bool

    :rtype: Address
    """
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.get_address(
                currency=currency,
                address=address,
                include_tags=include_tags))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")


def get_address_entity(currency, address, include_tags=None, tag_coherence=None):  # noqa: E501
    """Get the entity of an address

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param include_tags: Whether to include tags
    :type include_tags: bool
    :param tag_coherence: Whether to calculate coherence of address tags
    :type tag_coherence: bool

    :rtype: Entity
    """
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.get_address_entity(
                currency=currency,
                address=address,
                include_tags=include_tags,
                tag_coherence=tag_coherence))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")


def list_address_links(currency, address, neighbor):  # noqa: E501
    """Get transactions between two addresses

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param neighbor: Neighbor address
    :type neighbor: str

    :rtype: Links
    """
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.list_address_links(
                currency=currency,
                address=address,
                neighbor=neighbor))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")


def list_address_neighbors(currency, address, direction, include_labels=None, page=None, pagesize=None):  # noqa: E501
    """Get an addresses&#39; neighbors in the address graph

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param direction: Incoming or outgoing neighbors
    :type direction: str
    :param include_labels: Whether to include labels of tags
    :type include_labels: bool
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

    :rtype: Neighbors
    """
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.list_address_neighbors(
                currency=currency,
                address=address,
                direction=direction,
                include_labels=include_labels,
                page=page,
                pagesize=pagesize))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")


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

    :rtype: TxsAccount
    """
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.list_address_txs(
                currency=currency,
                address=address,
                page=page,
                pagesize=pagesize))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")


def list_addresses(currency, ids=None, page=None, pagesize=None):  # noqa: E501
    """Get addresses

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param ids: Restrict result to given set of comma separated addresses
    :type ids: List[str]
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

    :rtype: Addresses
    """
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.list_addresses(
                currency=currency,
                ids=ids,
                page=page,
                pagesize=pagesize))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")


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
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.list_tags_by_address(
                currency=currency,
                address=address))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")
