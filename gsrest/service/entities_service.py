from gsrest.service.common_service import get_address
from gsrest.service.rates_service import get_rates
from openapi_server.models.neighbor_entities import NeighborEntities
from openapi_server.models.neighbor_entity import NeighborEntity
from openapi_server.models.entity import Entity
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.address_tags import AddressTags
from gsrest.util.values import convert_value, to_values
from openapi_server.models.address import Address
from openapi_server.models.entity_addresses import EntityAddresses
from gsrest.db.util import tagstores, tagstores_with_paging
from gsrest.service.tags_service import address_tag_from_row
import gsrest.service.common_service as common
import importlib
import asyncio

MAX_DEPTH = 7


def from_row(currency, row, rates, tags=None, count=0):
    return Entity(
        currency=currency,
        entity=row['cluster_id'],
        root_address=row['root_address'],
        first_tx=TxSummary(
            row['first_tx'].height,
            row['first_tx'].timestamp,
            row['first_tx'].tx_hash.hex()),
        last_tx=TxSummary(
            row['last_tx'].height,
            row['last_tx'].timestamp,
            row['last_tx'].tx_hash.hex()),
        no_addresses=row['no_addresses'],
        no_incoming_txs=row['no_incoming_txs'],
        no_outgoing_txs=row['no_outgoing_txs'],
        total_received=to_values(row['total_received']),
        total_spent=to_values(row['total_spent']),
        in_degree=row['in_degree'],
        out_degree=row['out_degree'],
        balance=convert_value(currency, row['balance'], rates),
        best_address_tag=None if not tags else tags[0],
        no_address_tags=count
        )


async def list_address_tags_by_entity(request, currency, entity,
                                      page=None, pagesize=None):
    address_tags, next_page = \
        await tagstores_with_paging(
                request.app['tagstores'],
                address_tag_from_row,
                'list_address_tags_by_entity',
                page, pagesize,
                currency, entity, request.app['show_private_tags'])
    return AddressTags(address_tags=address_tags, next_page=next_page)


async def get_entity(request, currency, entity):
    db = request.app['db']
    result = await db.get_entity(currency, entity)

    if result is None:
        raise RuntimeError("Entity {} not found".format(entity))

    tags = await tagstores(
            request.app['tagstores'],
            address_tag_from_row,
            'list_entity_tags_by_entity',
            currency, entity, request.app['show_private_tags'])

    rates = (await get_rates(request, currency))['rates']

    counts = await tagstores(
            request.app['tagstores'],
            lambda x: x,
            'count_address_tags_by_entity',
            currency, entity, request.app['show_private_tags'])
    count = 0
    for c in counts:
        count += 0 if c['count'] is None else int(c['count'])
    return from_row(currency, result, rates, tags, count)


async def list_entity_neighbors(request, currency, entity, direction,
                                only_ids=None, include_labels=False,
                                page=None, pagesize=None,
                                relations_only=False):
    results, paging_state = \
           await common.list_neighbors(request, currency, entity, direction,
                                       'entity',
                                       only_ids, include_labels, page,
                                       pagesize)
    is_outgoing = "out" in direction
    dst = 'dst' if is_outgoing else 'src'
    relations = []
    if results is None:
        return NeighborEntities()
    if not relations_only:
        aws = [get_entity(request, currency, row[dst+'_cluster_id'])
               for row in results]

        nodes = await asyncio.gather(*aws)
    else:
        nodes = [r[dst+'_cluster_id'] for r in results]

    for row, node in zip(results, nodes):
        nb = NeighborEntity(
            labels=row['labels'],
            value=row['value'],
            no_txs=row['no_transactions'],
            entity=node)
        relations.append(nb)

    return NeighborEntities(next_page=paging_state,
                            neighbors=relations)


async def list_entity_addresses(request, currency, entity,
                                page=None, pagesize=None):
    db = request.app['db']
    addresses, paging_state = \
        await db.list_entity_addresses(currency, entity, page, pagesize)

    rates = (await get_rates(request, currency))['rates']
    addresses = [Address(
            currency=currency,
            address=row['address'],
            entity=row['cluster_id'],
            first_tx=TxSummary(
                row['first_tx'].height,
                row['first_tx'].timestamp,
                row['first_tx'].tx_hash.hex()),
            last_tx=TxSummary(
                row['last_tx'].height,
                row['last_tx'].timestamp,
                row['last_tx'].tx_hash.hex()),
            no_incoming_txs=row['no_incoming_txs'],
            no_outgoing_txs=row['no_outgoing_txs'],
            total_received=to_values(row['total_received']),
            total_spent=to_values(row['total_spent']),
            in_degree=row['in_degree'],
            out_degree=row['out_degree'],
            balance=convert_value(currency, row['balance'], rates)
            )
            for row in addresses]
    return EntityAddresses(next_page=paging_state, addresses=addresses)


async def search_entity_neighbors(request, currency, entity, direction,
                                  key, value,
                                  depth, breadth, skip_num_addresses=None):
    params = dict()
    db = request.app['db']
    if 'category' in key:
        params['category'] = value[0]

    elif 'total_received' in key or 'balance' in key:
        [curr, min_value, *max_value] = value
        min_value = float(min_value)
        max_value = float(max_value[0]) if len(max_value) > 0 else None
        if max_value is not None and min_value > max_value:
            raise ValueError('Min must not be greater than max')
        params['field'] = (key, curr, min_value, max_value)

    elif 'addresses' in key:
        addresses_list = []
        aws = [db.get_address_entity_id(currency, address)
               for address in value]
        for (address, e) in zip(value, await asyncio.gather(*aws)):
            if e:
                addresses_list.append({"address": address,
                                       "entity": e})
            else:
                raise RuntimeError(
                    "Entity of address {} not found in currency {}"
                    .format(address, currency))
        params['addresses'] = addresses_list

    elif 'entities' in key:
        params['entities'] = value

    level = 1
    result = \
        await recursive_search(request, currency, entity, params,
                               breadth, depth, level, skip_num_addresses,
                               direction)

    return result


async def recursive_search(request, currency, entity, params, breadth, depth,
                           level, skip_num_addresses, direction, cache=None):
    if cache is None:
        cache = dict()
    if depth <= 0:
        return []

    def get_cached(cl, key):
        return (cache.get(cl) or {}).get(key)

    def set_cached(cl, key, value):
        if cl not in cache:
            cache[cl] = {}
        cache[cl][key] = value
        return value

    async def cached(cl, key, get):
        return get_cached(cl, key) or set_cached(cl, key, await get())

    async def list_neighbors(entity, only_ids=None):
        first = (await list_entity_neighbors(
                request, currency, entity, direction, pagesize=breadth,
                only_ids=only_ids)).neighbors
        if only_ids is None or first:
            return first
        return await list_neighbors(entity, None)

    if 'addresses' in params:
        only_ids = [id["entity"] for id in params['addresses']]
    elif 'entities' in params:
        only_ids = [int(e) for e in params['entities']]
    else:
        only_ids = None

    neighbors = await cached(entity, 'neighbors',
                             lambda: list_neighbors(entity, only_ids))

    if level < MAX_DEPTH:
        mod = importlib.import_module(
            f'openapi_server.models.search_result_level{level}')
        levelClass = getattr(mod, f'SearchResultLevel{level}')
    else:
        mod = importlib.import_module(
            'openapi_server.models.search_result_leaf')
        levelClass = getattr(mod, 'SearchResultLeaf')

    async def handle_neighbor(neighbor):
        match = True
        entity = neighbor.entity if isinstance(neighbor.entity, int) else\
            neighbor.entity.entity

        if 'category' in params:
            props = neighbor.entity
            match = props.best_address_tag and \
                props.best_address_tag.category and \
                props.best_address_tag.category.lower() \
                == params['category'].lower()

        matching_addresses = []
        if 'addresses' in params:
            matching_addresses = [id["address"] for id in params['addresses']
                                  if id["entity"] == entity]
            match = len(matching_addresses) > 0

        if 'entities' in params:
            match = str(entity) in params['entities']

        if 'field' in params:
            (field, fieldcurrency, min_value, max_value) = params['field']
            values = getattr(neighbor.entity, field)
            v = None
            if fieldcurrency == 'value':
                v = values.value
            else:
                for f in values.fiat_values:
                    if f.code == fieldcurrency:
                        v = f.value
                        break
            match = v is not None and \
                v >= min_value and \
                (max_value is None or max_value >= v)

        subpaths = False
        if match:
            subpaths = True
        elif level < MAX_DEPTH and \
            (skip_num_addresses is None or
             neighbor.entity.no_addresses is not None and
             neighbor.entity.no_addresses <= skip_num_addresses):
            subpaths = await recursive_search(request,
                                              currency, int(entity),
                                              params, breadth,
                                              depth - 1,
                                              level + 1,
                                              skip_num_addresses,
                                              direction, cache)

        if not subpaths:
            return

        return {'neighbor': neighbor,
                'subpaths': subpaths,
                'matching_addresses': matching_addresses}

    aws = [handle_neighbor(neighbor) for neighbor in neighbors]

    paths = []

    for result in await asyncio.gather(*aws):
        if not result:
            continue

        obj = levelClass(neighbor=result['neighbor'],
                         matching_addresses=[])
        if result['subpaths'] is True:
            aws = [get_address(request, currency, address)
                   for address in result['matching_addresses']]
            addresses = await asyncio.gather(*aws)
            obj.matching_addresses = [address for address in
                                      addresses
                                      if address is not None]
            result['subpaths'] = []
        obj.paths = result['subpaths']
        paths.append(obj)

    return paths


async def list_entity_txs(request, currency, entity, page=None, pagesize=None):
    db = request.app['db']
    results, paging_state = \
        await db.list_entity_txs(currency, entity, page, pagesize)
    entity_txs = await common.txs_from_rows(request, currency, results)
    return AddressTxs(next_page=paging_state, address_txs=entity_txs)


async def list_entity_links(request, currency, entity, neighbor,
                            page=None, pagesize=None):
    db = request.app['db']
    result = await db.list_entity_links(currency, entity, neighbor,
                                        page=page, pagesize=pagesize)

    return await common.links_response(request, currency, result)
