import connexion
import six

from openapi_server.models.tx import Tx  # noqa: E501
from openapi_server.models.txs import Txs  # noqa: E501
from openapi_server import util
import gsrest.service.txs_service as service
from gsrest.service.problems import notfound


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
      return service.get_tx(currency, tx_hash)
    except RuntimeError as e:
      return notfound(str(e))


def list_txs(currency):  # noqa: E501
    """Returns details of a specific transaction identified by its hash.

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str

    :rtype: Txs
    """
    try:
      return service.list_txs(currency)
    except RuntimeError as e:
      return notfound(str(e))
