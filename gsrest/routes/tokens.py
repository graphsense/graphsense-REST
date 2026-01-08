"""Token API routes"""

from fastapi import APIRouter, Depends, Path, Request

from gsrest.dependencies import ServiceContainer
from gsrest.routes.base import (
    get_services,
    get_tagstore_access_groups,
    to_json_response,
)
import gsrest.service.tokens_service as service

router = APIRouter()


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
    "/supported_tokens/",
    summary="Get supported tokens for a currency",
    operation_id="list_supported_tokens",
)
async def list_supported_tokens(
    request: Request,
    currency: str = Path(..., description="The cryptocurrency code (e.g., eth)"),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
):
    """Get supported tokens for a currency"""
    currency = currency.lower()
    adapted_request = RequestAdapter(request, services, tagstore_groups)

    result = await service.list_supported_tokens(
        adapted_request,
        currency=currency,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)
