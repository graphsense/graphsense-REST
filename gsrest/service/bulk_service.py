import importlib
from csv import DictWriter, Error as CSVError
from openapi_server.models.values import Values
from openapi_server.models.entity import Entity
from openapi_server.models.address_tag import AddressTag
import asyncio
import json
from aiohttp import web
import traceback
import inspect
import contextlib
from functools import reduce
from gsrest.errors import NotFoundException, BadUserInputException


@contextlib.asynccontextmanager
async def asyncnullcontext():
    yield None


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
        gen = to_csv(the_stack, request.app.logger)
        mimetype = 'text/csv'
    else:
        gen = to_json(the_stack, request.app.logger)
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
    if isinstance(item, Entity) and item.best_address_tag is None:
        item.best_address_tag = AddressTag()
    if isinstance(item, Values):
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
            if not name == "actors":
                flat_dict[f'{name}_count'] = len(item)
        else:
            flat_dict[name[:-1]] = \
                [flatten(sub_item, format=format) for sub_item in item]
    else:
        # if item is not None:
        flat_dict[name[:-1]] = item
    return flat_dict


async def wrap(request, operation, currency, params, keys, num_pages, format,
               max_concurrency_sem_context):
    params = dict(params)
    for (k, v) in keys.items():
        params[k] = v
    try:
        async with max_concurrency_sem_context:
            result = await operation(request, currency, **params)
    except NotFoundException:
        result = {error_field: 'not found'}
    except BadUserInputException as e:
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
                          num_pages, format, max_concurrency_sem_context)
        for row in more:
            flat.append(row)
    return flat


def stack(request, currency, operation, body, num_pages, format):
    for api in apis:
        try:
            mod = importlib.import_module(f'gsrest.service.{api}_service')
            if hasattr(mod, operation):
                operation_name = operation
                operation = getattr(mod, operation)
                break
        except ModuleNotFoundError:
            raise NotFoundException(f'API {api} not found')
        except AttributeError:
            raise NotFoundException(f'{api}.{operation} not found')
    aws = []

    max_concurrency_bulk_operation = request.app['config']['database'].get(
        f"max_concurrency_bulk_{operation_name}", 10)

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

    if operation_name in ["list_entity_txs", "list_entity_addresses"]:
        context = asyncio.Semaphore(max_concurrency_bulk_operation)
    else:
        # async null context, does nothing
        # https://stackoverflow.com/questions/61479059
        # /it-there-any-default-asynchronious-null-context-manager-in-python3-7
        context = contextlib.AsyncExitStack()

    for i in range(0, ln):
        the_keys = {}
        for (k, v) in keys.items():
            the_keys[k] = v[i]
        aw = wrap(request, operation, currency, params, the_keys, num_pages,
                  format, context)

        aws.append(aw)

    return asyncio.as_completed(aws)


async def to_csv(stack, logger):
    wr = writer()

    def is_count_column(row, key):
        postfix = "_count"
        return key.endswith(postfix) and key[:-len(postfix)] in row and type(
            row.get(key, None)) == int

    def write_csv_row(csvwriter, buffer_writer, row, header_columns):
        try:
            # Filter rows not in header rows
            # (otherwise we get an error, unexpected keys)
            # This error is easy to go unnoticed.
            # One situation where such an
            # error is triggered are optional lists
            # (lets call it A) fields,
            # since the first row the function flatten
            # adds an A_count field for
            # every list if the list field is optional
            # it can be none,
            # if the first row has a none value for that
            # optional field the type
            # is not list thus no A_count field is added.
            # Because the first row is
            # used to create the headerline for the csv
            # the A_count is not part of the header
            # but if another row has a value set for A
            # (e.g. type(A)==list) a count field
            # is added. This causes problems since we write the
            # data into a stream
            # thus the header is already out. Also the DictWriter
            # raises a value error
            # on unexpected fields (only count_columns)
            out_row = {
                k: v
                for k, v in row.items()
                if (k in header_columns or not is_count_column(row, k))
            }

            csvwriter.writerow(out_row)
        except (BadUserInputException, CSVError) as e:
            logger.error(f"Error writing bulk row {row}: ({type(e)}) {e}")
            request_fields = {
                k: v
                for k, v in row.items() if k.startswith(request_field_prefix)
            }
            error_and_request_fields = {
                **{
                    error_field: "internal error - can't produce csv"
                },
                **request_fields
            }
            csvwriter.writerow(error_and_request_fields)
        return buffer_writer.get()

    NR_REGULAR_ROWS_USED_TO_INFER_HEADER = 100
    rows_to_infer_header = []
    regular_rows = 0
    ops_rest = []
    for op in stack:
        if regular_rows < NR_REGULAR_ROWS_USED_TO_INFER_HEADER:
            rows = await op
            rows_to_infer_header.extend(rows)
            regular_rows += sum(
                1 for r in rows
                if info_field not in r and error_field not in r)
        else:
            ops_rest.append(op)

    # Infer header
    headerfields = sorted(
        list(
            reduce(set.union, [set(r.keys()) for r in rows_to_infer_header],
                   set()).union(set([error_field, info_field]))))

    csv = DictWriter(wr, headerfields, restval='', extrasaction='ignore')

    # write header
    csv.writeheader()
    head = wr.get()
    yield head

    # write header infer rows
    for row in rows_to_infer_header:
        yield write_csv_row(csv, wr, row, headerfields)

    # write the rest
    for op in ops_rest:
        rows = await op
        for row in rows:
            yield write_csv_row(csv, wr, row, headerfields)


async def to_json(stack, logger):
    started = False
    yield "["
    for op in stack:
        try:
            rows = await op
        except NotFoundException:
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
