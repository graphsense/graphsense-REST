from typing import List, Dict
from aiohttp import web
import traceback
import json

from openapi_server.models.search_result import SearchResult
from openapi_server.models.stats import Stats
import gsrest.service.general_service as service
from openapi_server import util


async def get_statistics(request: web.Request, ) -> web.Response:
    """Get statistics of supported currencies

    


    """
    try:
        result = service.get_statistics(request
                )
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
        return web.Response(status=404, text=str(e))
    except ValueError as e:
        return web.Response(status=400, text=str(e))
    except TypeError as e:
        return web.Response(status=400, text=str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return web.Response(status=500)


async def search(request: web.Request, q, currency=None, limit=None) -> web.Response:
    """Returns matching addresses, transactions and labels

    

    :param q: It can be (the beginning of) an address, a transaction or a label
    :type q: str
    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param limit: Maximum number of search results
    :type limit: int

    """
    try:
        result = service.search(request
                ,q=q,currency=currency,limit=limit)
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
        return web.Response(status=404, text=str(e))
    except ValueError as e:
        return web.Response(status=400, text=str(e))
    except TypeError as e:
        return web.Response(status=400, text=str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return web.Response(status=500)
