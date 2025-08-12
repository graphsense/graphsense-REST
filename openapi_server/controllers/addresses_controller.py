from graphsenselib.errors import *

from typing import List, Dict
from aiohttp import web
import traceback
import json
import re

from gsrest.dependencies import get_username

from openapi_server.models.address import Address
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.entity import Entity
from openapi_server.models.links import Links
from openapi_server.models.neighbor_addresses import NeighborAddresses
from openapi_server.models.related_addresses import RelatedAddresses
from openapi_server.models.tag_summary import TagSummary
import gsrest.service.addresses_service as service
from openapi_server import util



async def get_address(request: web.Request, currency, address, include_actors=None) -> web.Response:
    """Get an address

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param include_actors: Whether to include information about the actor behind the address
    :type include_actors: bool

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
        if 'currency' in ['','currency','address','include_actors']:
            if currency is not None:
                currency = currency.lower()
        result = service.get_address(request
                ,currency=currency,address=address,include_actors=include_actors)
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


async def get_address_entity(request: web.Request, currency, address, include_actors=None) -> web.Response:
    """Get the entity of an address

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param include_actors: Whether to include information about the actor behind the address
    :type include_actors: bool

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
        if 'currency' in ['','currency','address','include_actors']:
            if currency is not None:
                currency = currency.lower()
        result = service.get_address_entity(request
                ,currency=currency,address=address,include_actors=include_actors)
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


async def get_tag_summary_by_address(request: web.Request, currency, address, include_best_cluster_tag=None) -> web.Response:
    """Get attribution tag summary for a given address

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param include_best_cluster_tag: If the best cluster tag should be inherited to the address level, often helpful for exchanges where not every address is tagged.
    :type include_best_cluster_tag: bool

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
        if 'currency' in ['','currency','address','include_best_cluster_tag']:
            if currency is not None:
                currency = currency.lower()
        result = service.get_tag_summary_by_address(request
                ,currency=currency,address=address,include_best_cluster_tag=include_best_cluster_tag)
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


async def list_address_links(request: web.Request, currency, address, neighbor, min_height=None, max_height=None, min_date=None, max_date=None, order=None, token_currency=None, page=None, pagesize=None) -> web.Response:
    """Get outgoing transactions between two addresses

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param neighbor: Neighbor address
    :type neighbor: str
    :param min_height: Return transactions starting from given height
    :type min_height: int
    :param max_height: Return transactions up to (including) given height
    :type max_height: int
    :param min_date: min date of txs
    :type min_date: str
    :param max_date: max date of txs
    :type max_date: str
    :param order: Sorting order
    :type order: str
    :param token_currency: Return transactions of given token or base currency
    :type token_currency: str
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

    """
    min_date = util.deserialize_datetime(min_date) if min_date is not None else None
    max_date = util.deserialize_datetime(max_date) if max_date is not None else None

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
        if 'currency' in ['','currency','address','neighbor','min_height','max_height','min_date','max_date','order','token_currency','page','pagesize']:
            if currency is not None:
                currency = currency.lower()
        result = service.list_address_links(request
                ,currency=currency,address=address,neighbor=neighbor,min_height=min_height,max_height=max_height,min_date=min_date,max_date=max_date,order=order,token_currency=token_currency,page=page,pagesize=pagesize)
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


async def list_address_neighbors(request: web.Request, currency, address, direction, only_ids=None, include_labels=None, include_actors=None, page=None, pagesize=None) -> web.Response:
    """Get an address&#39;s neighbors in the address graph

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param direction: Incoming or outgoing neighbors
    :type direction: str
    :param only_ids: Restrict result to given set of comma separated addresses
    :type only_ids: List[str]
    :param include_labels: Whether to include labels of first page of address tags
    :type include_labels: bool
    :param include_actors: Whether to include information about the actor behind the address
    :type include_actors: bool
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
        if 'currency' in ['','currency','address','direction','only_ids','include_labels','include_actors','page','pagesize']:
            if currency is not None:
                currency = currency.lower()
        result = service.list_address_neighbors(request
                ,currency=currency,address=address,direction=direction,only_ids=only_ids,include_labels=include_labels,include_actors=include_actors,page=page,pagesize=pagesize)
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


async def list_address_txs(request: web.Request, currency, address, direction=None, min_height=None, max_height=None, min_date=None, max_date=None, order=None, token_currency=None, page=None, pagesize=None) -> web.Response:
    """Get all transactions an address has been involved in

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param direction: Incoming or outgoing transactions
    :type direction: str
    :param min_height: Return transactions starting from given height
    :type min_height: int
    :param max_height: Return transactions up to (including) given height
    :type max_height: int
    :param min_date: min date of txs
    :type min_date: str
    :param max_date: max date of txs
    :type max_date: str
    :param order: Sorting order
    :type order: str
    :param token_currency: Return transactions of given token or base currency
    :type token_currency: str
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

    """
    min_date = util.deserialize_datetime(min_date) if min_date is not None else None
    max_date = util.deserialize_datetime(max_date) if max_date is not None else None

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
        if 'currency' in ['','currency','address','direction','min_height','max_height','min_date','max_date','order','token_currency','page','pagesize']:
            if currency is not None:
                currency = currency.lower()
        result = service.list_address_txs(request
                ,currency=currency,address=address,direction=direction,min_height=min_height,max_height=max_height,min_date=min_date,max_date=max_date,order=order,token_currency=token_currency,page=page,pagesize=pagesize)
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


async def list_related_addresses(request: web.Request, currency, address, address_relation_type=None, page=None, pagesize=None) -> web.Response:
    """Get related addresses to the input address

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param address_relation_type: what type of related addresses to return
    :type address_relation_type: str
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
        if 'currency' in ['','currency','address','address_relation_type','page','pagesize']:
            if currency is not None:
                currency = currency.lower()
        result = service.list_related_addresses(request
                ,currency=currency,address=address,address_relation_type=address_relation_type,page=page,pagesize=pagesize)
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


async def list_tags_by_address(request: web.Request, currency, address, page=None, pagesize=None, include_best_cluster_tag=None) -> web.Response:
    """Get attribution tags for a given address

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int
    :param include_best_cluster_tag: If the best cluster tag should be inherited to the address level, often helpful for exchanges where not every address is tagged.
    :type include_best_cluster_tag: bool

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
        if 'currency' in ['','currency','address','page','pagesize','include_best_cluster_tag']:
            if currency is not None:
                currency = currency.lower()
        result = service.list_tags_by_address(request
                ,currency=currency,address=address,page=page,pagesize=pagesize,include_best_cluster_tag=include_best_cluster_tag)
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
