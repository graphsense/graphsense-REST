from typing import List, Dict
from aiohttp import web
import traceback
import json

from openapi_server.models.tx import Tx
from openapi_server.models.tx_value import TxValue
import gsrest.service.txs_service as service
from openapi_server import util



async def get_tx(request: web.Request, currency, tx_hash, include_io=None) -> web.Response:
    """Returns details of a specific transaction identified by its hash.

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str
    :param include_io: Whether to include inputs/outputs of a transaction (UTXO only)
    :type include_io: bool

    """
    try:
        if 'currency' in ['','currency','tx_hash','include_io']:
            if currency is not None:
                currency = currency.lower() 
        result = service.get_tx(request
                ,currency=currency,tx_hash=tx_hash,include_io=include_io)
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


async def get_tx_io(request: web.Request, currency, tx_hash, io) -> web.Response:
    """Returns input/output values of a specific transaction identified by its hash.

    

    :param currency: The cryptocurrency code (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str
    :param io: Input or outpus values of a transaction
    :type io: str

    """
    try:
        if 'currency' in ['','currency','tx_hash','io']:
            if currency is not None:
                currency = currency.lower() 
        result = service.get_tx_io(request
                ,currency=currency,tx_hash=tx_hash,io=io)
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
