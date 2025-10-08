from graphsenselib.errors import *

from typing import List, Dict
from aiohttp import web
import traceback
import json
import re

from gsrest.dependencies import get_username

from openapi_server.models.search_result import SearchResult
from openapi_server.models.stats import Stats
import gsrest.service.general_service as service
from openapi_server import util



async def get_statistics(request: web.Request, ) -> web.Response:
    """Get statistics of supported currencies

    


    """

    for plugin in request.app['plugins']:
        if hasattr(plugin, 'before_request'):
            context =\
                request.app['plugin_contexts'][plugin.__module__]
            request = plugin.before_request(context, request)

    show_private_tags_conf = \
        request.app['config'].show_private_tags or False
    show_private_tags = bool(show_private_tags_conf)
    if show_private_tags:
        for (k,v) in show_private_tags_conf['on_header'].items():
            hval = request.headers.get(k, None)
            if not hval:
                show_private_tags = False
                break
            show_private_tags = show_private_tags and \
                bool(re.match(re.compile(v), hval))

    request.app['request_config']['show_private_tags'] = show_private_tags

    try:
        if 'currency' in ['']:
            if currency is not None:
                currency = currency.lower()
        result = service.get_statistics(request
                )
        result = await result

        for plugin in request.app['plugins']:
            if hasattr(plugin, 'before_response'):
                context =\
                    request.app['plugin_contexts'][plugin.__module__]
                plugin.before_response(context, request, result)

        if result is None:
            result = {}
        elif isinstance(result, list):
            result = [d.to_dict() for d in result]
        else:
            result = result.to_dict()

        result = web.Response(
                    status=200,
                    text=json.dumps(result),
                    headers={'Content-type': 'application/json'})
        return result
    except NotFoundException as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPNotFound(text=e.get_user_msg())
    except BadUserInputException as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPBadRequest(text=e.get_user_msg())
    except FeatureNotAvailableException as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPBadRequest(text=e.get_user_msg())
    except GsTimeoutException as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPRequestTimeout()
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)

        user = get_username(request) or "unknown"

        tb.append(f"Request URL: {request.url} from user: {user}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()


async def search(request: web.Request, q, currency=None, limit=None, include_sub_tx_identifiers=None) -> web.Response:
    """Returns matching addresses, transactions and labels

    

    :param q: It can be (the beginning of) an address, a transaction or a label
    :type q: str
    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param limit: Maximum number of search results
    :type limit: int
    :param include_sub_tx_identifiers: Whether to include sub-transaction identifiers
    :type include_sub_tx_identifiers: bool

    """

    for plugin in request.app['plugins']:
        if hasattr(plugin, 'before_request'):
            context =\
                request.app['plugin_contexts'][plugin.__module__]
            request = plugin.before_request(context, request)

    show_private_tags_conf = \
        request.app['config'].show_private_tags or False
    show_private_tags = bool(show_private_tags_conf)
    if show_private_tags:
        for (k,v) in show_private_tags_conf['on_header'].items():
            hval = request.headers.get(k, None)
            if not hval:
                show_private_tags = False
                break
            show_private_tags = show_private_tags and \
                bool(re.match(re.compile(v), hval))

    request.app['request_config']['show_private_tags'] = show_private_tags

    try:
        if 'currency' in ['','q','currency','limit','include_sub_tx_identifiers']:
            if currency is not None:
                currency = currency.lower()
        result = service.search(request
                ,q=q,currency=currency,limit=limit,include_sub_tx_identifiers=include_sub_tx_identifiers)
        result = await result

        for plugin in request.app['plugins']:
            if hasattr(plugin, 'before_response'):
                context =\
                    request.app['plugin_contexts'][plugin.__module__]
                plugin.before_response(context, request, result)

        if result is None:
            result = {}
        elif isinstance(result, list):
            result = [d.to_dict() for d in result]
        else:
            result = result.to_dict()

        result = web.Response(
                    status=200,
                    text=json.dumps(result),
                    headers={'Content-type': 'application/json'})
        return result
    except NotFoundException as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPNotFound(text=e.get_user_msg())
    except BadUserInputException as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPBadRequest(text=e.get_user_msg())
    except FeatureNotAvailableException as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPBadRequest(text=e.get_user_msg())
    except GsTimeoutException as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPRequestTimeout()
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)

        user = get_username(request) or "unknown"

        tb.append(f"Request URL: {request.url} from user: {user}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()
