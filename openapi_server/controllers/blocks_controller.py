import connexion
import six

from openapi_server.models.block import Block  # noqa: E501
from openapi_server.models.block_txs import BlockTxs  # noqa: E501
from openapi_server.models.blocks import Blocks  # noqa: E501
from openapi_server import util
import gsrest.service.blocks_service as service
from gsrest.service.problems import notfound


def get_block(currency, height):  # noqa: E501
    """Get a block by its height

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param height: The block height
    :type height: int

    :rtype: Block
    """
    try:
      return service.get_block(currency, height)
    except RuntimeError as e:
      return notfound(str(e))
from gsrest.service.problems import notfound


def list_block_txs(currency, height):  # noqa: E501
    """Get all blocks (100 per page)

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param height: The block height
    :type height: int

    :rtype: BlockTxs
    """
    try:
      return service.list_block_txs(currency, height)
    except RuntimeError as e:
      return notfound(str(e))
from gsrest.service.problems import notfound


def list_block_txs_csv(currency, height):  # noqa: E501
    """Get all blocks as CSV

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param height: The block height
    :type height: int

    :rtype: str
    """
    try:
      return service.list_block_txs_csv(currency, height)
    except RuntimeError as e:
      return notfound(str(e))
from gsrest.service.problems import notfound


def list_blocks(currency, page=None):  # noqa: E501
    """Get all blocks

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param page: Resumption token for retrieving the next page
    :type page: str

    :rtype: Blocks
    """
    try:
      return service.list_blocks(currency, page)
    except RuntimeError as e:
      return notfound(str(e))
