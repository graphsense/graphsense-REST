from typing import List, Dict
from aiohttp import web
import traceback
import json
import re

from openapi_server.models.tx import Tx
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.tx_value import TxValue
import gsrest.service.txs_service as service
from openapi_server import util



async def get_tx(request: web.Request, currency, tx_hash, include_io=None, token_tx_id=None) -> web.Response:
    """Returns details of a specific transaction identified by its hash.

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str
    :param include_io: Whether to include inputs/outputs of a transaction (UTXO only)
    :type include_io: bool
    :param token_tx_id: Select a specific token_transaction (Account model only)
    :type token_tx_id: int

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
            
    request.app['show_private_tags'] = show_private_tags

    try:
        if 'currency' in ['','currency','tx_hash','include_io','token_tx_id']:
            if currency is not None:
                currency = currency.lower() 
        result = service.get_tx(request
                ,currency=currency,tx_hash=tx_hash,include_io=include_io,token_tx_id=token_tx_id)
        result = await result

        for plugin in request.app['plugins']:
            if hasattr(plugin, 'before_response'):
                context =\
                    request.app['plugin_contexts'][plugin.__module__]
                plugin.before_response(context, request, result)

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
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()


async def get_tx_io(request: web.Request, currency, tx_hash, io) -> web.Response:
    """Returns input/output values of a specific transaction identified by its hash.

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str
    :param io: Input or outpus values of a transaction
    :type io: str

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
            
    request.app['show_private_tags'] = show_private_tags

    try:
        if 'currency' in ['','currency','tx_hash','io']:
            if currency is not None:
                currency = currency.lower() 
        result = service.get_tx_io(request
                ,currency=currency,tx_hash=tx_hash,io=io)
        result = await result

        for plugin in request.app['plugins']:
            if hasattr(plugin, 'before_response'):
                context =\
                    request.app['plugin_contexts'][plugin.__module__]
                plugin.before_response(context, request, result)

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
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()


async def list_token_txs(request: web.Request, currency, tx_hash) -> web.Response:
    """Returns all token transactions in a given transaction

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str

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
            
    request.app['show_private_tags'] = show_private_tags

    try:
        if 'currency' in ['','currency','tx_hash']:
            if currency is not None:
                currency = currency.lower() 
        result = service.list_token_txs(request
                ,currency=currency,tx_hash=tx_hash)
        result = await result

        for plugin in request.app['plugins']:
            if hasattr(plugin, 'before_response'):
                context =\
                    request.app['plugin_contexts'][plugin.__module__]
                plugin.before_response(context, request, result)

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
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()
