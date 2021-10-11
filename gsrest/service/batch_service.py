import importlib
from flask import Response
from gsrest.util.csvify import create_download_header
from csv import DictWriter
from openapi_server.models.values import Values
import asyncio


async def batch(currency, batch_operation):
    result = ""
    gen = to_csv(currency, batch_operation)
    async for row in gen:
        result += row
    return Response(result,
                    mimetype="text/csv",
                    headers=create_download_header('batch.csv'))


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
    else:
        flat_dict[name[:-1]] = item
    return flat_dict


async def wrap(operation, currency, params):
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
        for (k, v) in params.items():
            if k == 'page':
                continue
            fl[k] = v
        flat.append(fl)
    if page_state:
        params['page'] = page_state
        more = await wrap(operation, currency, params)
        for row in more:
            flat.append(row)
    return flat


async def to_csv(currency, batch_operation):
    page_state = None
    wr = writer()
    csv = None
    mod = importlib.import_module(
        f'gsrest.service.{batch_operation.api}_service')
    operation = getattr(mod, batch_operation.operation)
    aws = []

    for params in batch_operation.parameters:
        params = params.to_dict()
        params = {k: v for (k, v) in params.items() if v}
        if page_state:
            params['page_state'] = page_state
        aw = wrap(operation, currency, params)
        aws.append(aw)

    for op in asyncio.as_completed(aws):
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
