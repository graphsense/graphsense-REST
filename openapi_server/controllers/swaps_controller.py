from gsrest.errors import *

from typing import List, Dict
from aiohttp import web
import traceback
import json
import re

import gsrest.service.swaps_service as service
from openapi_server import util


async def get_tx_swaps(request: web.Request, currency, tx_hash) -> web.Response:
    """Returns swap information extracted from a specific transaction
    
    :param currency: The cryptocurrency code (e.g., eth)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str
    """

    for plugin in request.app['plugins']:
        if hasattr(plugin, 'before_request'):
            context = request.app['plugin_contexts'][plugin.__module__]
            request = plugin.before_request(context, request)

    show_private_tags_conf = request.app['config'].get('show_private_tags', False)
    show_private_tags = bool(show_private_tags_conf)
    if show_private_tags:
        for (k, v) in show_private_tags_conf['on_header'].items():
            hval = request.headers.get(k, None)
            if not hval:
                show_private_tags = False
                break
            show_private_tags = show_private_tags and bool(re.match(re.compile(v), hval))

    request.app['request_config']['show_private_tags'] = show_private_tags

    try:
        if currency is not None:
            currency = currency.lower()
            
        result = await service.get_tx_swaps(
            request, currency=currency, tx_hash=tx_hash
        )

        for plugin in request.app['plugins']:
            if hasattr(plugin, 'before_response'):
                context = request.app['plugin_contexts'][plugin.__module__]
                plugin.before_response(context, request, result)

        # Convert ExternalSwap objects to dictionaries for JSON serialization
        result_dict = []
        for swap in result:
            swap_dict = {
                'swapper': swap.swapper,
                'from_amount': swap.fromAmount,
                'to_amount': swap.toAmount,
                'from_token': swap.fromToken,
                'to_token': swap.toToken,
                'version': swap.version,
                'swap_log': swap.swap_log,
            }
            result_dict.append(swap_dict)

        result = web.Response(
            status=200,
            text=json.dumps(result_dict),
            headers={'Content-type': 'application/json'}
        )
        return result
        
    except NotFoundException as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPNotFound(text=e.get_user_msg())
    except BadUserInputException as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise web.HTTPBadRequest(text=e.get_user_msg())
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()
