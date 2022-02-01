from typing import List, Dict
from aiohttp import web
import traceback
import json
import re

from openapi_server.models.search_result import SearchResult
from openapi_server.models.stats import Stats
import gsrest.service.general_service as service
from openapi_server import util



async def get_statistics(request: web.Request, ) -> web.Response:
    """Get statistics of supported currencies

    


    """

    for plugin in request.app['plugins']:
        if hasattr(plugin, 'before_request'):
            request = plugin.before_request(request)

    show_private_tags_conf = \
        request.app['config'].get('show_private_tags', False)
    show_private_tags = bool(show_private_tags_conf)
    if show_private_tags:
        for (k,v) in show_private_tags_conf['on_header'].items():
            hval = request.headers.get(k, None)
            if not hval:
                show_private_tags = False
                break
            show_private_tags = show_private_tags and \
                bool(re.match(re.compile(v), hval))
            
    request.app['show_private_tags'] = show_private_tags

    try:
        if 'currency' in ['']:
            if currency is not None:
                currency = currency.lower() 
        result = service.get_statistics(request
                )
        result = await result

        for plugin in request.app['plugins']:
            if hasattr(plugin, 'before_response'):
                plugin.before_response(request, result)

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


async def search(request: web.Request, q, currency=None, limit=None) -> web.Response:
    """Returns matching addresses, transactions and labels

    

    :param q: It can be (the beginning of) an address, a transaction or a label
    :type q: str
    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param limit: Maximum number of search results
    :type limit: int

    """

    for plugin in request.app['plugins']:
        if hasattr(plugin, 'before_request'):
            request = plugin.before_request(request)

    show_private_tags_conf = \
        request.app['config'].get('show_private_tags', False)
    show_private_tags = bool(show_private_tags_conf)
    if show_private_tags:
        for (k,v) in show_private_tags_conf['on_header'].items():
            hval = request.headers.get(k, None)
            if not hval:
                show_private_tags = False
                break
            show_private_tags = show_private_tags and \
                bool(re.match(re.compile(v), hval))
            
    request.app['show_private_tags'] = show_private_tags

    try:
        if 'currency' in ['','q','currency','limit']:
            if currency is not None:
                currency = currency.lower() 
        result = service.search(request
                ,q=q,currency=currency,limit=limit)
        result = await result

        for plugin in request.app['plugins']:
            if hasattr(plugin, 'before_response'):
                plugin.before_response(request, result)

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
