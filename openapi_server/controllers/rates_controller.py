from typing import List, Dict
from aiohttp import web
import traceback
import json

from openapi_server.models.rates import Rates
import gsrest.service.rates_service as service
from openapi_server import util


async def get_exchange_rates(request: web.Request, currency, height) -> web.Response:
    """Returns exchange rate for a given height

    

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param height: The block height
    :type height: int

    """
    try:
        result = service.get_exchange_rates(request
                ,currency=currency,height=height)
        result = await result
        if isinstance(result, list):
            result = [d.to_dict() for d in result]
        else:
            result = result.to_dict()
        result = web.Response(
                    status=200,
                    text=json.dumps(result),
                    headers={'Content-type': 'application/json'})
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
