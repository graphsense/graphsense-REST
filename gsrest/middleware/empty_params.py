"""Middleware to normalize empty query parameters.

FastAPI/Pydantic will fail when parsing empty string values for typed parameters.
This middleware converts empty query string values to None before FastAPI processes them.
"""

from urllib.parse import parse_qsl, urlencode
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class EmptyQueryParamsMiddleware(BaseHTTPMiddleware):
    """Convert empty query string values to omitted parameters.

    This ensures compatibility with the old Connexion/OpenAPI behavior where
    empty string query parameters were treated as not provided.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Parse query string
        query_string = request.scope.get("query_string", b"").decode("utf-8")

        if query_string:
            # Parse query params, keeping only non-empty values
            params = parse_qsl(query_string, keep_blank_values=True)
            filtered_params = [(k, v) for k, v in params if v.strip() != ""]

            # Reconstruct query string
            new_query_string = urlencode(filtered_params)

            # Update scope with new query string
            request.scope["query_string"] = new_query_string.encode("utf-8")

        return await call_next(request)
