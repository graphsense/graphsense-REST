import pdb
from pprint import pprint
from gsrest.service.common_service import get_address
from gsrest.service.rates_service import get_rates
from openapi_server.models.neighbor_entities import NeighborEntities
from openapi_server.models.neighbor_entity import NeighborEntity
from openapi_server.models.entity import Entity
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.labeled_item_ref import LabeledItemRef
from gsrest.util.values import (convert_value, to_values,
                                convert_token_values_map, to_values_tokens)
from openapi_server.models.entity_addresses import EntityAddresses
from gsrest.db.util import tagstores, tagstores_with_paging
from gsrest.service.tags_service import address_tag_from_row
from gsrest.errors import ClusterNotFoundException, BadUserInputException
import gsrest.service.common_service as common
import importlib
import asyncio
import time
from gsrest.util.address import address_to_user_format
from gsrest.db.node_type import NodeType

MAX_DEPTH = 7
TAGS_PAGE_SIZE = 100
SEARCH_TIMEOUT = 300


def from_row(currency,
             row,
             rates,
             token_config,
             tags=None,
             count=0,
             actors=None):
    return Entity(
        currency=currency,
        entity=row['cluster_id'],
        root_address=address_to_user_format(currency, row['root_address']),
        first_tx=TxSummary(row['first_tx'].height, row['first_tx'].timestamp,
                           row['first_tx'].tx_hash.hex()),
        last_tx=TxSummary(row['last_tx'].height, row['last_tx'].timestamp,
                          row['last_tx'].tx_hash.hex()),
        no_addresses=row['no_addresses'],
        no_incoming_txs=row['no_incoming_txs'],
        no_outgoing_txs=row['no_outgoing_txs'],
        total_received=to_values(row['total_received']),
        total_tokens_received=to_values_tokens(
            row.get("total_tokens_received", None)),
        total_spent=to_values(row['total_spent']),
        total_tokens_spent=to_values_tokens(row.get("total_tokens_spent",
                                                    None)),
        in_degree=row['in_degree'],
        out_degree=row['out_degree'],
        balance=convert_value(currency, row['balance'], rates),
        token_balances=convert_token_values_map(
            currency, row.get('token_balances', None), rates, token_config),
        best_address_tag=None if not tags else tags[0],
        no_address_tags=count,
        actors=actors if actors else None)


async def list_address_tags_by_entity(request,
                                      currency,
                                      entity,
                                      page=None,
                                      pagesize=None):
    pagesize = min(pagesize or TAGS_PAGE_SIZE, TAGS_PAGE_SIZE)
    address_tags, next_page = \
        await tagstores_with_paging(
            request.app['tagstores'],
            address_tag_from_row,
            'list_address_tags_by_entity',
            page, pagesize,
            currency, entity,
            request.app['request_config']['show_private_tags'])
    return AddressTags(address_tags=address_tags, next_page=next_page)


async def get_entity(request,
                     currency,
                     entity,
                     exclude_best_address_tag=False,
                     include_actors=False):
    db = request.app['db']
    result = await db.get_entity(currency, entity)

    if result is None:
        raise ClusterNotFoundException(currency, entity)

    tags = None
    count = 0
    if not exclude_best_address_tag:
        tags = await tagstores(
            request.app['tagstores'], address_tag_from_row,
            'get_best_entity_tag', currency, entity,
            request.app['request_config']['show_private_tags'])

    counts = await tagstores(
        request.app['tagstores'], lambda x: x, 'count_address_tags_by_entity',
        currency, entity, request.app['request_config']['show_private_tags'])
    for c in counts:
        count += 0 if c['count'] is None else int(c['count'])

    actors = None
    if include_actors:
        actors = await tagstores(
            request.app['tagstores'],
            lambda row: LabeledItemRef(id=row["id"], label=row["label"]),
            'list_actors_entity', currency, entity,
            request.app['request_config']['show_private_tags'])

    request.app.logger.debug(f'result address {result}')
    rates = (await get_rates(request, currency))['rates']
    return from_row(currency, result, rates,
                    db.get_token_configuration(currency), tags, count, actors)


async def list_entity_neighbors(request,
                                currency,
                                entity,
                                direction,
                                only_ids=None,
                                include_labels=False,
                                page=None,
                                pagesize=None,
                                relations_only=False,
                                exclude_best_address_tag=False,
                                include_actors=False):
    results, paging_state = \
        await common.list_neighbors(request, currency, entity, direction,
                                    NodeType.CLUSTER,
                                    only_ids, include_labels, page,
                                    pagesize)
    is_outgoing = "out" in direction
    dst = 'dst' if is_outgoing else 'src'
    relations = []
    if results is None:
        return NeighborEntities()
    if not relations_only:
        aws = [
            get_entity(request,
                       currency,
                       row[dst + '_cluster_id'],
                       exclude_best_address_tag=exclude_best_address_tag,
                       include_actors=include_actors) for row in results
        ]

        nodes = await asyncio.gather(*aws)
    else:
        nodes = [r[dst + '_cluster_id'] for r in results]

    for row, node in zip(results, nodes):
        nb = NeighborEntity(labels=row['labels'],
                            value=row['value'],
                            token_values=row.get("token_values", None),
                            no_txs=row['no_transactions'],
                            entity=node)
        relations.append(nb)

    return NeighborEntities(next_page=paging_state, neighbors=relations)


async def list_entity_addresses(request,
                                currency,
                                entity,
                                page=None,
                                pagesize=None):
    db = request.app['db']
    addresses, paging_state = \
        await db.list_entity_addresses(currency, entity, page, pagesize)

    rates = (await get_rates(request, currency))['rates']
    addresses = [
        common.address_from_row(
            currency, row, rates, db.get_token_configuration(currency), await
            tagstores(
                request.app['tagstores'],
                lambda row: LabeledItemRef(id=row["id"], label=row["label"]),
                'list_actors_address', currency,
                address_to_user_format(currency, row["address"]),
                request.app['request_config']['show_private_tags']))
        for row in addresses
    ]
    return EntityAddresses(next_page=paging_state, addresses=addresses)


async def search_entity_neighbors(request,
                                  currency,
                                  entity,
                                  direction,
                                  key,
                                  value,
                                  depth,
                                  breadth,
                                  skip_num_addresses=None):
    targets = None
    with_tag = False
    addresses = []
    MAGIC_VALUE_ANY_CATEGORY = '--'

    def stop_neighbor(neighbor):
        return skip_num_addresses is not None \
            and neighbor.entity.no_addresses > skip_num_addresses

    if 'category' in key and value[0] != MAGIC_VALUE_ANY_CATEGORY:
        with_tag = True

        def match_neighbor(neighbor):
            return neighbor.entity.best_address_tag and \
                neighbor.entity.best_address_tag.category == value[0]

    elif 'category' in key and value[0] == MAGIC_VALUE_ANY_CATEGORY:
        with_tag = True

        def match_neighbor(neighbor):
            return neighbor.entity.best_address_tag

    elif 'total_received' in key or 'balance' in key:
        [curr, min_value, *max_value] = value
        min_value = float(min_value)
        max_value = float(max_value[0]) if len(max_value) > 0 else None
        if max_value is not None and min_value > max_value:
            raise BadUserInputException('Min must not be greater than max')

        def match_neighbor(neighbor):
            values = getattr(neighbor.entity, key)
            v = None
            if curr == 'value':
                v = values.value
            else:
                for f in values.fiat_values:
                    if f.code == curr:
                        v = f.value
                        break
            return v is not None and \
                v >= min_value and \
                (max_value is None or max_value >= v)

    elif 'addresses' in key:
        aws = [get_address(request, currency, address) for address in value]
        addresses = await asyncio.gather(*aws)
        addresses_list = [{
            "address": a.address,
            "entity": a.entity
        } for a in addresses if a is not None]

        targets = [id["entity"] for id in addresses_list]

        request.app.logger.debug(f'addresses_list {addresses_list}')

        def match_neighbor(neighbor):
            matching_addresses = [
                id["address"] for id in addresses_list
                if id["entity"] == neighbor.entity.entity
            ]
            request.app.logger.debug(
                f'matching addresses {matching_addresses}')
            return len(matching_addresses) > 0

    elif 'entities' in key:
        targets = [int(v) for v in value]

        def match_neighbor(neighbor):
            return str(neighbor.entity.entity) in value

    async def list_neighbors(entity):
        pagesize = max(breadth, len(targets)) if targets else breadth
        result = await list_entity_neighbors(
            request,
            currency,
            entity,
            direction,
            only_ids=targets,
            exclude_best_address_tag=not with_tag,
            pagesize=pagesize)
        if targets and not result.neighbors:
            result = \
                await list_entity_neighbors(
                    request,
                    currency,
                    entity,
                    direction,
                    only_ids=None,
                    exclude_best_address_tag=not with_tag,
                    pagesize=pagesize)

        return result.neighbors

    def key_accessor(neighbor):
        return neighbor.entity.entity

    result = \
        await bfs(request, entity, key_accessor,
                  list_neighbors, stop_neighbor, match_neighbor,
                  depth, skip_visited=True)

    async def resolve(neighbor):
        if not with_tag:
            neighbor.entity = \
                await get_entity(request, currency, neighbor.entity.entity)
        return neighbor

    async def resolve_path(path):
        aws = [resolve(dst) for dst in path]
        neighbors = list(enumerate(await asyncio.gather(*aws)))
        neighbors.reverse()
        paths = []
        for (i, neighbor) in neighbors:
            level = i + 1
            if level < MAX_DEPTH:
                mod = importlib.import_module(
                    f'openapi_server.models.search_result_level{level}')
                levelClass = getattr(mod, f'SearchResultLevel{level}')
                paths = [
                    levelClass(
                        neighbor=neighbor,
                        matching_addresses=addresses if not paths else [],
                        paths=paths)
                ]
            else:
                mod = importlib.import_module(
                    'openapi_server.models.search_result_leaf')
                levelClass = getattr(mod, 'SearchResultLeaf')
                paths = [
                    levelClass(neighbor=neighbor, matching_addresses=addresses)
                ]
        return paths[0]

    aws = [resolve_path(path) for path in result]
    return await asyncio.gather(*aws)


async def bfs(request,
              node,
              key_accessor,
              list_neighbors,
              stop_neighbor,
              match_neighbor,
              max_depth=3,
              skip_visited=True):

    # collect matching paths
    matching_paths = []

    # maintain a queue of paths
    queue = []

    # visited nodes
    visited = set()

    start = True

    # count number of requests
    no_requests = 0

    start_time = time.time()

    request.app.logger.debug(f"start_time {start_time}")

    request.app.logger.debug(f"seed node {node}")

    pop = 100

    while (start or queue):

        if not start:
            # get first 100 path from the queue
            paths = queue[0:pop]
            queue = queue[pop:]

            # get the last node from the path
            lasts = [key_accessor(path[-1]) for path in paths]
        else:
            paths = [[]]
            lasts = [node]

        start = False

        run_time = time.time() - start_time

        request.app.logger.debug(f"No requests: {no_requests}, " +
                                 f"Queue size: {len(queue)}, " +
                                 f"path length: {len(paths[0])}, " +
                                 f"run time: {run_time}")

        # retrieve neighbors
        def retrieve_neighbor(last):
            return list_neighbors(last)

        no_requests += pop

        aws = [retrieve_neighbor(last) for last in lasts]
        list_of_neighbors = await asyncio.gather(*aws)

        for neighbors, path in zip(list_of_neighbors, paths):
            for neighbor in neighbors:

                id = key_accessor(neighbor)
                new_path = list(path)
                new_path.append(neighbor)

                # found path
                if match_neighbor(neighbor):
                    request.app.logger.debug(f"MATCH {id}")
                    matching_paths.append(new_path)
                    continue

                # stop if max depth is reached
                if len(new_path) == max_depth:
                    request.app.logger.debug("STOP | max depth")
                    continue

                # stop if stop criteria fulfilled
                if (stop_neighbor(neighbor)):
                    request.app.logger.debug(f"STOP {id}")
                    continue

                # stop if node was already visited
                if id in visited:
                    request.app.logger.debug(f"ALREADY VISITED {id}")
                    continue

                if skip_visited:
                    visited.add(id)

                queue.append(new_path)

        if len(queue) == 0 or run_time > SEARCH_TIMEOUT:
            return matching_paths


async def recursive_search(request,
                           currency,
                           entity,
                           params,
                           breadth,
                           depth,
                           level,
                           skip_num_addresses,
                           direction,
                           cache=None):
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
        first = (await list_entity_neighbors(request,
                                             currency,
                                             entity,
                                             direction,
                                             pagesize=breadth,
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
            matching_addresses = [
                id["address"] for id in params['addresses']
                if id["entity"] == entity
            ]
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
            subpaths = await recursive_search(request, currency, int(entity),
                                              params, breadth, depth - 1,
                                              level + 1, skip_num_addresses,
                                              direction, cache)

        if not subpaths:
            return

        return {
            'neighbor': neighbor,
            'subpaths': subpaths,
            'matching_addresses': matching_addresses
        }

    aws = [handle_neighbor(neighbor) for neighbor in neighbors]

    paths = []

    for result in await asyncio.gather(*aws):
        if not result:
            continue

        obj = levelClass(neighbor=result['neighbor'], matching_addresses=[])
        if result['subpaths'] is True:
            aws = [
                get_address(request, currency, address)
                for address in result['matching_addresses']
            ]
            addresses = await asyncio.gather(*aws)
            obj.matching_addresses = [
                address for address in addresses if address is not None
            ]
            result['subpaths'] = []
        obj.paths = result['subpaths']
        paths.append(obj)

    return paths


async def list_entity_txs(request,
                          currency,
                          entity,
                          direction,
                          min_height=None,
                          max_height=None,
                          token_currency=None,
                          page=None,
                          pagesize=None):
    db = request.app['db']
    results, paging_state = \
        await db.list_entity_txs(currency, entity, direction,
                                 min_height, max_height,
                                 token_currency,
                                 page, pagesize
                                 )
    entity_txs = await common.txs_from_rows(
        request, currency, results, db.get_token_configuration(currency))
    return AddressTxs(next_page=paging_state, address_txs=entity_txs)


async def list_entity_links(request,
                            currency,
                            entity,
                            neighbor,
                            page=None,
                            pagesize=None):
    db = request.app['db']
    result = await db.list_entity_links(currency,
                                        entity,
                                        neighbor,
                                        page=page,
                                        pagesize=pagesize)

    return await common.links_response(request, currency, result)
