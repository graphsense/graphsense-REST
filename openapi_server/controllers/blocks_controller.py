from gsrest.errors import *

from typing import List, Dict
from aiohttp import web
import traceback
import json
import re

from openapi_server.models.block import Block
from openapi_server.models.block_at_date import BlockAtDate
from openapi_server.models.tx import Tx
import gsrest.service.blocks_service as service
from openapi_server import util



async def get_block(request: web.Request, currency, height) -> web.Response:
    """Get a block by its height

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param height: The block height
    :type height: int

    """

    for plugin in request.app['plugins']:
        if hasattr(plugin, 'before_request'):
            context =\
                request.app['plugin_contexts'][plugin.__module__]
            request = plugin.before_request(context, request)

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

    request.app['request_config']['show_private_tags'] = show_private_tags

    try:
        if 'currency' in ['','currency','height']:
            if currency is not None:
                currency = currency.lower()
        result = service.get_block(request
                ,currency=currency,height=height)
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
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()


async def get_block_by_date(request: web.Request, currency, date) -> web.Response:
    """Get the closest blocks given a timestamp

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param date: The time of the block
    :type date: str

    """
    date = util.deserialize_datetime(date) if date is not None else None

    for plugin in request.app['plugins']:
        if hasattr(plugin, 'before_request'):
            context =\
                request.app['plugin_contexts'][plugin.__module__]
            request = plugin.before_request(context, request)

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

    request.app['request_config']['show_private_tags'] = show_private_tags

    try:
        if 'currency' in ['','currency','date']:
            if currency is not None:
                currency = currency.lower()
        result = service.get_block_by_date(request
                ,currency=currency,date=date)
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
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()


async def list_block_txs(request: web.Request, currency, height) -> web.Response:
    """Get block transactions

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param height: The block height
    :type height: int

    """

    for plugin in request.app['plugins']:
        if hasattr(plugin, 'before_request'):
            context =\
                request.app['plugin_contexts'][plugin.__module__]
            request = plugin.before_request(context, request)

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

    request.app['request_config']['show_private_tags'] = show_private_tags

    try:
        if 'currency' in ['','currency','height']:
            if currency is not None:
                currency = currency.lower()
        result = service.list_block_txs(request
                ,currency=currency,height=height)
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
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()
