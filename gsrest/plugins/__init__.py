import abc
import inspect
from typing import Any

# Support both aiohttp and FastAPI request types
try:
    from aiohttp import web as aiohttp_web

    AioHTTPRequest = aiohttp_web.Request
except ImportError:
    AioHTTPRequest = None

try:
    from fastapi import Request as FastAPIRequest
except ImportError:
    FastAPIRequest = None


class Plugin(abc.ABC):
    """Base class for plugins.

    Plugins can implement before_request and before_response hooks to modify
    request handling and responses. The interface is designed to work with
    both aiohttp (legacy) and FastAPI (new) request objects.
    """

    @classmethod
    @abc.abstractmethod
    def before_request(cls, context: dict, request: Any) -> Any:
        """Called before request processing.

        For aiohttp: Can return a modified request or the original.
        For FastAPI: Should modify request.state and return None or a dict
                    of header modifications.
        """
        return request

    @classmethod
    @abc.abstractmethod
    def before_response(cls, context: dict, request: Any, result: Any) -> None:
        """Called after response is prepared but before serialization.

        Can modify the result object in place.
        """
        return


def get_subclass(module):
    klasses = inspect.getmembers(module, inspect.isclass)
    for name, kls in klasses:
        if kls is Plugin:
            continue
        if issubclass(kls, Plugin):
            return kls
    raise TypeError(f"{module.__name__} does not implement " "gsrest.plugins.Plugin")


def is_fastapi_request(request: Any) -> bool:
    """Check if request is a FastAPI Request object."""
    if FastAPIRequest is not None:
        return isinstance(request, FastAPIRequest)
    return False


def is_aiohttp_request(request: Any) -> bool:
    """Check if request is an aiohttp Request object."""
    if AioHTTPRequest is not None:
        return isinstance(request, AioHTTPRequest)
    return False


def get_request_path(request: Any) -> str:
    """Get the request path from either request type."""
    if is_fastapi_request(request):
        return request.url.path
    return request.path


def get_request_query_string(request: Any) -> str:
    """Get the query string from either request type."""
    if is_fastapi_request(request):
        return str(request.query_params)
    return request.query_string


def get_request_header(request: Any, name: str, default: str = "") -> str:
    """Get a header value from either request type."""
    return request.headers.get(name, default)
