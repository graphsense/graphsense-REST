import connexion
import six
import traceback
import asyncio

from openapi_server.models.batch_operation import BatchOperation  # noqa: E501
import gsrest.service.batch_service as service
from gsrest.service.problems import notfound, badrequest, internalerror


def batch(currency, batch_operation=None):  # noqa: E501
    """Get data as CSV in batch

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param batch_operation: 
    :type batch_operation: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        batch_operation = BatchOperation.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.batch(
                currency=currency,
                batch_operation=batch_operation))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")
