"""Base utilities for FastAPI routes"""

import logging
import re
from datetime import datetime
from functools import wraps
from typing import Annotated, Any, Optional

from fastapi import Depends, Header, Request

from gsrest.config import GSRestConfig
from gsrest.dependencies import ServiceContainer

logger = logging.getLogger(__name__)


class RequestAdapter:
    """Adapter to make FastAPI Request compatible with existing service layer.

    This adapter provides a unified interface that the service layer expects,
    bridging FastAPI's Request object with the dict-style access patterns
    used by the service layer.
    """

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
        self._username = username
        self._cache = {}
        self.logger = logger

        # Auto-detect show_private_tags from tagstore_groups if not explicitly set
        if show_private_tags is None:
            self._show_private_tags = "private" in tagstore_groups
        else:
            self._show_private_tags = show_private_tags

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
        elif key == "openapi":
            # Used by general_service for version info
            # Try to get from generated OpenAPI schema, fall back to app version
            schema = getattr(self._fastapi_request.app.state, "openapi_schema", None)
            if schema:
                return schema
            # Fallback: construct minimal openapi info from app
            return {"info": {"version": self._fastapi_request.app.version}}
        raise KeyError(key)

    @property
    def headers(self):
        return self._fastapi_request.headers


def apply_plugin_hooks(request: Request, result):
    """Apply plugin response hooks to a result.

    This function iterates through registered plugins and calls their
    before_response hooks, allowing plugins to modify the response.
    """
    plugins = getattr(request.app.state, "plugins", [])
    plugin_contexts = getattr(request.app.state, "plugin_contexts", {})
    for plugin in plugins:
        if hasattr(plugin, "before_response"):
            ctx = plugin_contexts.get(plugin.__module__, {})
            plugin.before_response(ctx, request, result)


def get_config(request: Request) -> GSRestConfig:
    """Get application config"""
    return request.app.state.config


def get_services(request: Request) -> ServiceContainer:
    """Get service container"""
    return request.app.state.services


def get_request_cache(request: Request) -> dict:
    """Get or create request-scoped cache"""
    if not hasattr(request.state, "cache"):
        request.state.cache = {}
    return request.state.cache


def get_username(
    x_consumer_username: Annotated[Optional[str], Header()] = None,
) -> Optional[str]:
    """Extract username from header"""
    return x_consumer_username


def get_show_private_tags(
    request: Request,
) -> bool:
    """Determine if private tags should be shown based on config and headers"""
    config = request.app.state.config
    show_private_tags_conf = config.show_private_tags or False

    if not show_private_tags_conf:
        return False

    show_private_tags = True
    for k, v in show_private_tags_conf.get("on_header", {}).items():
        hval = request.headers.get(k, None)
        if not hval:
            return False
        show_private_tags = show_private_tags and bool(re.match(re.compile(v), hval))

    # Store in request state for other dependencies
    request.state.show_private_tags = show_private_tags
    return show_private_tags


def get_tagstore_access_groups(
    request: Request,
    show_private: bool = Depends(get_show_private_tags),
) -> list[str]:
    """Get tagstore access groups based on request"""
    config = request.app.state.config
    groups = ["public"]
    if show_private:
        groups.append("private")
    groups.append(config.user_tag_reporting_acl_group)
    return groups


def should_obfuscate_private_tags(request: Request) -> bool:
    """Check if private tags should be obfuscated"""
    from gsrest.builtin.plugins.obfuscate_tags.obfuscate_tags import (
        GROUPS_HEADER_NAME,
        OBFUSCATION_MARKER_GROUP,
    )

    # Check header modifications from middleware
    header_mods = getattr(request.state, "header_modifications", {})
    if header_mods.get(GROUPS_HEADER_NAME) == OBFUSCATION_MARKER_GROUP:
        return True

    return request.headers.get(GROUPS_HEADER_NAME, "") == OBFUSCATION_MARKER_GROUP


def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    """Parse datetime string to datetime object"""
    if dt_str is None:
        return None
    from dateutil import parser

    return parser.parse(dt_str)


def with_plugin_response_hooks(func):
    """Decorator to apply plugin before_response hooks to route handlers.

    This decorator must wrap async route handlers that need plugin response processing.
    The route handler must accept a 'request: Request' parameter.
    """

    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        result = await func(*args, request=request, **kwargs)

        plugins = getattr(request.app.state, "plugins", [])
        plugin_contexts = getattr(request.app.state, "plugin_contexts", {})

        for plugin in plugins:
            if hasattr(plugin, "before_response"):
                ctx = plugin_contexts.get(plugin.__module__, {})
                plugin.before_response(ctx, request, result)

        return result

    return wrapper


def to_json_response(result: Any) -> dict:
    """Convert OpenAPI model result to JSON-serializable dict"""
    if result is None:
        return {}
    elif isinstance(result, list):
        return [d.to_dict() if hasattr(d, "to_dict") else d for d in result]
    elif hasattr(result, "to_dict"):
        return result.to_dict()
    return result


def parse_comma_separated_ints(value: Optional[str]) -> Optional[list[int]]:
    """Parse comma-separated string of integers into a list of integers.

    Used for query params like only_ids that accept CSV format.
    """
    if value is None:
        return None
    if value.strip() == "":
        return None
    return [int(x.strip()) for x in value.split(",") if x.strip()]


def parse_comma_separated_strings(value: Optional[str]) -> Optional[list[str]]:
    """Parse comma-separated string into a list of strings.

    Used for query params like only_ids that accept CSV format.
    """
    if value is None:
        return None
    if value.strip() == "":
        return None
    return [x.strip() for x in value.split(",") if x.strip()]
