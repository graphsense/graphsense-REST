import connexion
import six

from openapi_server.models.currency import Currency  # noqa: E501
from openapi_server import util
import gsrest.service.general_service as service


def get_statistics(currency):  # noqa: E501
    """Get statistics of currency

     # noqa: E501

    :param currency: The currency
    :type currency: str

    :rtype: Currency
    """
    return service.get_statistics(currency)
