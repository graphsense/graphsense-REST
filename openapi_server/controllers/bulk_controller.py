from typing import List, Dict
from aiohttp import web
import traceback
import json

import gsrest.service.bulk_service as service
from openapi_server import util


async def bulk_csv(request: web.Request, currency, api, operation, body) -> web.Response:
    """Get data as CSV in bulk

    

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param api: The api of the operation to execute in bulk
    :type api: str
    :param operation: The operation to execute in bulk
    :type operation: str
    :param body: Map of the operation&#39;s parameter names to (arrays of) values
    :type body: 

    """
    try:
        result = service.bulk_csv(request
                ,currency=currency,api=api,operation=operation,body=body)
        return result
    except RuntimeError as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPNotFound(text=str(e))
    except ValueError as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPBadRequest(text=str(e))
    except TypeError as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPBadRequest(text=str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPInternalServerError()


async def bulk_json(request: web.Request, currency, api, operation, body) -> web.Response:
    """Get data as JSON in bulk

    

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param api: The api of the operation to execute in bulk
    :type api: str
    :param operation: The operation to execute in bulk
    :type operation: str
    :param body: Map of the operation&#39;s parameter names to (arrays of) values
    :type body: 

    """
    try:
        result = service.bulk_json(request
                ,currency=currency,api=api,operation=operation,body=body)
        return result
    except RuntimeError as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPNotFound(text=str(e))
    except ValueError as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPBadRequest(text=str(e))
    except TypeError as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPBadRequest(text=str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPInternalServerError()
