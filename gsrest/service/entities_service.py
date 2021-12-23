from gsrest.service.common_service import get_address
from gsrest.service.rates_service import get_rates
from openapi_server.models.entity import Entity
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.address_txs import AddressTxs
from gsrest.util.values import convert_value, to_values
from openapi_server.models.entity_tag import EntityTag
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.address_and_entity_tags import AddressAndEntityTags
from openapi_server.models.tags import Tags
from openapi_server.models.search_result_level1 import SearchResultLevel1
from openapi_server.models.address import Address
from openapi_server.models.entity_addresses import EntityAddresses
from gsrest.db.util import tagstores_with_paging, dt_to_int
import gsrest.service.common_service as common
import importlib
import asyncio

MAX_DEPTH = 6


def from_row(currency, row, rates, tags=None):
    return Entity(
        entity=row['cluster_id'],
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
        tags=tags
        )


async def list_tags_by_entity(request, currency, entity, level,
                              page=None, pagesize=None):
    if level == 'address':
        address_tags, next_page = \
            await list_address_tags_by_entity(request, currency, entity)
        return Tags(address_tags=address_tags, next_page=next_page)
    else:
        entity_tags, next_page = \
            await list_entity_tags_by_entity(request, currency, entity)
        return Tags(entity_tags=entity_tags, next_page=next_page)


async def list_entity_tags_by_entity(request, currency, entity,
                                     page=None, pagesize=None):
    return await tagstores_with_paging(
            request.app['tagstores'],
            lambda row:
            EntityTag(label=row['label'],
                      entity=row['cluster_id'],
                      category=row['category'],
                      abuse=row['abuse'],
                      tagpack_uri=row['tagpack'],
                      source=row['source'],
                      lastmod=dt_to_int(row['lastmod']),
                      active=True,
                      currency=row['currency'].upper()),
            'list_entity_tags_by_entity',
            page, pagesize,
            currency, entity)


async def list_address_tags_by_entity(request, currency, address,
                                      page=None, pagesize=None):
    return await tagstores_with_paging(
            request.app['tagstores'],
            lambda row:
            AddressTag(label=row['label'],
                       address=row['address'],
                       category=row['category'],
                       abuse=row['abuse'],
                       tagpack_uri=row['tagpack'],
                       source=row['source'],
                       lastmod=dt_to_int(row['lastmod']),
                       active=True,
                       currency=row['currency'].upper()),
            'list_address_tags_by_entity',
            page, pagesize,
            currency, address)


async def get_entity(request, currency, entity, include_tags=False):
    db = request.app['db']
    result = await db.get_entity(currency, entity)

    if result is None:
        raise RuntimeError("Entity {} not found".format(entity))

    tags = None
    if include_tags:
        [(entity_tags, _), (address_tags, _)] = await asyncio.gather(
            list_entity_tags_by_entity(request, currency,
                                       result['cluster_id']),
            list_address_tags_by_entity(request, currency,
                                        result['cluster_id']))
        tags = AddressAndEntityTags(address_tags=address_tags,
                                    entity_tags=entity_tags)
    rates = (await get_rates(request, currency))['rates']
    return from_row(currency, result, rates, tags)


async def list_entity_neighbors(request, currency, entity, direction,
                                only_ids=None, include_labels=False,
                                page=None, pagesize=None):
    return await common.list_neighbors(request, currency, entity, direction,
                                       'entity',
                                       only_ids, include_labels, page,
                                       pagesize)


async def list_entity_addresses(request, currency, entity,
                                page=None, pagesize=None):
    db = request.app['db']
    addresses, paging_state = \
        await db.list_entity_addresses(currency, entity, page, pagesize)

    rates = (await get_rates(request, currency))['rates']
    addresses = [Address(
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

    level = 2
    result = \
        await recursive_search(request, currency, entity, params,
                               breadth, depth, level, skip_num_addresses,
                               direction)

    return SearchResultLevel1(paths=result)


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

    async def list_neighbors(entity):
        return (await list_entity_neighbors(
            request, currency, entity, direction, pagesize=breadth)).neighbors

    async def get_entity_and_tags(entity):
        return await get_entity(request, currency, entity, include_tags=True)

    neighbors = await cached(entity, 'neighbors',
                             lambda: list_neighbors(entity))

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
        props = \
            await cached(int(neighbor.id), 'props',
                         lambda: get_entity_and_tags(int(neighbor.id)))
        if props is None:
            return

        if 'category' in params:
            # find first occurrence of category in tags
            tags = props.tags.entity_tags
            match = next((True for t in tags if t.category and
                          t.category.lower() == params['category'].lower()),
                         False)

        matching_addresses = []
        if 'addresses' in params:
            matching_addresses = [id["address"] for id in params['addresses']
                                  if str(id["entity"]) == neighbor.id]
            match = len(matching_addresses) > 0

        if 'entities' in params:
            match = neighbor.id in params['entities']

        if 'field' in params:
            (field, fieldcurrency, min_value, max_value) = params['field']
            values = getattr(props, field)
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
        elif props.no_addresses is not None and \
                level < MAX_DEPTH and \
                (skip_num_addresses is None or
                 props.no_addresses <= skip_num_addresses):
            subpaths = await recursive_search(request,
                                              currency, int(neighbor.id),
                                              params, breadth,
                                              depth - 1,
                                              level + 1,
                                              skip_num_addresses,
                                              direction, cache)

        if not subpaths:
            return

        return {'props': props,
                'neighbor': neighbor,
                'subpaths': subpaths,
                'matching_addresses': matching_addresses}

    aws = [handle_neighbor(neighbor) for neighbor in neighbors]

    paths = []

    for result in await asyncio.gather(*aws):
        if not result:
            continue

        obj = levelClass(node=result['props'], relation=result['neighbor'],
                         matching_addresses=[])
        if result['subpaths'] is True:
            aws = [get_address(request, currency, address, include_tags=True)
                   for address in result['matching_addresses']]
            addresses_with_tags = await asyncio.gather(*aws)
            obj.matching_addresses = [address for address in
                                      addresses_with_tags
                                      if address is not None]
            result['subpaths'] = None
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
