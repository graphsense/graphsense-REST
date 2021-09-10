import connexion
import six
import traceback

from openapi_server.models.rates import Rates  # noqa: E501
import gsrest.service.rates_service as service
from gsrest.service.problems import notfound, badrequest, internalerror


def get_exchange_rates(currency, height):  # noqa: E501
    """Returns exchange rate for a given height

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param height: The block height
    :type height: int

    :rtype: Rates
    """
    try:
        return service.get_exchange_rates(
            currency=currency,
            height=height)
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")
