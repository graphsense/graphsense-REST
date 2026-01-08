"""Plugin middleware for FastAPI

This middleware adapts the existing plugin system (before_request/before_response hooks)
to work with FastAPI's middleware pattern.
"""

from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class PluginMiddleware(BaseHTTPMiddleware):
    """Middleware that invokes plugin before_request hooks.

    Note: before_response hooks are handled at the route level via decorators
    since middleware only sees serialized bytes, not the response objects.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        # Get plugins from app state (may not be set during startup)
        plugins = getattr(request.app.state, "plugins", [])
        plugin_contexts = getattr(request.app.state, "plugin_contexts", {})

        # Initialize request state for plugin data
        request.state.show_private_tags = False
        request.state.header_modifications = {}

        # Execute before_request hooks
        for plugin in plugins:
            if hasattr(plugin, "before_request"):
                ctx = plugin_contexts.get(plugin.__module__, {})
                header_mods = plugin.before_request(ctx, request)
                if header_mods:
                    request.state.header_modifications.update(header_mods)

        # Process request
        response = await call_next(request)

        return response
