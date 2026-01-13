"""Tags API routes"""

from typing import Optional

from fastapi import APIRouter, Depends, Path, Query, Request
from pydantic import BaseModel

from gsrest.dependencies import ServiceContainer
from gsrest.routes.base import (
    get_services,
    get_show_private_tags,
    get_tagstore_access_groups,
    get_username,
    to_json_response,
)
import gsrest.service.tags_service as service

router = APIRouter()


def _normalize_page(page: Optional[str]) -> Optional[str]:
    """Convert empty string to None for pagination parameter."""
    if page is not None and page.strip() == "":
        return None
    return page


class UserReportedTag(BaseModel):
    """User reported tag model"""

    address: str
    network: str
    actor: Optional[str] = None
    label: str
    description: Optional[str] = None


class RequestAdapter:
    """Adapter to make FastAPI Request compatible with existing service layer"""

    def __init__(
        self,
        fastapi_request: Request,
        services: ServiceContainer,
        tagstore_groups: list[str],
        show_private_tags: bool = None,
        username: Optional[str] = None,
    ):
        self._fastapi_request = fastapi_request
        self._services = services
        self._tagstore_groups = tagstore_groups
        # Auto-detect show_private_tags from tagstore_groups if not explicitly set
        if show_private_tags is None:
            self._show_private_tags = "private" in tagstore_groups
        else:
            self._show_private_tags = show_private_tags
        self._username = username

    @property
    def app(self):
        return self

    def __getitem__(self, key):
        if key == "services":
            return self._services
        elif key == "config":
            return self._fastapi_request.app.state.config
        elif key == "request_config":
            return {"show_private_tags": self._show_private_tags}
        raise KeyError(key)

    @property
    def headers(self):
        return self._fastapi_request.headers


def _apply_plugin_hooks(request: Request, result):
    """Apply plugin response hooks"""
    plugins = getattr(request.app.state, "plugins", [])
    plugin_contexts = getattr(request.app.state, "plugin_contexts", {})
    for plugin in plugins:
        if hasattr(plugin, "before_response"):
            ctx = plugin_contexts.get(plugin.__module__, {})
            plugin.before_response(ctx, request, result)


@router.get(
    "/tags",
    summary="Get address tags by label",
    operation_id="list_address_tags",
)
async def list_address_tags(
    request: Request,
    label: str = Query(..., description="The label to search for"),
    page: Optional[str] = Query(
        None, description="Resumption token for retrieving the next page"
    ),
    pagesize: Optional[int] = Query(
        None, ge=1, description="Number of items returned in a single page"
    ),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
    show_private: bool = Depends(get_show_private_tags),
):
    """Get address tags by label"""
    adapted_request = RequestAdapter(
        request, services, tagstore_groups, show_private_tags=show_private
    )

    result = await service.list_address_tags(
        adapted_request,
        label=label,
        page=_normalize_page(page),
        pagesize=pagesize,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)


@router.get(
    "/tags/actors/{actor}",
    summary="Get an actor by ID",
    operation_id="get_actor",
)
async def get_actor(
    request: Request,
    actor: str = Path(..., description="The actor ID"),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
    show_private: bool = Depends(get_show_private_tags),
):
    """Get an actor by ID"""
    adapted_request = RequestAdapter(
        request, services, tagstore_groups, show_private_tags=show_private
    )

    result = await service.get_actor(
        adapted_request,
        actor=actor,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)


@router.get(
    "/tags/actors/{actor}/tags",
    summary="Get tags associated with an actor",
    operation_id="get_actor_tags",
)
async def get_actor_tags(
    request: Request,
    actor: str = Path(..., description="The actor ID"),
    page: Optional[str] = Query(
        None, description="Resumption token for retrieving the next page"
    ),
    pagesize: Optional[int] = Query(
        None, ge=1, description="Number of items returned in a single page"
    ),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
    show_private: bool = Depends(get_show_private_tags),
):
    """Get tags associated with an actor"""
    adapted_request = RequestAdapter(
        request, services, tagstore_groups, show_private_tags=show_private
    )

    result = await service.get_actor_tags(
        adapted_request,
        actor=actor,
        page=_normalize_page(page),
        pagesize=pagesize,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)


@router.get(
    "/tags/taxonomies",
    summary="List all taxonomies",
    operation_id="list_taxonomies",
)
async def list_taxonomies(
    request: Request,
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
    show_private: bool = Depends(get_show_private_tags),
):
    """List all taxonomies"""
    adapted_request = RequestAdapter(
        request, services, tagstore_groups, show_private_tags=show_private
    )

    result = await service.list_taxonomies(adapted_request)

    _apply_plugin_hooks(request, result)
    return to_json_response(result)


@router.get(
    "/tags/taxonomies/{taxonomy}/concepts",
    summary="List concepts for a taxonomy",
    operation_id="list_concepts",
)
async def list_concepts(
    request: Request,
    taxonomy: str = Path(..., description="The taxonomy name"),
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
    show_private: bool = Depends(get_show_private_tags),
):
    """List concepts for a taxonomy"""
    adapted_request = RequestAdapter(
        request, services, tagstore_groups, show_private_tags=show_private
    )

    result = await service.list_concepts(
        adapted_request,
        taxonomy=taxonomy,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)


@router.post(
    "/tags/report-tag",
    summary="Report a new tag",
    operation_id="report_tag",
)
async def report_tag(
    request: Request,
    body: UserReportedTag,
    services: ServiceContainer = Depends(get_services),
    tagstore_groups: list[str] = Depends(get_tagstore_access_groups),
    show_private: bool = Depends(get_show_private_tags),
    username: Optional[str] = Depends(get_username),
):
    """Report a new tag"""
    adapted_request = RequestAdapter(
        request,
        services,
        tagstore_groups,
        show_private_tags=show_private,
        username=username,
    )

    result = await service.report_tag(
        adapted_request,
        body=body,
    )

    _apply_plugin_hooks(request, result)
    return to_json_response(result)
