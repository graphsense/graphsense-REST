from openapi_server.models.address_txs import AddressTxs
from gsrest.service.entities_service import get_entity, from_row
from gsrest.service.rates_service import get_rates
import gsrest.service.common_service as common
from openapi_server.models.neighbor_addresses import NeighborAddresses
from openapi_server.models.neighbor_address import NeighborAddress
import asyncio


async def get_address(request, currency, address):
    return await common.get_address(request, currency, address)


async def list_tags_by_address(request, currency, address,
                               page=None, pagesize=None):
    return await common.list_tags_by_address(request, currency, address,
                                             page=page, pagesize=pagesize)


async def list_address_txs(request, currency, address,
                           page=None, pagesize=None):
    db = request.app['db']
    results, paging_state = \
        await db.list_address_txs(currency, address, page, pagesize)
    address_txs = await common.txs_from_rows(request, currency, results)
    return AddressTxs(next_page=paging_state, address_txs=address_txs)


async def list_address_neighbors(request, currency, address, direction,
                                 include_labels=False,
                                 page=None, pagesize=None):
    results, paging_state = \
           await common.list_neighbors(request, currency, address, direction,
                                       'address',
                                       include_labels=include_labels,
                                       page=page, pagesize=pagesize, ids=None)
    is_outgoing = "out" in direction
    dst = 'dst' if is_outgoing else 'src'
    relations = []
    if results is None:
        return NeighborAddresses()
    aws = [get_address(request, currency, row[dst+'_address'])
           for row in results]

    nodes = await asyncio.gather(*aws)

    for row, node in zip(results, nodes):
        nb = NeighborAddress(
            labels=row['labels'],
            value=row['value'],
            no_txs=row['no_transactions'],
            address=node)
        relations.append(nb)

    return NeighborAddresses(next_page=paging_state,
                             neighbors=relations)


async def list_address_links(request, currency, address, neighbor,
                             page=None, pagesize=None):
    db = request.app['db']
    result = await db.list_address_links(currency, address, neighbor,
                                         page=page, pagesize=pagesize)

    return await common.links_response(request, currency, result)


async def get_address_entity(request, currency, address):
    # from address to complete entity stats
    e = RuntimeError('Entity for address {} not found'.format(address))
    db = request.app['db']

    entity_id, status = await db.get_address_entity_id(currency, address)
    if entity_id is None:
        raise e

    if status == "new":
        aws = [get_rates(request, currency), db.new_entity(currency, address)]
        [rates, entity] = await asyncio.gather(*aws)
        return from_row(currency, entity, rates['rates'])

    result = await get_entity(request, currency, entity_id)
    if result is None:
        raise e

    return result
