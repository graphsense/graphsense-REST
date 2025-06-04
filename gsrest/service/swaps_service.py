from typing import List
import logging

from gsrest.errors import (
    BadUserInputException,
    TransactionNotFoundException,
)
from gsrest.util import is_eth_like
from graphsenselib.datatypes.abi import decode_logs_dict
from graphsenselib.utils.defi import get_swap_from_decoded_logs, ExternalSwap

logger = logging.getLogger(__name__)


async def get_tx_swaps(request, currency: str, tx_hash: str) -> List[ExternalSwap]:
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
        tx_hash_bytes = bytes.fromhex(tx_hash.replace("0x", ""))
        tx = await db.get_tx_by_hash(currency, tx_hash_bytes)
    except ValueError:
        raise BadUserInputException(
            f"{tx_hash} does not look like a valid transaction hash"
        )

    if not tx:
        raise TransactionNotFoundException(currency, tx_hash)

    block_id = tx["block_id"]

    # todo wasteful but for now okay
    logs_result = await db.get_logs_in_block_eth(currency, block_id)
    traces_result = await db.get_traces_in_block(currency, block_id)

    # Filter logs and traces for our specific transaction
    tx_logs = [
        log for log in logs_result.current_rows if log["tx_hash"] == tx["tx_hash"]
    ]
    tx_traces = [
        trace
        for trace in traces_result.current_rows
        if trace["tx_hash"] == tx["tx_hash"]
    ]

    if not tx_logs:
        logger.info(f"No logs found for transaction {tx_hash}")
        return []

    try:
        decoded_logs = decode_logs_dict(tx_logs)
        decoded_log_data = [decoded_log for decoded_log, _ in decoded_logs]
        swap = get_swap_from_decoded_logs(decoded_log_data, tx_logs, tx_traces)

        if swap:
            logger.info(f"Found swap in transaction {tx_hash}: {swap}")
            return [swap]
        else:
            logger.info(f"No swaps found in transaction {tx_hash}")
            return []

    except Exception as e:
        logger.warning(f"Failed to process transaction {tx_hash}: {e}")
        raise BadUserInputException(
            f"Failed to extract swap data from transaction: {str(e)}"
        )
