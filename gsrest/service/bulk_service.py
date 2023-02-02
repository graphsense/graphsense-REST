import importlib
from csv import DictWriter
from openapi_server.models.values import Values
from openapi_server.models.entity import Entity
from openapi_server.models.address_tag import AddressTag
import asyncio
import json
from aiohttp import web
import traceback
import inspect


def bulk_json(*args, **kwargs):
    kwargs['form'] = 'json'
    return bulk(*args, **kwargs)


def bulk_csv(*args, **kwargs):
    kwargs['form'] = 'csv'
    return bulk(*args, **kwargs)


apis = ['addresses', 'entities', 'blocks', 'txs', 'rates', 'tags']

error_field = '_error'
info_field = '_info'
request_field_prefix = '_request_'


async def bulk(request, currency, operation, body, num_pages, form='csv'):
    try:
        the_stack = stack(request, currency, operation, body, num_pages, form)
    except TypeError as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        text = str(e).replace('positional ', '') \
            .replace('()', '') \
            .replace('keyword ', '')
        raise web.HTTPBadRequest(text=text)

    if form == 'csv':
        gen = to_csv(the_stack)
        mimetype = 'text/csv'
    else:
        gen = to_json(the_stack)
        mimetype = 'application/json'

    response = web.StreamResponse(status=200,
                                  reason='OK',
                                  headers={
                                      'Content-Type':
                                      mimetype,
                                      'Content-Disposition':
                                      f'attachment; filename=bulk.{form}'
                                  })

    response.enable_chunked_encoding()
    await response.prepare(request)

    async for row in gen:
        await response.write(bytes(row, 'utf-8'))
    await response.write_eof()
    return response


class writer:
    def write(self, str):
        self.str = str

    def get(self):
        return self.str


def flatten(item, name="", flat_dict=None, format=None):
    if format == 'json':
        if isinstance(item, dict):
            return item
        return item.to_dict()
    if flat_dict is None:
        # going this way instead of a default argument value
        # like "..., flat_dict = {}):" because
        # default arguments are mutable in python!
        # See https://towardsdatascience.com/python-pitfall-mutable-default-arguments-9385e8265422 # noqa
        flat_dict = {}
    if type(item) == Entity and item.best_address_tag is None:
        item.best_address_tag = AddressTag()
    if type(item) == Values:
        flat_dict[name + 'value'] = item.value
        for rate in item.fiat_values:
            flat_dict[name + rate.code] = rate.value
        return
    if 'to_dict' in dir(item):
        item = item.to_dict(shallow=True)
    if isinstance(item, dict):
        for sub_item in item:
            flatten(item[sub_item], name + sub_item + "_", flat_dict, format)
    elif isinstance(item, list):
        if format == 'csv':
            name = name[:-1]
            item = [i if isinstance(i, str) else str(i) for i in item if i]
            flat_dict[name] = ','.join(item)
            flat_dict[f'{name}_count'] = len(item)
        else:
            flat_dict[name[:-1]] = \
                [flatten(sub_item, format=format) for sub_item in item]
    else:
        flat_dict[name[:-1]] = item
    return flat_dict


async def wrap(request, operation, currency, params, keys, num_pages, format):
    params = dict(params)
    for (k, v) in keys.items():
        params[k] = v
    try:
        result = await operation(request, currency, **params)
    except RuntimeError:
        result = {error_field: 'not found'}
    except ValueError as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        result = {error_field: str(e)}
    except TypeError as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        result = {error_field: str(e)}
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        result = {error_field: 'internal error'}
    if isinstance(result, list):
        rows = result
        page_state = None
    elif not hasattr(result, 'next_page'):
        rows = [result]
        page_state = None
    else:
        result = result.to_dict(shallow=True)
        for k in result:
            if k != 'next_page':
                rows = result[k]
                break
        page_state = result.get('next_page', None)
    flat = []

    def append_keys(fl):
        for (k, v) in keys.items():
            fl[request_field_prefix + k] = v

    for row in rows:
        fl = flatten(row, format=format)
        append_keys(fl)
        flat.append(fl)
    if not rows:
        fl = {}
        append_keys(fl)
        fl[info_field] = 'no data'
        flat.append(fl)
    num_pages -= 1
    if num_pages > 0 and page_state:
        params['page'] = page_state
        more = await wrap(request, operation, currency, params, keys,
                          num_pages, format)
        for row in more:
            flat.append(row)
    return flat


def stack(request, currency, operation, body, num_pages, format):
    try:
        for api in apis:
            mod = importlib.import_module(f'gsrest.service.{api}_service')
            if hasattr(mod, operation):
                operation = getattr(mod, operation)
                break
    except ModuleNotFoundError:
        raise RuntimeError(f'API {api} not found')
    except AttributeError:
        raise RuntimeError(f'{api}.{operation}' ' not found')
    aws = []

    params = {}
    keys = {}
    check = {'request': None, 'currency': currency}
    ln = 0
    for (attr, a) in body.items():
        if a is None:
            continue
        if attr == 'only_ids' or not isinstance(a, list):
            # filter out this param because it's also a list
            # and must not be taken as a key
            params[attr] = a
            check[attr] = a
        elif len(a) > 0:
            keys[attr] = a
            le = len(a)
            ln = min(le, ln) if ln > 0 else le
            check[attr] = a[0]

    if not keys:
        raise TypeError('Keys need to be passed as list')
    inspect.getcallargs(operation, **check)

    for i in range(0, ln):
        the_keys = {}
        for (k, v) in keys.items():
            the_keys[k] = v[i]
        aw = wrap(request, operation, currency, params, the_keys, num_pages,
                  format)

        aws.append(aw)

    return asyncio.as_completed(aws)


async def to_csv(stack):
    wr = writer()
    csv = None

    stash = []
    has_data = False

    for op in stack:
        rows = await op

        for row in rows:

            if error_field in row and not csv:
                stash.append(row)
                continue

            if info_field in row and not csv:
                stash.append(row)
                continue

            head = ""
            has_data = True
            if not csv:
                fieldnames = list(row.keys())
                fieldnames.append(info_field)
                fieldnames.append(error_field)
                fieldnames = sorted(fieldnames)
                csv = DictWriter(wr, fieldnames)
                csv.writeheader()
                head = wr.get()
                yield head

            for stashed_row in stash:
                csv.writerow(stashed_row)
                yield wr.get()

            stash = []

            csv.writerow(row)
            yield wr.get()

    if not has_data:
        for row in stash:
            if not csv:
                fieldnames = list(row.keys())
                if info_field not in fieldnames:
                    fieldnames.append(info_field)
                if error_field not in fieldnames:
                    fieldnames.append(error_field)
                fieldnames = sorted(fieldnames)
                csv = DictWriter(wr, fieldnames)
                csv.writeheader()
                yield wr.get()

            csv.writerow(row)
            yield wr.get()


async def to_json(stack):
    started = False
    yield "["
    for op in stack:
        try:
            rows = await op
        except RuntimeError:
            continue
        if started and rows:
            yield ","
        else:
            started = True

        s = False
        for row in rows:
            if s:
                yield ","
            else:
                s = True
            yield json.dumps(row)
    yield "]"
