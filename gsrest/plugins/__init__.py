from aiohttp import web
import abc
import inspect


class Plugin(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def before_request(cls, context, request: web.Request):
        return request

    @classmethod
    @abc.abstractmethod
    def before_response(cls, context, request: web.Request, result):
        return


def get_subclass(module):
    klasses = inspect.getmembers(module, inspect.isclass)
    for name, kls in klasses:
        if kls is Plugin:
            continue
        if issubclass(kls, Plugin):
            return kls
    raise TypeError(f"{module.__name__} does not implement " "gsrest.plugins.Plugin")
