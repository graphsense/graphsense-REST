from graphsenselib.errors import *

from typing import List, Dict
from aiohttp import web
import traceback
import json
import re

from openapi_server.models.address_tags import AddressTags
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.entity import Entity
from openapi_server.models.entity_addresses import EntityAddresses
from openapi_server.models.links import Links
from openapi_server.models.neighbor_entities import NeighborEntities
from openapi_server.models.search_result_level1 import SearchResultLevel1
import gsrest.service.entities_service as service
from openapi_server import util



async def get_entity(request: web.Request, currency, entity, exclude_best_address_tag=None, include_actors=None) -> web.Response:
    """Get an entity

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param exclude_best_address_tag: Whether to exclude the best address tag
    :type exclude_best_address_tag: bool
    :param include_actors: Whether to include information about the actor behind the address
    :type include_actors: bool

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
        if 'currency' in ['','currency','entity','exclude_best_address_tag','include_actors']:
            if currency is not None:
                currency = currency.lower()
        result = service.get_entity(request
                ,currency=currency,entity=entity,exclude_best_address_tag=exclude_best_address_tag,include_actors=include_actors)
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


async def list_address_tags_by_entity(request: web.Request, currency, entity, page=None, pagesize=None) -> web.Response:
    """Get address tags for a given entity

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
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
        if 'currency' in ['','currency','entity','page','pagesize']:
            if currency is not None:
                currency = currency.lower()
        result = service.list_address_tags_by_entity(request
                ,currency=currency,entity=entity,page=page,pagesize=pagesize)
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


async def list_entity_addresses(request: web.Request, currency, entity, page=None, pagesize=None) -> web.Response:
    """Get an entity&#39;s addresses

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
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
        if 'currency' in ['','currency','entity','page','pagesize']:
            if currency is not None:
                currency = currency.lower()
        result = service.list_entity_addresses(request
                ,currency=currency,entity=entity,page=page,pagesize=pagesize)
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


async def list_entity_links(request: web.Request, currency, entity, neighbor, min_height=None, max_height=None, min_date=None, max_date=None, order=None, token_currency=None, page=None, pagesize=None) -> web.Response:
    """Get transactions between two entities

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param neighbor: Neighbor entity
    :type neighbor: int
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
        if 'currency' in ['','currency','entity','neighbor','min_height','max_height','min_date','max_date','order','token_currency','page','pagesize']:
            if currency is not None:
                currency = currency.lower()
        result = service.list_entity_links(request
                ,currency=currency,entity=entity,neighbor=neighbor,min_height=min_height,max_height=max_height,min_date=min_date,max_date=max_date,order=order,token_currency=token_currency,page=page,pagesize=pagesize)
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


async def list_entity_neighbors(request: web.Request, currency, entity, direction, only_ids=None, include_labels=None, exclude_best_address_tag=None, include_actors=None, page=None, pagesize=None) -> web.Response:
    """Get an entity&#39;s direct neighbors

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param direction: Incoming or outgoing neighbors
    :type direction: str
    :param only_ids: Restrict result to given set of comma separated IDs
    :type only_ids: List[int]
    :param include_labels: Whether to include labels of first page of address tags
    :type include_labels: bool
    :param exclude_best_address_tag: Whether to exclude the best address tag
    :type exclude_best_address_tag: bool
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
        if 'currency' in ['','currency','entity','direction','only_ids','include_labels','exclude_best_address_tag','include_actors','page','pagesize']:
            if currency is not None:
                currency = currency.lower()
        result = service.list_entity_neighbors(request
                ,currency=currency,entity=entity,direction=direction,only_ids=only_ids,include_labels=include_labels,exclude_best_address_tag=exclude_best_address_tag,include_actors=include_actors,page=page,pagesize=pagesize)
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


async def list_entity_txs(request: web.Request, currency, entity, direction=None, min_height=None, max_height=None, min_date=None, max_date=None, order=None, token_currency=None, page=None, pagesize=None) -> web.Response:
    """Get all transactions an entity has been involved in

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
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
        if 'currency' in ['','currency','entity','direction','min_height','max_height','min_date','max_date','order','token_currency','page','pagesize']:
            if currency is not None:
                currency = currency.lower()
        result = service.list_entity_txs(request
                ,currency=currency,entity=entity,direction=direction,min_height=min_height,max_height=max_height,min_date=min_date,max_date=max_date,order=order,token_currency=token_currency,page=page,pagesize=pagesize)
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


async def search_entity_neighbors(request: web.Request, currency, entity, direction, key, value, depth, breadth=None, skip_num_addresses=None) -> web.Response:
    """Search deeply for matching neighbors

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param entity: The entity ID
    :type entity: int
    :param direction: Incoming or outgoing neighbors
    :type direction: str
    :param key: Match neighbors against one and only one of these properties: - the category the entity belongs to - addresses the entity contains - entity ids - total_received: amount the entity received in total - balance: amount the entity holds finally
    :type key: str
    :param value: If key is - category: comma separated list of category names - addresses: comma separated list of address IDs - entities: comma separated list of entity IDs - total_received/balance: comma separated tuple of (currency, min, max) where currency is &#39;value&#39; for the cryptocurrency value or an ISO currency code
    :type value: List[str]
    :param depth: How many hops should the transaction graph be searched
    :type depth: int
    :param breadth: How many siblings of each neighbor should be tried
    :type breadth: int
    :param skip_num_addresses: Skip entities containing more addresses
    :type skip_num_addresses: int

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
        if 'currency' in ['','currency','entity','direction','key','value','depth','breadth','skip_num_addresses']:
            if currency is not None:
                currency = currency.lower()
        result = service.search_entity_neighbors(request
                ,currency=currency,entity=entity,direction=direction,key=key,value=value,depth=depth,breadth=breadth,skip_num_addresses=skip_num_addresses)
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
