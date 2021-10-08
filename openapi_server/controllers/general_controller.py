import connexion
import six
import traceback
import asyncio

from openapi_server.models.search_result import SearchResult  # noqa: E501
from openapi_server.models.stats import Stats  # noqa: E501
import gsrest.service.general_service as service
from gsrest.service.problems import notfound, badrequest, internalerror


def get_statistics():  # noqa: E501
    """Get statistics of supported currencies

     # noqa: E501


    :rtype: Stats
    """
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.get_statistics(
                ))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")


def search(q, currency=None, limit=None):  # noqa: E501
    """Returns matching addresses, transactions and labels

     # noqa: E501

    :param q: It can be (the beginning of) an address, a transaction or a label
    :type q: str
    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param limit: Maximum number of search results
    :type limit: int

    :rtype: SearchResult
    """
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.search(
                q=q,
                currency=currency,
                limit=limit))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")
