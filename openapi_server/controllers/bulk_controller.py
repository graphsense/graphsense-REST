import connexion
import six
import traceback
import asyncio

import gsrest.service.bulk_service as service
from gsrest.service.problems import notfound, badrequest, internalerror


def bulk(currency, api, operation, body, form=None):  # noqa: E501
    """Get data as CSV or JSON in bulk

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param api: The api of the operation to execute in bulk
    :type api: str
    :param operation: The operation to execute in bulk
    :type operation: str
    :param body: Map of the operation&#39;s parameter names to (arrays of) values
    :type body: 
    :param form: The response data format
    :type form: str

    :rtype: List[Dict[str, object]]
    """
    try:
        result = asyncio.run(
            service.bulk(
                currency=currency,
                api=api,
                operation=operation,
                body=body,
                form=form))
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except TypeError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")
