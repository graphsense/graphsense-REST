import connexion
import six
import traceback
import asyncio

from openapi_server.models.io import Io  # noqa: E501
from openapi_server.models.tx import Tx  # noqa: E501
from openapi_server.models.tx_value import TxValue  # noqa: E501
from openapi_server.models.txs import Txs  # noqa: E501
import gsrest.service.txs_service as service
from gsrest.service.problems import notfound, badrequest, internalerror


def get_tx(currency, tx_hash):  # noqa: E501
    """Returns details of a specific transaction identified by its hash.

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str

    :rtype: Tx
    """
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.get_tx(
                currency=currency,
                tx_hash=tx_hash))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")


def get_tx_io(currency, tx_hash, io):  # noqa: E501
    """Returns input/output values of a specific transaction identified by its hash.

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str
    :param io: Input or outpus values of a transaction
    :type io: dict | bytes

    :rtype: List[TxValue]
    """
    if connexion.request.is_json:
        io =  Io.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.get_tx_io(
                currency=currency,
                tx_hash=tx_hash,
                io=io))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")


def list_txs(currency, page=None):  # noqa: E501
    """Returns transactions

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param page: Resumption token for retrieving the next page
    :type page: str

    :rtype: Txs
    """
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            service.list_txs(
                currency=currency,
                page=page))
        loop.close()
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")
