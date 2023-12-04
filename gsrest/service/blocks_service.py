from openapi_server.models.block import Block
from gsrest.service.rates_service import get_rates
from gsrest.service.txs_service import from_row
from gsrest.errors import NotFoundException
from gsrest.util import is_eth_like


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
        raise NotFoundException("Block {} not found".format(height))
    return block_from_row(currency, row)


async def list_block_txs(request, currency, height):
    db = request.app['db']
    txs = await db.list_block_txs(currency, height)

    if txs is None:
        raise NotFoundException("Block {} not found".format(height))
    rates = await get_rates(request, currency, height)

    return [
        from_row(currency,
                 tx,
                 rates['rates'],
                 db.get_token_configuration(currency),
                 include_io=True) for tx in txs
    ]
