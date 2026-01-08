"""General API routes (search, stats)"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, Request

from gsrest.routes.base import (
    get_services,
    get_show_private_tags,
    get_tagstore_access_groups,
    to_json_response,
)
from gsrest.dependencies import ServiceContainer
import gsrest.service.general_service as service

router = APIRouter()


# Create a FastAPI-compatible request adapter for the service layer
class RequestAdapter:
    """Adapter to make FastAPI Request compatible with existing service layer"""

    def __init__(
        self,
        fastapi_request: Request,
        services: ServiceContainer,
        tagstore_groups: list[str],
        show_private_tags: bool = None,
    ):
        self._fastapi_request = fastapi_request
        self._services = services
        self._tagstore_groups = tagstore_groups
        # Auto-detect show_private_tags from tagstore_groups if not explicitly set
        if show_private_tags is None:
            self._show_private_tags = "private" in tagstore_groups
        else:
            self._show_private_tags = show_private_tags
        self._cache = {}

    @property
    def app(self):
        """Return an app-like object compatible with existing service layer"""
        return self

    def __getitem__(self, key):
        if key == "services":
            return self._services
        elif key == "config":
            return self._fastapi_request.app.state.config
        elif key == "openapi":
            return {"info": {"version": "1.16.0rc2"}}
        elif key == "request_config":
            return {"show_private_tags": self._show_private_tags}
        raise KeyError(key)

    @property
    def headers(self):
        return self._fastapi_request.headers


@router.get(
    "/stats",
    summary="Get statistics of supported currencies",
    operation_id="get_statistics",
)
async def get_statistics(
    request: Request,
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
    show_private: bool = Depends(get_show_private_tags),
):
    """Get statistics of supported currencies"""
    # Create adapter for service layer
    adapted_request = RequestAdapter(
        request, services, tagstore_groups, show_private_tags=show_private
    )

    result = await service.get_statistics(adapted_request)

    # Apply plugin response hooks
    plugins = getattr(request.app.state, "plugins", [])
    plugin_contexts = getattr(request.app.state, "plugin_contexts", {})
    for plugin in plugins:
        if hasattr(plugin, "before_response"):
            ctx = plugin_contexts.get(plugin.__module__, {})
            plugin.before_response(ctx, request, result)

    return to_json_response(result)


@router.get(
    "/search",
    summary="Returns matching addresses, transactions and labels",
    operation_id="search",
)
async def search(
    request: Request,
    q: str = Query(..., description="Search query (address, transaction, or label)"),
    currency: Optional[str] = Query(None, description="The cryptocurrency (e.g., btc)"),
    limit: int = Query(10, description="Maximum number of search results"),
    include_sub_tx_identifiers: bool = Query(
        False, description="Whether to include sub-transaction identifiers"
    ),
    include_labels: bool = Query(True, description="Whether to include labels"),
    include_actors: bool = Query(True, description="Whether to include actors"),
    include_txs: bool = Query(True, description="Whether to include transactions"),
    include_addresses: bool = Query(True, description="Whether to include addresses"),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
    show_private: bool = Depends(get_show_private_tags),
):
    """Returns matching addresses, transactions and labels"""
    # Normalize currency
    if currency is not None:
        currency = currency.lower()

    # Create adapter for service layer
    adapted_request = RequestAdapter(
        request, services, tagstore_groups, show_private_tags=show_private
    )

    result = await service.search(
        adapted_request,
        q=q,
        currency=currency,
        limit=limit,
        include_sub_tx_identifiers=include_sub_tx_identifiers,
        include_labels=include_labels,
        include_actors=include_actors,
        include_txs=include_txs,
        include_addresses=include_addresses,
    )

    # Apply plugin response hooks
    plugins = getattr(request.app.state, "plugins", [])
    plugin_contexts = getattr(request.app.state, "plugin_contexts", {})
    for plugin in plugins:
        if hasattr(plugin, "before_response"):
            ctx = plugin_contexts.get(plugin.__module__, {})
            plugin.before_response(ctx, request, result)

    return to_json_response(result)
