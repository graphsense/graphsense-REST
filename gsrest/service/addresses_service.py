from openapi_server.models.address_txs import AddressTxs
from gsrest.service.entities_service import get_entity
import gsrest.service.common_service as common


async def get_address(request, currency, address, include_tags=False):
    return await common.get_address(request, currency, address, include_tags)


async def list_tags_by_address(request, currency, address):
    return await common.list_tags_by_address(request, currency, address)


async def list_address_txs(request, currency, address, page=None,
                           pagesize=None):
    db = request.app['db']
    results, paging_state = \
        await db.list_address_txs(currency, address, page, pagesize)
    address_txs = await common.txs_from_rows(request, currency, results)
    return AddressTxs(next_page=paging_state, address_txs=address_txs)


async def list_address_neighbors(request, currency, address, direction,
                                 include_labels=False,
                                 page=None, pagesize=None):
    return await common.list_neighbors(request, currency, address, direction,
                                       'address',
                                       include_labels=include_labels,
                                       page=page, pagesize=pagesize, ids=None)


async def list_address_links(request, currency, address, neighbor,
                             page=None, pagesize=None):
    db = request.app['db']
    print(f'pagesize {pagesize}')
    result = await db.list_address_links(currency, address, neighbor,
                                         page=page, pagesize=pagesize)

    return await common.links_response(request, currency, result)


async def get_address_entity(request, currency, address, include_tags=False,
                             tag_coherence=False):
    # from address to complete entity stats
    e = RuntimeError('Entity for address {} not found'.format(address))
    db = request.app['db']

    entity_id = await db.get_address_entity_id(currency, address)
    if entity_id is None:
        raise e

    result = await get_entity(request, currency, entity_id,
                              include_tags, tag_coherence)
    if result is None:
        raise e

    return result


async def list_matching_addresses(request, currency, expression):
    db = request.app['db']
    return await db.list_matching_addresses(currency, expression)
