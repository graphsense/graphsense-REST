from openapi_server.models.block import Block
from openapi_server.models.block_at_date import BlockAtDate
from gsrest.service.rates_service import get_rates
from gsrest.service.txs_service import from_row
from gsrest.errors import BlockNotFoundException
from gsrest.util import is_eth_like
from async_lru import alru_cache


async def find_insertion_point_async(accessor, x, low: int, high: int):
    mid = 0

    while low <= high:

        mid = (high + low) // 2
        mid_item = await accessor(mid)

        # If x is greater, ignore left half
        if mid_item < x:
            low = mid + 1

        # If x is smaller, ignore right half
        elif mid_item > x:
            high = mid - 1

        # means x is present at mid (exact match)
        else:
            return mid

    # If we reach here, then the element was not present\
    return mid - 1 if (mid_item > x) else mid


def block_from_row(currency, row):
    if is_eth_like(currency):
        return Block(currency=currency,
                     height=row['block_id'],
                     block_hash=row['block_hash'].hex(),
                     no_txs=row['transaction_count'],
                     timestamp=row['timestamp'])
    return Block(currency=currency,
                 height=row['block_id'],
                 block_hash=row['block_hash'].hex(),
                 no_txs=row['no_transactions'],
                 timestamp=row['timestamp'])


async def get_block(request, currency, height):
    db = request.app['db']
    row = await db.get_block(currency, height)
    if not row:
        raise BlockNotFoundException(currency, height)
    return block_from_row(currency, row)


async def list_block_txs(request, currency, height):
    db = request.app['db']
    txs = await db.list_block_txs(currency, height)

    if txs is None:
        raise BlockNotFoundException(currency, height)
    rates = await get_rates(request, currency, height)

    return [
        from_row(currency,
                 tx,
                 rates['rates'],
                 db.get_token_configuration(currency),
                 include_io=True) for tx in txs
    ]


@alru_cache(maxsize=1000)
async def find_block_by_ts(get_timestamp, currency, ts, start, end):
    return await find_insertion_point_async(get_timestamp,
                                            ts,
                                            low=start,
                                            high=end)


async def get_block_by_date(request, currency, date):
    db = request.app['db']
    hb = (await db.get_currency_statistics(currency))['no_blocks']
    start = 0
    ts = int(date.timestamp())

    async def get_timestamp(blk):
        return int((await db.get_block_timestamp(currency, blk))['timestamp'])

    r = await find_block_by_ts(get_timestamp, currency, ts, start, hb)

    if r >= hb:
        raise BlockNotFoundException(currency, r)

    bt = await get_timestamp(r)

    if bt > ts and r == 0:
        raise BlockNotFoundException(currency, -1)

    at = await get_timestamp(r + 1)

    assert bt <= ts
    assert at >= ts

    return BlockAtDate(before_block=r,
                       before_timestamp=bt,
                       after_block=r + 1,
                       after_timestamp=at)
