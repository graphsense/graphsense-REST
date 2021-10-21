import connexion
import six
import traceback
import asyncio

from openapi_server.models.tx import Tx  # noqa: E501
from openapi_server.models.tx_value import TxValue  # noqa: E501
import gsrest.service.txs_service as service
from gsrest.service.problems import notfound, badrequest, internalerror


def get_tx(currency, tx_hash, include_io=None):  # noqa: E501
    """Returns details of a specific transaction identified by its hash.

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param tx_hash: The transaction hash
    :type tx_hash: str
    :param include_io: Whether to include inputs/outputs of a transaction (UTXO only)
    :type include_io: bool

    :rtype: Tx
    """
    try:
        result = asyncio.run(
            service.get_tx(
                currency=currency,
                tx_hash=tx_hash,
                include_io=include_io))
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except TypeError as e:
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
    :type io: str

    :rtype: List[TxValue]
    """
    try:
        result = asyncio.run(
            service.get_tx_io(
                currency=currency,
                tx_hash=tx_hash,
                io=io))
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except TypeError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")
