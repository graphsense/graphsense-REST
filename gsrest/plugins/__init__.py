from aiohttp import web
import abc
import inspect


class Plugin(abc.ABC):

    @abc.abstractclassmethod
    def before_request(cls, request: web.Request):
        return request

    @abc.abstractclassmethod
    def before_response(cls, request: web.Request, result):
        return


def get_subclass(module):
    klasses = inspect.getmembers(module, inspect.isclass)
    print(f'module {module}')
    for (name, kls) in klasses:
        print(f'name {name}')
        if kls is Plugin:
            continue
        if issubclass(kls, Plugin):
            return kls
    raise TypeError(f"{module.__name__} does not implement "
                    "gsrest.plugins.Plugin")
