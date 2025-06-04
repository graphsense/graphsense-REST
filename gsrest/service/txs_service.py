from typing import Optional

from gsrest.db.cassandra import SUBTX_IDENT_SEPERATOR_CHAR, get_tx_idenifier
from gsrest.errors import (
    BadUserInputException,
    NotFoundException,
    TransactionNotFoundException,
)
from gsrest.service.rates_service import get_rates
from gsrest.util import get_first_key_present, is_eth_like
from gsrest.util.address import address_to_user_format
from gsrest.util.values import convert_token_value, convert_value
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.tx_ref import TxRef
from openapi_server.models.tx_utxo import TxUtxo
from openapi_server.models.tx_value import TxValue


def get_type_account(row):
    if row["type"] == "internal":
        return "account"
    elif row["type"] == "erc20":
        return "account"
    elif row["type"] == "external":
        return "account"
    else:
        raise Exception(f"Unknown transaction type {row}")


def tx_account_from_row(currency, row, rates, token_config):
    height_keys = ["height", "block_id"]
    timestamp_keys = ["timestamp", "block_timestamp"]
    height = get_first_key_present(row, height_keys)

    r = rates[height] if isinstance(rates, dict) else rates

    return TxAccount(
        currency=currency if "token_tx_id" not in row else row["currency"].lower(),
        network=currency,
        tx_type=get_type_account(row),
        identifier=get_tx_idenifier(row),
        tx_hash=row["tx_hash"].hex(),
        timestamp=get_first_key_present(row, timestamp_keys),
        height=height,
        from_address=address_to_user_format(currency, row["from_address"]),
        to_address=address_to_user_format(currency, row["to_address"]),
        token_tx_id=row.get("token_tx_id", None),
        contract_creation=row.get("contract_creation", None),
        value=convert_value(currency, row["value"], r)
        if "token_tx_id" not in row
        else convert_token_value(row["value"], r, token_config[row["currency"]]),
    )


def from_row(
    currency,
    row,
    rates,
    token_config,
    include_io=False,
    include_nonstandard_io=False,
    include_io_index=False,
):
    if is_eth_like(currency):
        return tx_account_from_row(currency, row, rates, token_config)

    return TxUtxo(
        currency=currency,
        tx_hash=row["tx_hash"].hex(),
        coinbase=row["coinbase"],
        height=row["block_id"],
        no_inputs=0 if not row["inputs"] else len(row["inputs"]),
        no_outputs=0 if not row["outputs"] else len(row["outputs"]),
        inputs=io_from_rows(
            currency,
            row,
            "inputs",
            rates,
            include_io,
            include_nonstandard_io,
            include_io_index,
        ),
        outputs=io_from_rows(
            currency,
            row,
            "outputs",
            rates,
            include_io,
            include_nonstandard_io,
            include_io_index,
        ),
        timestamp=row["timestamp"],
        total_input=convert_value(currency, row["total_input"], rates),
        total_output=convert_value(currency, row["total_output"], rates),
    )


async def get_spent_in_txs(
    request, currency: str, tx_hash: str, io_index: Optional[int]
):
    db = request.app["db"]
    results = await db.get_spent_in_txs(currency, tx_hash, io_index=io_index)
    results = [
        TxRef(
            input_index=t["spending_input_index"],
            output_index=t["spent_output_index"],
            tx_hash=t["spending_tx_hash"].hex(),
        )
        for t in results.current_rows
    ]
    return results


async def get_spending_txs(
    request, currency: str, tx_hash: str, io_index: Optional[int]
):
    db = request.app["db"]
    results = await db.get_spending_txs(currency, tx_hash, io_index=io_index)
    results = [
        TxRef(
            input_index=t["spending_input_index"],
            output_index=t["spent_output_index"],
            tx_hash=t["spent_tx_hash"].hex(),
        )
        for t in results.current_rows
    ]
    return results


def io_from_rows(
    currency, values, key, rates, include_io, include_nonstandard_io, include_io_index
):
    if not include_io:
        return None
    if key not in values:
        return None
    if not values[key]:
        return []

    results = []
    for idx, i in enumerate(values[key]):
        if i.address is not None:
            results.append(
                TxValue(
                    address=i.address,
                    value=convert_value(currency, i.value, rates),
                    index=idx if include_io_index else None,
                )
            )
        elif include_nonstandard_io:
            results.append(
                TxValue(
                    address=[],
                    value=convert_value(currency, i.value, rates),
                    index=idx if include_io_index else None,
                )
            )
    return results


async def list_token_txs(request, currency, tx_hash, token_tx_id=None):
    db = request.app["db"]
    results = await db.list_token_txs(currency, tx_hash, log_index=token_tx_id)

    results = [
        from_row(
            currency,
            result,
            (await get_rates(request, currency, result["block_id"]))["rates"],
            db.get_token_configuration(currency),
        )
        for result in results
    ]

    return results


async def get_trace_txs(request, currency, tx, trace_index=None):
    db = request.app["db"]
    result = await db.fetch_transaction_trace(currency, tx, trace_index)

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
            # is_tx_trace = (
            #     result["trace_address"] is None or result["trace_address"].strip() == ""
            # )
            # result["is_tx_trace"] = is_tx_trace
            # if is_tx_trace:
            #     result["type"] = "external"

        return from_row(
            currency,
            result,
            (await get_rates(request, currency, result["block_id"]))["rates"],
            db.get_token_configuration(currency),
        )
    else:
        return None


async def get_tx(
    request,
    currency,
    tx_hash,
    token_tx_id=None,
    include_io=False,
    include_nonstandard_io=False,
    include_io_index=False,
):
    db = request.app["db"]

    trace_index = None

    tx_ident = tx_hash

    if f"{SUBTX_IDENT_SEPERATOR_CHAR}I" in tx_hash:
        h, postfix, *_ = tx_hash.split(SUBTX_IDENT_SEPERATOR_CHAR)
        try:
            tindexS = postfix.strip("IT")
            trace_index = int(tindexS)
        except ValueError:
            raise BadUserInputException(f"Trace index: {tindexS} is not an integer.")
        tx_hash = h
    elif f"{SUBTX_IDENT_SEPERATOR_CHAR}T" in tx_hash:
        h, postfix, *_ = tx_hash.split(SUBTX_IDENT_SEPERATOR_CHAR)

        try:
            tindexS = postfix.strip("IT")
            if token_tx_id is None:
                token_tx_id = int(tindexS)
        except ValueError:
            raise BadUserInputException(f"Token index: {tindexS} is not an integer.")

        tx_hash = h

    if token_tx_id is not None:
        if is_eth_like(currency):
            results = await list_token_txs(
                request, currency, tx_hash, token_tx_id=token_tx_id
            )

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
            tx = await db.get_tx(currency, tx_hash)
            res = await get_trace_txs(request, currency, tx, trace_index)

            if res:
                return res
            else:
                raise TransactionNotFoundException(currency, tx_ident, token_tx_id)

        else:
            raise BadUserInputException(
                f"{currency} does not support trace transactions."
            )
    else:
        result = await db.get_tx(currency, tx_hash)
        rates = (await get_rates(request, currency, result["block_id"]))["rates"]

        if result:
            result["type"] = "external"

        result = from_row(
            currency,
            result,
            rates,
            db.get_token_configuration(currency),
            include_io,
            include_nonstandard_io,
            include_io_index,
        )
        return result


async def get_tx_io(
    request, currency, tx_hash, io, include_nonstandard_io, include_io_index
):
    if is_eth_like(currency):
        raise NotFoundException("get_tx_io not implemented for ETH")
    result = await get_tx(
        request,
        currency,
        tx_hash,
        include_io=True,
        include_nonstandard_io=include_nonstandard_io,
        include_io_index=include_io_index,
    )
    return getattr(result, io)


async def list_matching_txs(request, currency, expression):
    db = request.app["db"]
    results = await db.list_matching_txs(currency, expression)

    leading_zeros = 0
    pos = 0
    # leading zeros will be lost when casting to int
    while expression[pos] == "0":
        pos += 1
        leading_zeros += 1

    txs = [
        "0" * leading_zeros
        + str(hex(int.from_bytes(row["tx_hash"], byteorder="big")))[2:]
        for row in results
    ]
    return [tx for tx in txs if tx.startswith(expression)]
