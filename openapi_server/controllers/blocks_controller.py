from typing import List, Dict
from aiohttp import web
import traceback
import json

from openapi_server.models.block import Block
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
    try:
        if 'currency' in ['','currency','height']:
            if currency is not None:
                currency = currency.lower() 
        result = service.get_block(request
                ,currency=currency,height=height)
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


async def list_block_txs(request: web.Request, currency, height) -> web.Response:
    """Get block transactions

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param height: The block height
    :type height: int

    """
    try:
        if 'currency' in ['','currency','height']:
            if currency is not None:
                currency = currency.lower() 
        result = service.list_block_txs(request
                ,currency=currency,height=height)
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
