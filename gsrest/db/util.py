import asyncio
import base64
from datetime import timezone
import binascii

from gsrest.errors import (BadUserInputException)

ts_sep = '$'
sep = '|'
encoding = 'ascii'


async def tagstores(tss, wrapper, fun, *args):
    aws = [getattr(ts, fun)(*args) for ts in tss]
    results = await asyncio.gather(*aws)

    return [wrapper(row) for rows, _ in results for row in rows]


def decode_page_handles(page):
    if page is None:
        return {}

    def b64decode(value):
        try:
            return str(base64.b64decode(value.encode(encoding)), encoding)
        except (UnicodeDecodeError, binascii.Error):
            raise BadUserInputException(f"{page} does not look like a"
                                        " valid (base64 encoded) page handle.")

    page = b64decode(page)

    page_handles = {}
    if not page:
        return page_handles
    for ts_handle in page.split(ts_sep):
        [key, value] = ts_handle.split(sep)
        page_handles[key] = b64decode(value)

    return page_handles


def encode_page_handles(pagesAndIds):

    def b64encode(value):
        return str(base64.b64encode(value.encode(encoding)), encoding)

    next_page = None
    for (page, id) in pagesAndIds:
        if page is None:
            continue
        if not isinstance(page, str):
            page = str(page)
        if next_page is not None:
            next_page += ts_sep
        else:
            next_page = ''
        encoded = b64encode(page)
        next_page += id + sep + encoded
    if next_page is None:
        return None
    return b64encode(next_page)


async def tagstores_with_paging(tss, wrapper, fun, page, pagesize, *args):
    page_handles = decode_page_handles(page)

    aws = []
    for ts in tss:
        page = page_handles.get(ts.id(), None)
        f = getattr(ts, fun)
        aws.append(f(*args, page=page, pagesize=pagesize))
        breakpoint()

    results = await asyncio.gather(*aws)

    pagesAndIds = [(page, ts.id()) for (_, page), ts in zip(results, tss)]

    next_page = encode_page_handles(pagesAndIds)

    return [wrapper(row) for rows, _ in results for row in rows], next_page


def dt_to_int(dt):
    return int(dt.replace(tzinfo=timezone.utc).timestamp())
