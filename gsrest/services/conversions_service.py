import logging
from typing import Any, Dict, List, Optional, Protocol

from graphsenselib.defi import Bridge, ExternalSwap
from graphsenselib.defi.conversions import get_conversions_from_db
from graphsenselib.errors import BadUserInputException, TransactionNotFoundException
from graphsenselib.utils.accountmodel import hex_to_bytes
from graphsenselib.utils.transactions import (
    SubTransactionIdentifier,
    SubTransactionType,
)

from gsrest.services.common import is_eth_like
from gsrest.services.models import ExternalConversions

logger = logging.getLogger(__name__)


class DatabaseProtocol(Protocol):
    async def get_tx_by_hash(
        self, currency: str, tx_hash_bytes: bytes
    ) -> Optional[Dict[str, Any]]: ...


class ConversionsService:
    def __init__(self, logger: Any):
        self.logger = logger

    def _conversion_from_external_swap(
        self, network: str, swap: ExternalSwap
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

    def _conversion_from_bridge(self, bridge: Bridge) -> ExternalConversions:
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
        self, db: DatabaseProtocol, currency: str, identifier: str
    ) -> List[ExternalConversions]:
        """Extract swap information from a single transaction hash."""
        if not is_eth_like(currency):
            raise BadUserInputException(
                f"Swap extraction is only supported for EVM-like networks, not {currency}"
            )

        tx_obj = SubTransactionIdentifier.from_string(identifier)
        tx_hash = tx_obj.tx_hash

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

        conversions_gslib = await get_conversions_from_db(
            currency, db, tx, include_bridging_actions=False
        )

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
                conversions.append(
                    self._conversion_from_external_swap(currency, conversion)
                )
            elif isinstance(conversion, Bridge):
                conversions.append(self._conversion_from_bridge(conversion))
            else:
                raise ValueError(f"Unknown conversion type: {type(conversion)}")

        return conversions
