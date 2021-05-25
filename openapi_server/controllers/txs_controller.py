import connexion
import six
import traceback

from openapi_server.models.tx import Tx  # noqa: E501
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
        return service.get_tx(
            currency=currency,
            tx_hash=tx_hash)
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror(str(e))


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
        return service.list_txs(
            currency=currency,
            page=page)
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror(str(e))
