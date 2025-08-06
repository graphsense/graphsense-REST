from datetime import datetime
from typing import Optional, Tuple

from async_lru import alru_cache
from graphsenselib.errors import BadUserInputException, BlockNotFoundException

from gsrest.service.rates_service import get_rates
from gsrest.service.txs_service import from_row
from gsrest.util import is_eth_like
from openapi_server.models.block import Block
from openapi_server.models.block_at_date import BlockAtDate


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
        return Block(
            currency=currency,
            height=row["block_id"],
            block_hash=row["block_hash"].hex(),
            no_txs=row["transaction_count"],
            timestamp=row["timestamp"],
        )
    return Block(
        currency=currency,
        height=row["block_id"],
        block_hash=row["block_hash"].hex(),
        no_txs=row["no_transactions"],
        timestamp=row["timestamp"],
    )


async def get_block(request, currency, height):
    db = request.app["db"]
    row = await db.get_block(currency, height)
    if not row:
        raise BlockNotFoundException(currency, height)
    return block_from_row(currency, row)


async def list_block_txs(request, currency, height):
    db = request.app["db"]
    txs = await db.list_block_txs(currency, height)

    if txs is None:
        raise BlockNotFoundException(currency, height)
    rates = await get_rates(request, currency, height)

    return [
        from_row(
            currency,
            tx,
            rates["rates"],
            db.get_token_configuration(currency),
            include_io=True,
        )
        for tx in txs
    ]


async def get_min_max_height(
    request,
    network,
    min_height: Optional[int],
    max_height: Optional[int],
    min_date: Optional[datetime],
    max_date: Optional[datetime],
) -> Tuple[Optional[int], Optional[int]]:
    if min_date is not None and min_height is not None:
        raise BadUserInputException(
            "Both min_height and min_date parameters are specified. Please chose one."
        )

    if max_date is not None and max_height is not None:
        raise BadUserInputException(
            "Both max_height and max_date parameters are specified. Please chose one."
        )

    if min_height is None and min_date is not None:
        bspec_min = await get_block_by_date(request, network, min_date)
        min_height = bspec_min.before_block

    if max_height is None and max_date is not None:
        bspec_max = await get_block_by_date(request, network, max_date)
        max_height = bspec_max.before_block

    return (min_height, max_height)


@alru_cache(maxsize=1000)
async def find_block_by_ts(get_timestamp, currency, ts, start, end):
    return await find_insertion_point_async(get_timestamp, ts, low=start, high=end)


async def get_block_by_date(request, currency, date):
    db = request.app["db"]
    use_linear_search = request.app["config"]["database"].get(
        "block_by_date_use_linear_search", False
    )
    ts = int(date.timestamp())

    if use_linear_search:
        """
        Expensive method to circumvent the need of having all the blocks
        in the database.
        """

        x = await db.get_block_by_date_allow_filtering(currency, ts)

        if x:
            block = x["block_id"]
            block_before = await db.get_block_below_block_allow_filtering(
                currency, block
            )

            return BlockAtDate(
                before_block=block_before["block_id"],
                before_timestamp=block_before["timestamp"],
                after_block=block,
                after_timestamp=x["timestamp"],
            )
        else:
            return BlockAtDate(
                before_block=None,
                before_timestamp=None,
                after_block=None,
                after_timestamp=None,
            )
    else:
        hb = (await db.get_currency_statistics(currency))["no_blocks"] - 1
        start = 0

        async def get_timestamp(blk):
            bts = await db.get_block_timestamp(currency, blk)
            if bts is None:
                return None
            else:
                return int(bts.get("timestamp", None))

        r = await find_block_by_ts(get_timestamp, currency, ts, start, hb)

        if r == -1 or r > hb:
            r = None
            at = None
            bt = None
        elif r == hb:
            bt = await get_timestamp(r)
            at = None

        else:
            bt = await get_timestamp(r)

            at = await get_timestamp(r + 1)

        return BlockAtDate(
            before_block=r,
            before_timestamp=bt,
            after_block=r + 1 if at is not None else None,
            after_timestamp=at,
        )
