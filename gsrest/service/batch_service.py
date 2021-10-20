import importlib
from flask import Response
from gsrest.util.csvify import create_download_header
from csv import DictWriter
from openapi_server.models.values import Values
import asyncio
import json


async def batch(currency, batch_operation, format='csv'):
    result = ""
    the_stack = stack(currency, batch_operation)
    if format == 'csv':
        gen = to_csv(the_stack)
        mimetype = 'text/csv'
    else:
        gen = to_json(the_stack)
        mimetype = 'application/json'

    async for row in gen:
        result += row
    return Response(result,
                    mimetype=mimetype,
                    headers=create_download_header(f'batch.{format}'))


class writer:
    def write(self, str):
        self.str = str

    def get(self):
        return self.str


def flatten(item, name="", flat_dict=None):
    if flat_dict is None:
        # going this way instead of a default argument value
        # like "..., flat_dict = {}):" because
        # default arguments are mutable in python!
        # See https://towardsdatascience.com/python-pitfall-mutable-default-arguments-9385e8265422 # noqa
        flat_dict = {}
    if type(item) == Values:
        flat_dict[name + 'value'] = item.value
        for rate in item.fiat_values:
            flat_dict[name + rate.code] = rate.value
        return
    if 'to_dict' in dir(item):
        item = item.to_dict()
    if isinstance(item, dict):
        for sub_item in item:
            flatten(item[sub_item], name + sub_item + "_", flat_dict)
    elif isinstance(item, list):
        name = name[:-1]
        item = [i if isinstance(i, str) else str(i)
                for i in item if i]
        flat_dict[name] = ','.join(item)
        flat_dict[f'{name}_count'] = len(item)
    else:
        flat_dict[name[:-1]] = item
    return flat_dict


async def wrap(operation, currency, params, keys):
    params = dict(params)
    for (k, v) in keys.items():
        params[k] = v
    result = await operation(currency, **params)
    if isinstance(result, list):
        rows = result
        page_state = None
    elif not hasattr(result, 'next_page'):
        rows = [result]
        page_state = None
    else:
        result = result.to_dict()
        for k in result:
            if k != 'next_page':
                rows = result[k]
                break
        page_state = result['next_page']
    flat = []
    for row in rows:
        fl = flatten(row)
        for (k, v) in keys.items():
            fl[k] = v
        flat.append(fl)
    if page_state:
        params['page'] = page_state
        more = await wrap(operation, currency, params)
        for row in more:
            flat.append(row)
    return flat


def stack(currency, batch_operation):
    try:
        mod = importlib.import_module(
            f'gsrest.service.{batch_operation.api}_service')
        operation = getattr(mod, batch_operation.operation)
    except ModuleNotFoundError:
        raise RuntimeError(f'API {batch_operation.api} not found')
    except AttributeError:
        raise RuntimeError(f'{batch_operation.api}.{batch_operation.operation}'
                           ' not found')
    aws = []

    params = {}
    keys = {}
    ln = 0
    for (attr, a) in batch_operation.to_dict().items():
        if attr in ['api', 'operation']:
            continue
        if a is None:
            continue
        if attr == 'only_ids' or not isinstance(a, list):
            # filter out this param because it's also a list
            # and must not be taken as a key
            params[attr] = a
        else:
            keys[attr] = a
            le = len(a)
            ln = min(le, ln) if ln > 0 else le

    for i in range(0, ln):
        the_keys = {}
        for (k, v) in keys.items():
            the_keys[k] = v[i]
        aw = wrap(operation, currency, params, the_keys)

        aws.append(aw)

    return asyncio.as_completed(aws)


async def to_csv(stack):
    wr = writer()
    csv = None

    for op in stack:
        try:
            rows = await op
        except RuntimeError:
            continue

        for row in rows:
            head = ""
            if not csv:
                fieldnames = sorted(row.keys())
                csv = DictWriter(wr, fieldnames)
                csv.writeheader()
                head = wr.get()
                yield head

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
        if started:
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
