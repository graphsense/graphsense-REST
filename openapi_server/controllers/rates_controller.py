from openapi_server.models.rates import Rates  # noqa: E501
import gsrest.service.rates_service as service
from gsrest.service.problems import notfound


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
