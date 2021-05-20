from gsrest.db import get_connection
from gsrest.service.common_service import get_address
from gsrest.service.rates_service import get_rates
from openapi_server.models.entity import Entity
from openapi_server.models.entities import Entities
from openapi_server.models.tx_summary import TxSummary
from gsrest.util.values import compute_balance, convert_value, make_values
from openapi_server.models.entity_tag import EntityTag
from openapi_server.models.search_result_level1 import SearchResultLevel1
from gsrest.util.tag_coherence import compute_tag_coherence
from flask import Response, stream_with_context
from gsrest.util.csvify import create_download_header, to_csv
from openapi_server.models.address import Address
from openapi_server.models.entity_addresses import EntityAddresses
import gsrest.service.common_service as common
import importlib

MAX_DEPTH = 3


def from_row(row, rates, tags=None):
    tag_coherence = compute_tag_coherence(tag.label for tag in tags) \
                    if tags else None
    return Entity(
        entity=row['cluster'],
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
        total_received=make_values(
            value=row['total_received'].value,
            eur=row['total_received'].eur,
            usd=row['total_received'].usd),
        total_spent=make_values(
            eur=row['total_spent'].eur,
            usd=row['total_spent'].usd,
            value=row['total_spent'].value),
        in_degree=row['in_degree'],
        out_degree=row['out_degree'],
        balance=convert_value(
                compute_balance(
                    row['total_received'].value,
                    row['total_spent'].value,
                ),
                rates),
        tags=tags,
        tag_coherence=tag_coherence
        )


def list_tags_by_entity(currency, entity):
    db = get_connection()
    tags = db.list_tags_by_entity(currency, entity)
    return [EntityTag(label=row.label,
                      entity=row.cluster,
                      category=row.category,
                      abuse=row.abuse,
                      tagpack_uri=row.tagpack_uri,
                      source=row.source,
                      lastmod=row.lastmod,
                      active=True,
                      currency=currency)
            for row in tags]


def list_tags_by_entity_csv(currency, entity):
    def query_function(_):
        tags = list_tags_by_entity(currency, entity)
        return (None, tags)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                        'tags of entity {} ({}).csv'
                        .format(entity,
                                currency.upper())))


def get_entity(currency, entity, include_tags=False):
    db = get_connection()
    result = db.get_entity(currency, entity)

    if result is None:
        raise RuntimeError("Entity {} not found".format(entity))

    tags = list_tags_by_entity(currency, result['cluster']) \
        if include_tags else None
    return from_row(result, get_rates(currency)['rates'], tags)


def list_entities(currency, ids=None, page=None, pagesize=None):
    db = get_connection()
    result, next_page = db.list_entities(currency, ids, page, pagesize)
    rates = get_rates(currency)['rates']
    return Entities(entities=[from_row(row, rates) for row in result],
                    next_page=next_page)


def list_entities_csv(currency, ids):
    def query_function(page_state):
        result = list_entities(currency, ids, page_state)
        return (result.next_page, result.entities)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                            'entities ({}).csv'
                            .format(currency.upper())))


def list_entity_neighbors(currency, entity, direction, ids=None,
                          page=None, pagesize=None):
    return common.list_neighbors(currency, entity, direction, 'entity',
                                 ids=ids, page=page, pagesize=pagesize)


def list_entity_neighbors_csv(currency, entity, direction):
    def query_function(page_state):
        result = list_entity_neighbors(currency, entity, direction,
                                       page=page_state)
        return (result.next_page, result.neighbors)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                            '{} neighbors of entity {} ({}).csv'
                            .format(direction, entity, currency.upper())))


def list_entity_addresses(currency, entity, page=None, pagesize=None):
    db = get_connection()
    addresses, paging_state = \
        db.list_entity_addresses(currency, entity, page, pagesize)

    rates = get_rates(currency)['rates']
    addresses = [Address(
            address=row['address'],
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
            total_received=make_values(
                value=row['total_received'].value,
                eur=row['total_received'].eur,
                usd=row['total_received'].usd),
            total_spent=make_values(
                eur=row['total_spent'].eur,
                usd=row['total_spent'].usd,
                value=row['total_spent'].value),
            in_degree=row['in_degree'],
            out_degree=row['out_degree'],
            balance=convert_value(
                    compute_balance(
                        row['total_received'].value,
                        row['total_spent'].value,
                    ), rates)
            )
            for row in addresses]
    return EntityAddresses(next_page=paging_state, addresses=addresses)


def list_entity_addresses_csv(currency, entity):
    def query_function(page_state):
        result = list_entity_addresses(currency, entity, page_state)
        return (result.next_page, result.addresses)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                            'addresses of entity {} ({}).csv'
                            .format(entity, currency.upper())))


def search_entity_neighbors(currency, entity, direction, key, value, depth, breadth, skip_num_addresses=None):  # noqa: E501
    params = dict()
    db = get_connection()
    if 'category' in key:
        params['category'] = value[0]

    elif 'total_received' in key or 'balance' in key:
        [curr, min_value, *max_value] = value
        max_value = max_value[0] if len(max_value) > 0 else None
        if min_value > max_value:
            raise ValueError('Min must not be greater than max')
        elif curr not in ['value', 'eur', 'usd']:
            raise ValueError('Currency must be one of "value", "eur" or '
                             '"usd"')
        params['field'] = (key, curr, min_value, max_value)

    elif 'addresses' in key:
        addresses_list = []
        for address in value:
            e = db.get_address_entity_id(currency, address)
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
        recursive_search(currency, entity, params,
                         breadth, depth, level, skip_num_addresses,
                         direction)

    def add_tag_coherence(paths):
        if not paths:
            return
        for path in paths:
            path.node.tag_coherence = compute_tag_coherence(
                t.label for t in path.node.tags)
            add_tag_coherence(path.paths)

    add_tag_coherence(result)

    return SearchResultLevel1(paths=result)


def recursive_search(currency, entity, params, breadth, depth, level,
                     skip_num_addresses, direction, cache=None):
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

    def cached(cl, key, get):
        return get_cached(cl, key) or set_cached(cl, key, get())

    neighbors = cached(entity, 'neighbors',
                       lambda: list_entity_neighbors(
                        currency, entity, direction,
                        pagesize=breadth).neighbors)

    paths = []

    for neighbor in neighbors:
        match = True
        props = cached(neighbor.id, 'props',
                       lambda: get_entity(currency, neighbor.id, True))
        if props is None:
            continue

        if 'category' in params:
            # find first occurrence of category in tags
            match = next((True for t in props.tags if t.category and
                          t.category.lower() == params['category'].lower()),
                         False)

        matching_addresses = []
        if 'addresses' in params:
            matching_addresses = [id["address"] for id in params['addresses']
                                  if str(id["entity"]) == str(neighbor.id)]
            match = len(matching_addresses) > 0

        if 'entities' in params:
            match = str(neighbor.id) in params['entities']

        if 'field' in params:
            (field, fieldcurrency, min_value, max_value) = params['field']
            v = getattr(getattr(props, field), fieldcurrency)
            match = v >= min_value and (max_value is None or max_value >= v)

        subpaths = False
        if match:
            subpaths = True
        elif props.no_addresses is not None and \
                level < MAX_DEPTH and \
                (skip_num_addresses is None or
                 props.no_addresses <= skip_num_addresses):
            subpaths = recursive_search(currency, neighbor.id,
                                        params, breadth,
                                        depth - 1,
                                        level + 1,
                                        skip_num_addresses,
                                        direction, cache)

        if not subpaths:
            continue

        if level < MAX_DEPTH:
            mod = importlib.import_module(
                f'openapi_server.models.search_result_level{level}')
            levelClass = getattr(mod, f'SearchResultLevel{level}')
        else:
            mod = importlib.import_module(
                'openapi_server.models.search_result_leaf')
            levelClass = getattr(mod, 'SearchResultLeaf')
        obj = levelClass(node=props, relation=neighbor,
                         matching_addresses=[])
        if subpaths is True:
            addresses_with_tags = [get_address(currency, address, True)
                                   for address in matching_addresses]
            obj.matching_addresses = [address for address in
                                      addresses_with_tags
                                      if address is not None]
            subpaths = None
        obj.paths = subpaths
        paths.append(obj)
    return paths
