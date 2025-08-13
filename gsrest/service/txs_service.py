from typing import Optional

from gsrest.dependencies import get_service_container
from gsrest.translators import (
    pydantic_external_conversions_to_openapi,
    pydantic_tx_account_to_openapi,
    pydantic_tx_ref_to_openapi,
    pydantic_tx_to_openapi,
    pydantic_tx_value_to_openapi,
)


async def get_tx(
    request,
    currency,
    tx_hash,
    token_tx_id=None,
    include_io=False,
    include_nonstandard_io=False,
    include_io_index=False,
):
    services = get_service_container(request)

    result = await services.txs_service.get_tx(
        currency,
        tx_hash,
        token_tx_id,
        include_io,
        include_nonstandard_io,
        include_io_index,
    )
    return pydantic_tx_to_openapi(result)


async def get_tx_io(
    request, currency, tx_hash, io, include_nonstandard_io, include_io_index
):
    services = get_service_container(request)
    result = await services.txs_service.get_tx_io(
        currency, tx_hash, io, include_nonstandard_io, include_io_index
    )
    return [pydantic_tx_value_to_openapi(tx_value) for tx_value in result or []]


async def list_token_txs(request, currency, tx_hash, token_tx_id=None):
    services = get_service_container(request)
    results = await services.txs_service.list_token_txs(currency, tx_hash, token_tx_id)
    return [pydantic_tx_account_to_openapi(tx) for tx in results]


async def get_spent_in_txs(
    request, currency: str, tx_hash: str, io_index: Optional[int]
):
    services = get_service_container(request)
    results = await services.txs_service.get_spent_in_txs(currency, tx_hash, io_index)
    return [pydantic_tx_ref_to_openapi(tx_ref) for tx_ref in results]


async def get_spending_txs(
    request, currency: str, tx_hash: str, io_index: Optional[int]
):
    services = get_service_container(request)
    results = await services.txs_service.get_spending_txs(currency, tx_hash, io_index)
    return [pydantic_tx_ref_to_openapi(tx_ref) for tx_ref in results]


async def list_matching_txs(request, currency, expression):
    services = get_service_container(request)
    return await services.txs_service.list_matching_txs(currency, expression)


async def get_tx_conversions(request, currency, tx_hash):
    services = get_service_container(request)
    result = await services.txs_service.get_conversions(currency, tx_hash)
    return [pydantic_external_conversions_to_openapi(conv) for conv in result]
