import connexion
import six

from openapi_server.models.address import Address  # noqa: E501
from openapi_server import util
import gsrest.service.addresses_service as service


def get_address_with_tags(currency, address):  # noqa: E501
    """Get an address with tags

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

    :rtype: Address
    """
    return service.get_address_with_tags(currency, address)
