import connexion
import six

from openapi_server.models.stats import Stats  # noqa: E501
from openapi_server import util
import gsrest.service.general_service as service


def get_statistics():  # noqa: E501
    """Get statistics of supported currencies

     # noqa: E501


    :rtype: Stats
    """
    return service.get_statistics()
