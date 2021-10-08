import importlib
from flask import Response, stream_with_context
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


def flatten(flat_dict, item, name=""):
    if type(item) == Values:
        flat_dict[name + 'value'] = item.value
        for rate in item.fiat_values:
            flat_dict[name + rate.code] = rate.value
        return
    if 'to_dict' in dir(item):
        item = item.to_dict()
    if isinstance(item, dict):
        for sub_item in item:
            flatten(flat_dict, item[sub_item], name + sub_item + "_")
    else:
        flat_dict[name[:-1]] = item


async def to_csv(currency, batch_operation):
    flat_dict = {}
    page_state = None
    wr = writer()
    csv = None
    mod = importlib.import_module(
        f'gsrest.service.{batch_operation.api}_service')
    operation = getattr(mod, batch_operation.operation)
    aws = []

    for params in batch_operation.parameters:
        params = params.to_dict()
        params = {k:v for (k,v) in params.items() if v}
        if page_state:
            params['page_state'] = page_state
        aw = operation(currency, **params)
        aws.append(aw)

    for op in asyncio.as_completed(aws):
        result = await op
        if not hasattr(result, 'next_page'):
            rows = [result]
            page_state = None
        else:
            raise RuntimeError('paging not implemented')

        if rows is None:
            raise ValueError('nothing found')

        for row in rows:
            flatten(flat_dict, row)
            if not csv:
                fieldnames = sorted(flat_dict.keys())
                csv = DictWriter(wr, fieldnames)
                csv.writeheader()
                yield wr.get()

            csv.writerow(flat_dict)
            yield wr.get()
            flat_dict = {}

        #if not page_state:
            #break
