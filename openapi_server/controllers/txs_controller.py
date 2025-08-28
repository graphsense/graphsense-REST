from graphsenselib.errors import *

from typing import List, Dict
from aiohttp import web
import traceback
import json
import re

from gsrest.dependencies import get_username

from openapi_server.models.external_conversion import ExternalConversion
from openapi_server.models.tx import Tx
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.tx_ref import TxRef
from openapi_server.models.tx_value import TxValue
from openapi_server.models.txs import Txs
import gsrest.service.txs_service as service
from openapi_server import util



async def get_spending_txs(request: web.Request, currency, tx_hash, io_index=None) -> web.Response:
    """Returns in which other transaction&#39;s outputs the asked transaction spent. Think backwards references is the transaction graph. This endpoint is only available for utxo like currencies.

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str
    :param io_index: index of the input or output in question
    :type io_index: int

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
        if 'currency' in ['','currency','tx_hash','io_index']:
            if currency is not None:
                currency = currency.lower()
        result = service.get_spending_txs(request
                ,currency=currency,tx_hash=tx_hash,io_index=io_index)
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


async def get_spent_in_txs(request: web.Request, currency, tx_hash, io_index=None) -> web.Response:
    """Returns in which other transactions, outputs from the asked transaction are spent. Think forward references in the transaction graph. This endpoint is only available for utxo like currencies.

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str
    :param io_index: index of the input or output in question
    :type io_index: int

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
        if 'currency' in ['','currency','tx_hash','io_index']:
            if currency is not None:
                currency = currency.lower()
        result = service.get_spent_in_txs(request
                ,currency=currency,tx_hash=tx_hash,io_index=io_index)
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


async def get_tx(request: web.Request, currency, tx_hash, include_io=None, include_nonstandard_io=None, include_io_index=None, token_tx_id=None) -> web.Response:
    """Returns details of a specific transaction identified by its hash

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str
    :param include_io: Whether to include inputs/outputs of a transaction (UTXO only)
    :type include_io: bool
    :param include_nonstandard_io: Whether to include non-standard inputs/outputs such as OP_RETURN of a transaction (UTXO only)
    :type include_nonstandard_io: bool
    :param include_io_index: Whether to include the index of inputs/outputs of a transaction (UTXO only)
    :type include_io_index: bool
    :param token_tx_id: Select a specific token_transaction (Account model only)
    :type token_tx_id: int

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
        if 'currency' in ['','currency','tx_hash','include_io','include_nonstandard_io','include_io_index','token_tx_id']:
            if currency is not None:
                currency = currency.lower()
        result = service.get_tx(request
                ,currency=currency,tx_hash=tx_hash,include_io=include_io,include_nonstandard_io=include_nonstandard_io,include_io_index=include_io_index,token_tx_id=token_tx_id)
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


async def get_tx_conversions(request: web.Request, currency, tx_hash) -> web.Response:
    """Returns conversion information (swaps or bridging txs) extracted from a specific transaction

    

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
        if 'currency' in ['','currency','tx_hash']:
            if currency is not None:
                currency = currency.lower()
        result = service.get_tx_conversions(request
                ,currency=currency,tx_hash=tx_hash)
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


async def get_tx_io(request: web.Request, currency, tx_hash, io, include_nonstandard_io=None, include_io_index=None) -> web.Response:
    """Returns input/output values of a specific transaction identified by its hash

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str
    :param io: Input or outpus values of a transaction
    :type io: str
    :param include_nonstandard_io: Whether to include non-standard inputs/outputs such as OP_RETURN of a transaction (UTXO only)
    :type include_nonstandard_io: bool
    :param include_io_index: Whether to include the index of inputs/outputs of a transaction (UTXO only)
    :type include_io_index: bool

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
        if 'currency' in ['','currency','tx_hash','io','include_nonstandard_io','include_io_index']:
            if currency is not None:
                currency = currency.lower()
        result = service.get_tx_io(request
                ,currency=currency,tx_hash=tx_hash,io=io,include_nonstandard_io=include_nonstandard_io,include_io_index=include_io_index)
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


async def list_tx_flows(request: web.Request, currency, tx_hash, strip_zero_value_txs=None, only_token_txs=None, token_currency=None, page=None, pagesize=None) -> web.Response:
    """Returns all asset flows / Internal txs and token flows within a given transaction

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str
    :param strip_zero_value_txs: Whether to strip zero-value transactions from the response
    :type strip_zero_value_txs: bool
    :param only_token_txs: Whether to include only token transactions
    :type only_token_txs: bool
    :param token_currency: Return transactions of given token or base currency
    :type token_currency: str
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

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
        if 'currency' in ['','currency','tx_hash','strip_zero_value_txs','only_token_txs','token_currency','page','pagesize']:
            if currency is not None:
                currency = currency.lower()
        result = service.list_tx_flows(request
                ,currency=currency,tx_hash=tx_hash,strip_zero_value_txs=strip_zero_value_txs,only_token_txs=only_token_txs,token_currency=token_currency,page=page,pagesize=pagesize)
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
