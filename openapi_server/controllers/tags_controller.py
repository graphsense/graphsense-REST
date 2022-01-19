from typing import List, Dict
from aiohttp import web
import traceback
import json

from openapi_server.models.concept import Concept
from openapi_server.models.tags import Tags
from openapi_server.models.taxonomy import Taxonomy
import gsrest.service.tags_service as service
from openapi_server import util



async def list_concepts(request: web.Request, taxonomy) -> web.Response:
    """Returns the supported concepts of a taxonomy

    

    :param taxonomy: The taxonomy
    :type taxonomy: str

    """
    try:
        if 'currency' in ['','taxonomy']:
            if currency is not None:
                currency = currency.lower() 
        result = service.list_concepts(request
                ,taxonomy=taxonomy)
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


async def list_tags(request: web.Request, currency, label, level, page=None, pagesize=None) -> web.Response:
    """Returns address or entity tags associated with a given label

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param label: The label of an entity
    :type label: str
    :param level: Whether tags on the address or entity level are requested
    :type level: str
    :param page: Resumption token for retrieving the next page
    :type page: str
    :param pagesize: Number of items returned in a single page
    :type pagesize: int

    """
    try:
        if 'currency' in ['','currency','label','level','page','pagesize']:
            if currency is not None:
                currency = currency.lower() 
        result = service.list_tags(request
                ,currency=currency,label=label,level=level,page=page,pagesize=pagesize)
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


async def list_taxonomies(request: web.Request, ) -> web.Response:
    """Returns the supported taxonomies

    


    """
    try:
        if 'currency' in ['']:
            if currency is not None:
                currency = currency.lower() 
        result = service.list_taxonomies(request
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
