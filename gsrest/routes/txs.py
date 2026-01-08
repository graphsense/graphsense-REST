"""Transaction API routes"""

from typing import Optional

from fastapi import APIRouter, Depends, Path, Query, Request

from gsrest.dependencies import ServiceContainer
from gsrest.routes.base import (
    get_services,
    get_tagstore_access_groups,
    to_json_response,
)
import gsrest.service.txs_service as service

router = APIRouter()


def _normalize_page(page: Optional[str]) -> Optional[str]:
    """Convert empty string to None for pagination parameter."""
    if page is not None and page.strip() == "":
        return None
    return page


class RequestAdapter:
    """Adapter to make FastAPI Request compatible with existing service layer"""

    def __init__(
        self,
        fastapi_request: Request,
        services: ServiceContainer,
        tagstore_groups: list[str],
    ):
        self._fastapi_request = fastapi_request
        self._services = services
        self._tagstore_groups = tagstore_groups

    @property
    def app(self):
        return self

    def __getitem__(self, key):
        if key == "services":
            return self._services
        elif key == "config":
            return self._fastapi_request.app.state.config
        raise KeyError(key)


def _apply_plugin_hooks(request: Request, result):
    """Apply plugin response hooks"""
    plugins = getattr(request.app.state, "plugins", [])
    plugin_contexts = getattr(request.app.state, "plugin_contexts", {})
    for plugin in plugins:
        if hasattr(plugin, "before_response"):
            ctx = plugin_contexts.get(plugin.__module__, {})
            plugin.before_response(ctx, request, result)


@router.get(
    "/token_txs/{tx_hash}",
    summary="Returns all token transactions in a given transaction",
    operation_id="list_token_txs",
    deprecated=True,
)
async def list_token_txs(
    request: Request,
    currency: str = Path(..., description="The cryptocurrency code (e.g., eth)"),
    tx_hash: str = Path(..., description="The transaction hash"),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
):
    """Returns all token transactions in a given transaction"""
    currency = currency.lower()
    adapted_request = RequestAdapter(request, services, tagstore_groups)

    result = await service.list_token_txs(
        adapted_request,
        currency=currency,
        tx_hash=tx_hash,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)


@router.get(
    "/txs/{tx_hash}",
    summary="Get a transaction by its hash",
    operation_id="get_tx",
)
async def get_tx(
    request: Request,
    currency: str = Path(..., description="The cryptocurrency code (e.g., btc)"),
    tx_hash: str = Path(..., description="The transaction hash"),
    token_tx_id: Optional[int] = Query(
        None, description="Token transaction ID for account-model currencies"
    ),
    include_io: Optional[bool] = Query(
        None, description="Include transaction inputs/outputs"
    ),
    include_nonstandard_io: Optional[bool] = Query(
        None, description="Include non-standard inputs/outputs"
    ),
    include_io_index: Optional[bool] = Query(
        None, description="Include input/output indices"
    ),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
):
    """Get a transaction by its hash"""
    currency = currency.lower()
    adapted_request = RequestAdapter(request, services, tagstore_groups)

    result = await service.get_tx(
        adapted_request,
        currency=currency,
        tx_hash=tx_hash,
        token_tx_id=token_tx_id,
        include_io=include_io,
        include_nonstandard_io=include_nonstandard_io,
        include_io_index=include_io_index,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)


@router.get(
    "/txs/{tx_hash}/spent_in",
    summary="Get transactions that spent outputs from this transaction",
    operation_id="get_spent_in_txs",
)
async def get_spent_in(
    request: Request,
    currency: str = Path(..., description="The cryptocurrency code (e.g., btc)"),
    tx_hash: str = Path(..., description="The transaction hash"),
    io_index: Optional[int] = Query(None, description="Output index to check"),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
):
    """Get transactions that spent outputs from this transaction"""
    currency = currency.lower()
    adapted_request = RequestAdapter(request, services, tagstore_groups)

    result = await service.get_spent_in_txs(
        adapted_request,
        currency=currency,
        tx_hash=tx_hash,
        io_index=io_index,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)


@router.get(
    "/txs/{tx_hash}/spending",
    summary="Get transactions that this transaction is spending from",
    operation_id="get_spending_txs",
)
async def get_spending(
    request: Request,
    currency: str = Path(..., description="The cryptocurrency code (e.g., btc)"),
    tx_hash: str = Path(..., description="The transaction hash"),
    io_index: Optional[int] = Query(None, description="Input index to check"),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
):
    """Get transactions that this transaction is spending from"""
    currency = currency.lower()
    adapted_request = RequestAdapter(request, services, tagstore_groups)

    result = await service.get_spending_txs(
        adapted_request,
        currency=currency,
        tx_hash=tx_hash,
        io_index=io_index,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)


@router.get(
    "/txs/{tx_hash}/conversions",
    summary="Get DeFi conversions for a transaction",
    operation_id="get_tx_conversions",
)
async def get_tx_conversions(
    request: Request,
    currency: str = Path(..., description="The cryptocurrency code (e.g., eth)"),
    tx_hash: str = Path(..., description="The transaction hash"),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
):
    """Get DeFi conversions for a transaction"""
    currency = currency.lower()
    adapted_request = RequestAdapter(request, services, tagstore_groups)

    result = await service.get_tx_conversions(
        adapted_request,
        currency=currency,
        tx_hash=tx_hash,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)


@router.get(
    "/txs/{tx_hash}/flows",
    summary="Get asset flows within a transaction",
    operation_id="list_tx_flows",
)
async def list_tx_flows(
    request: Request,
    currency: str = Path(..., description="The cryptocurrency code (e.g., eth)"),
    tx_hash: str = Path(..., description="The transaction hash"),
    strip_zero_value_txs: Optional[bool] = Query(
        None, description="Strip zero value transactions"
    ),
    only_token_txs: Optional[bool] = Query(
        None, description="Only return token transactions"
    ),
    token_currency: Optional[str] = Query(None, description="Filter by token currency"),
    page: Optional[str] = Query(
        None, description="Resumption token for retrieving the next page"
    ),
    pagesize: Optional[int] = Query(
        None, description="Number of items returned in a single page"
    ),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
):
    """Get asset flows within a transaction"""
    currency = currency.lower()
    adapted_request = RequestAdapter(request, services, tagstore_groups)

    result = await service.list_tx_flows(
        adapted_request,
        currency=currency,
        tx_hash=tx_hash,
        strip_zero_value_txs=strip_zero_value_txs or False,
        only_token_txs=only_token_txs or False,
        token_currency=token_currency,
        page=_normalize_page(page),
        pagesize=pagesize,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)


# NOTE: This route MUST be defined AFTER all other /txs/{tx_hash}/... routes
# because {io} is a catch-all that would match "spent_in", "spending", etc.
@router.get(
    "/txs/{tx_hash}/{io}",
    summary="Get transaction inputs or outputs",
    operation_id="get_tx_io",
)
async def get_tx_io(
    request: Request,
    currency: str = Path(..., description="The cryptocurrency code (e.g., btc)"),
    tx_hash: str = Path(..., description="The transaction hash"),
    io: str = Path(
        ..., description="Input or output values of a transaction (inputs or outputs)"
    ),
    include_nonstandard_io: Optional[bool] = Query(
        None, description="Include non-standard inputs/outputs"
    ),
    include_io_index: Optional[bool] = Query(
        None, description="Include input/output indices"
    ),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
):
    """Get transaction inputs or outputs"""
    currency = currency.lower()
    adapted_request = RequestAdapter(request, services, tagstore_groups)

    result = await service.get_tx_io(
        adapted_request,
        currency=currency,
        tx_hash=tx_hash,
        io=io,
        include_nonstandard_io=include_nonstandard_io,
        include_io_index=include_io_index,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)
