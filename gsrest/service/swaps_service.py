import logging
from typing import List

from graphsenselib.defi import Bridge, ExternalSwap
from graphsenselib.defi.conversions import get_conversions_from_db
from graphsenselib.errors import (
    BadUserInputException,
    TransactionNotFoundException,
)
from graphsenselib.utils.accountmodel import hex_to_bytes
from graphsenselib.utils.transactions import (
    SubTransactionIdentifier,
    SubTransactionType,
)

from gsrest.util import is_eth_like
from openapi_server.models.external_conversions import ExternalConversions

logger = logging.getLogger(__name__)


def conversion_from_external_swap(
    network: str, swap: ExternalSwap
) -> ExternalConversions:
    return ExternalConversions(
        conversion_type="dex_swap",
        from_address=swap.fromAddress,
        to_address=swap.toAddress,
        from_asset=swap.fromAsset,
        to_asset=swap.toAsset,
        from_amount=hex(swap.fromAmount),
        to_amount=hex(swap.toAmount),
        from_asset_transfer=swap.fromPayment,
        to_asset_transfer=swap.toPayment,
        from_network=network,
        to_network=network,
    )


def conversion_from_bridge(bridge: Bridge) -> ExternalConversions:
    return ExternalConversions(
        conversion_type="bridge",
        from_address=bridge.fromAddress,
        to_address=bridge.toAddress,
        from_asset=bridge.fromAsset,
        to_asset=bridge.toAsset,
        from_amount=hex(bridge.fromAmount),
        to_amount=hex(bridge.toAmount),
        from_asset_transfer=bridge.fromPayment,
        to_asset_transfer=bridge.toPayment,
        from_network=bridge.fromNetwork,
        to_network=bridge.toNetwork,
    )


async def get_conversions(
    request, currency: str, identifier: str
) -> List[ExternalSwap]:
    """
    Extract swap information from a single transaction hash.

    Args:
        request: The aiohttp request object containing the database connection
        currency: The currency/network identifier (e.g., 'eth')
        tx_hash: The transaction hash to analyze for swaps

    Returns:
        List of ExternalSwap objects found in the transaction

    Raises:
        TransactionNotFoundException: If the transaction is not found
        BadUserInputException: If inputs are invalid
    """
    if not is_eth_like(currency):
        raise BadUserInputException(
            f"Swap extraction is only supported for EVM-like networks, not {currency}"
        )

    tx_obj = SubTransactionIdentifier.from_string(identifier)
    tx_hash = tx_obj.tx_hash

    db = request.app["db"]
    # Get tx to get block_id
    try:
        tx_hash_bytes = hex_to_bytes(tx_hash)
        tx = await db.get_tx_by_hash(currency, tx_hash_bytes)
    except ValueError:
        raise BadUserInputException(
            f"{tx_hash} does not look like a valid transaction hash"
        )

    if not tx:
        raise TransactionNotFoundException(currency, tx_hash)

    # try:

    conversions_gslib = await get_conversions_from_db(currency, db, tx)

    # if it is a raw tx hash without a subtx, dont filter, otherwise
    # filter the conversions to the ones that have either fromPayment or toPayment as identifier
    if tx_obj.tx_type is SubTransactionType.ExternalTx:
        filtered_conversions = conversions_gslib
    else:
        filtered_conversions = [
            c
            for c in conversions_gslib
            if c.fromPayment.lower() == tx_obj.to_string().lower()
            or c.toPayment.lower() == tx_obj.to_string().lower()
        ]

    conversions = []

    for conversion in filtered_conversions:
        if isinstance(conversion, ExternalSwap):
            conversions.append(conversion_from_external_swap(currency, conversion))
        elif isinstance(conversion, Bridge):
            conversions.append(conversion_from_bridge(conversion))
        else:
            raise ValueError(f"Unknown conversion type: {type(conversion)}")

    return conversions

    # except Exception as e:
    #    logger.warning(f"Failed to process transaction {identifier}: {e}")
    #    raise BadUserInputException(
    #        f"Failed to extract conversion data from transaction: {str(e)}"
    #    )
