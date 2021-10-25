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
        return web.Response(status=404, text=str(e))
    except ValueError as e:
        return web.Response(status=400, text=str(e))
    except TypeError as e:
        return web.Response(status=400, text=str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return web.Response(status=500)


async def list_tags(request: web.Request, label, currency=None) -> web.Response:
    """Returns address and entity tags associated with a given label

    

    :param label: The label of an entity
    :type label: str
    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str

    """
    try:
        result = service.list_tags(request
                ,label=label,currency=currency)
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
        return web.Response(status=404, text=str(e))
    except ValueError as e:
        return web.Response(status=400, text=str(e))
    except TypeError as e:
        return web.Response(status=400, text=str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return web.Response(status=500)


async def list_taxonomies(request: web.Request, ) -> web.Response:
    """Returns the supported taxonomies

    


    """
    try:
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
        return web.Response(status=404, text=str(e))
    except ValueError as e:
        return web.Response(status=400, text=str(e))
    except TypeError as e:
        return web.Response(status=400, text=str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return web.Response(status=500)
