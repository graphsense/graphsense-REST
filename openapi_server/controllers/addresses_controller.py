from typing import List, Dict
from aiohttp import web
import traceback
import json
import re

from openapi_server.models.address import Address
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.entity import Entity
from openapi_server.models.links import Links
from openapi_server.models.neighbor_addresses import NeighborAddresses
import gsrest.service.addresses_service as service
from openapi_server import util



async def get_address(request: web.Request, currency, address) -> web.Response:
    """Get an address, optionally with tags

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

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
        if 'currency' in ['','currency','address']:
            if currency is not None:
                currency = currency.lower() 
        result = service.get_address(request
                ,currency=currency,address=address)
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
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()


async def get_address_entity(request: web.Request, currency, address) -> web.Response:
    """Get the entity of an address

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str

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
        if 'currency' in ['','currency','address']:
            if currency is not None:
                currency = currency.lower() 
        result = service.get_address_entity(request
                ,currency=currency,address=address)
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
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()


async def list_address_links(request: web.Request, currency, address, neighbor, page=None, pagesize=None) -> web.Response:
    """Get outgoing transactions between two addresses

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param neighbor: Neighbor address
    :type neighbor: str
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

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
        if 'currency' in ['','currency','address','neighbor','page','pagesize']:
            if currency is not None:
                currency = currency.lower() 
        result = service.list_address_links(request
                ,currency=currency,address=address,neighbor=neighbor,page=page,pagesize=pagesize)
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
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()


async def list_address_neighbors(request: web.Request, currency, address, direction, include_labels=None, page=None, pagesize=None) -> web.Response:
    """Get an address&#39;s neighbors in the address graph

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param direction: Incoming or outgoing neighbors
    :type direction: str
    :param include_labels: Whether to include labels of first page of tags
    :type include_labels: bool
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

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
        if 'currency' in ['','currency','address','direction','include_labels','page','pagesize']:
            if currency is not None:
                currency = currency.lower() 
        result = service.list_address_neighbors(request
                ,currency=currency,address=address,direction=direction,include_labels=include_labels,page=page,pagesize=pagesize)
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
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()


async def list_address_txs(request: web.Request, currency, address, page=None, pagesize=None) -> web.Response:
    """Get all transactions an address has been involved in

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

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
        if 'currency' in ['','currency','address','page','pagesize']:
            if currency is not None:
                currency = currency.lower() 
        result = service.list_address_txs(request
                ,currency=currency,address=address,page=page,pagesize=pagesize)
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
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()


async def list_tags_by_address(request: web.Request, currency, address, page=None, pagesize=None) -> web.Response:
    """Get attribution tags for a given address

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param address: The cryptocurrency address
    :type address: str
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

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
        if 'currency' in ['','currency','address','page','pagesize']:
            if currency is not None:
                currency = currency.lower() 
        result = service.list_tags_by_address(request
                ,currency=currency,address=address,page=page,pagesize=pagesize)
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
    except Exception as e:
        tb = traceback.format_exception(type(e), e, e.__traceback__)
        tb.append(f"Request URL: {request.url}")
        tb = "\n".join(tb)
        request.app.logger.error(tb)
        raise web.HTTPInternalServerError()
