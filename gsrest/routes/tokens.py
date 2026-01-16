"""Token API routes"""

from fastapi import APIRouter, Depends, Path, Request

from gsrest.dependencies import ServiceContainer
from gsrest.routes.base import (
    RequestAdapter,
    apply_plugin_hooks,
    get_services,
    get_tagstore_access_groups,
    to_json_response,
)
import gsrest.service.tokens_service as service

router = APIRouter()


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

    apply_plugin_hooks(request, result)
    return to_json_response(result)
