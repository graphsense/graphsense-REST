from typing import Any, Dict, List, Optional, Union

from graphsenselib.errors import (
    BadUserInputException,
    NotFoundException,
    TransactionNotFoundException,
)
from graphsenselib.utils.transactions import (
    SubTransactionIdentifier,
    SubTransactionType,
)

from gsrest.services.common import is_eth_like, std_tx_from_row
from gsrest.services.models import TxAccount, TxRef, TxUtxo, TxValue
from gsrest.services.rates_service import RatesService


class TxsService:
    def __init__(
        self,
        db: Any,
        rates_service: RatesService,
        logger: Any,
    ):
        self.db = db
        self.rates_service = rates_service
        self.logger = logger

    async def get_tx(
        self,
        currency: str,
        tx_hash: str,
        token_tx_id: Optional[int] = None,
        include_io: bool = False,
        include_nonstandard_io: bool = False,
        include_io_index: bool = False,
    ) -> Union[TxAccount, TxUtxo]:
        trace_index = None
        tx_ident = tx_hash

        try:
            subtxIdent = SubTransactionIdentifier.from_string(tx_hash)
        except ValueError as e:
            raise BadUserInputException(str(e))

        if subtxIdent.tx_type == SubTransactionType.InternalTx:
            tx_hash = subtxIdent.tx_hash
            trace_index = subtxIdent.sub_index
        elif subtxIdent.tx_type == SubTransactionType.ERC20:
            tx_hash = subtxIdent.tx_hash
            if token_tx_id is None:
                token_tx_id = subtxIdent.sub_index

        if token_tx_id is not None:
            if is_eth_like(currency):
                results = await self.list_token_txs(currency, tx_hash, token_tx_id)
                if len(results):
                    return results[0]
                else:
                    raise TransactionNotFoundException(currency, tx_ident, token_tx_id)
            else:
                raise BadUserInputException(
                    f"{currency} does not support token transactions."
                )
        elif trace_index is not None:
            if is_eth_like(currency):
                tx = await self.db.get_tx(currency, tx_hash)
                res = await self._get_trace_txs(currency, tx, trace_index)
                if res:
                    return res
                else:
                    raise TransactionNotFoundException(currency, tx_ident, token_tx_id)
            else:
                raise BadUserInputException(
                    f"{currency} does not support trace transactions."
                )
        else:
            result = await self.db.get_tx(currency, tx_hash)
            rates = await self.rates_service.get_rates(currency, result["block_id"])

            if result:
                result["type"] = "external"

            return await std_tx_from_row(
                currency,
                result,
                rates.rates,
                self.db.get_token_configuration(currency),
                include_io,
                include_nonstandard_io,
                include_io_index,
            )

    async def get_tx_io(
        self,
        currency: str,
        tx_hash: str,
        io: str,
        include_nonstandard_io: bool = False,
        include_io_index: bool = False,
    ) -> Optional[List[TxValue]]:
        if is_eth_like(currency):
            raise NotFoundException("get_tx_io not implemented for ETH")

        result = await self.get_tx(
            currency,
            tx_hash,
            include_io=True,
            include_nonstandard_io=include_nonstandard_io,
            include_io_index=include_io_index,
        )
        return getattr(result, io)

    async def list_token_txs(
        self, currency: str, tx_hash: str, token_tx_id: Optional[int] = None
    ) -> List[TxAccount]:
        results = await self.db.list_token_txs(currency, tx_hash, log_index=token_tx_id)

        txs = []
        for result in results:
            rates = await self.rates_service.get_rates(currency, result["block_id"])
            tx = await std_tx_from_row(
                currency,
                result,
                rates.rates,
                self.db.get_token_configuration(currency),
            )
            txs.append(tx)

        return txs

    async def get_spent_in_txs(
        self, currency: str, tx_hash: str, io_index: Optional[int]
    ) -> List[TxRef]:
        results = await self.db.get_spent_in_txs(currency, tx_hash, io_index=io_index)

        return [
            TxRef(
                input_index=t["spending_input_index"],
                output_index=t["spent_output_index"],
                tx_hash=t["spending_tx_hash"].hex(),
            )
            for t in results.current_rows
        ]

    async def get_spending_txs(
        self, currency: str, tx_hash: str, io_index: Optional[int]
    ) -> List[TxRef]:
        results = await self.db.get_spending_txs(currency, tx_hash, io_index=io_index)

        return [
            TxRef(
                input_index=t["spending_input_index"],
                output_index=t["spent_output_index"],
                tx_hash=t["spent_tx_hash"].hex(),
            )
            for t in results.current_rows
        ]

    async def list_matching_txs(self, currency: str, expression: str) -> List[str]:
        results = await self.db.list_matching_txs(currency, expression)

        leading_zeros = 0
        pos = 0
        while pos < len(expression) and expression[pos] == "0":
            pos += 1
            leading_zeros += 1

        txs = [
            "0" * leading_zeros
            + str(hex(int.from_bytes(row["tx_hash"], byteorder="big")))[2:]
            for row in results
        ]
        return [tx for tx in txs if tx.startswith(expression)]

    async def get_tx_conversions(self, currency: str, tx_hash: str):
        """Extract swap information from a single transaction hash."""
        # This will be injected as a dependency
        pydantic_results = await self.conversions_service.get_conversions(
            self.db, currency, tx_hash
        )

        from gsrest.translators import pydantic_external_conversions_to_openapi

        return [
            pydantic_external_conversions_to_openapi(conversion)
            for conversion in pydantic_results
        ]

    async def _get_trace_txs(
        self, currency: str, tx: Dict[str, Any], trace_index: Optional[int]
    ) -> Optional[Union[TxAccount, TxUtxo]]:
        result = await self.db.fetch_transaction_trace(currency, tx, trace_index)

        if result and result["tx_hash"] == tx["tx_hash"]:
            result["type"] = "internal"
            result["timestamp"] = tx["block_timestamp"]
            result["is_tx_trace"] = False

            if currency == "trx":
                result["from_address"] = result["caller_address"]
                result["to_address"] = result["transferto_address"]
                result["value"] = result["call_value"]
            else:
                result["contract_creation"] = result["trace_type"] == "create"

            rates = await self.rates_service.get_rates(currency, result["block_id"])
            return await std_tx_from_row(
                currency,
                result,
                rates.rates,
                self.db.get_token_configuration(currency),
            )
        else:
            return None
