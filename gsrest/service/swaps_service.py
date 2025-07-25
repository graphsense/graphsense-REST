import logging
from typing import List

from graphsenselib.datatypes.abi import decode_logs_dict
from graphsenselib.utils.accountmodel import hex_to_bytes
from graphsenselib.defi import ExternalSwap, Bridge
from graphsenselib.defi.conversions import get_conversions_from_decoded_logs

from gsrest.errors import (
    BadUserInputException,
    TransactionNotFoundException,
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


async def get_tx_dex_swap_conversions(
    request, currency: str, tx_hash: str
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

    # todo wasteful but for now okay
    tx_logs_raw = await db.fetch_transaction_logs(currency, tx)
    tx_traces = await db.fetch_transaction_traces(currency, tx)

    if not tx_logs_raw:
        logger.info(f"No logs found for transaction {tx_hash}")
        return []

    try:
        decoded_logs_and_logs = decode_logs_dict(tx_logs_raw)
        decoded_log_data, tx_logs_raw_filtered = zip(*decoded_logs_and_logs)
        conversions_gslib = get_conversions_from_decoded_logs(
            currency, tx, decoded_log_data, tx_logs_raw_filtered, tx_traces
        )

        conversions = []

        for conversion in conversions_gslib:
            if isinstance(conversion, ExternalSwap):
                conversions.append(conversion_from_external_swap(currency, conversion))
            elif isinstance(conversion, Bridge):
                conversions.append(conversion_from_bridge(conversion))
            else:
                raise ValueError(f"Unknown conversion type: {type(conversion)}")

        return conversions

    except Exception as e:
        logger.warning(f"Failed to process transaction {tx_hash}: {e}")
        raise BadUserInputException(
            f"Failed to extract conversion data from transaction: {str(e)}"
        )
