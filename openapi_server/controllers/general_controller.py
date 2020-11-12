from openapi_server.models.search_result import SearchResult  # noqa: E501
from openapi_server.models.stats import Stats  # noqa: E501
import gsrest.service.general_service as service
from gsrest.service.problems import notfound


def get_statistics():  # noqa: E501
    """Get statistics of supported currencies

     # noqa: E501


    :rtype: Stats
    """
    try:
        return service.get_statistics(
            )
    except RuntimeError as e:
        return notfound(str(e))


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
        return service.search(
            q=q,
            currency=currency,
            limit=limit)
    except RuntimeError as e:
        return notfound(str(e))
