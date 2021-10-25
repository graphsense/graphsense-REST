from typing import List, Dict
from aiohttp import web
import traceback
import json

import gsrest.service.bulk_service as service
from openapi_server import util


async def bulk(request: web.Request, currency, api, operation, body, form=None) -> web.Response:
    """Get data as CSV or JSON in bulk

    

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

    """
    try:
        result = service.bulk(request
                ,currency=currency,api=api,operation=operation,body=body,form=form)
        return result
    except RuntimeError as e:
        return web.Response(status=404, text=str(e))
    except ValueError as e:
        return web.Response(status=400, text=str(e))
    except TypeError as e:
        return web.Response(status=400, text=str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return web.Response(status=500)
