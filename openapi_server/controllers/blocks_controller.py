import connexion
import six
import traceback
import asyncio

from openapi_server.models.block import Block  # noqa: E501
from openapi_server.models.tx import Tx  # noqa: E501
import gsrest.service.blocks_service as service
from gsrest.service.problems import notfound, badrequest, internalerror


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
        result = asyncio.run(
            service.get_block(
                currency=currency,
                height=height))
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


def list_block_txs(currency, height):  # noqa: E501
    """Get block transactions

     # noqa: E501

    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str
    :param height: The block height
    :type height: int

    :rtype: List[Tx]
    """
    try:
        result = asyncio.run(
            service.list_block_txs(
                currency=currency,
                height=height))
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
