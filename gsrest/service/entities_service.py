from gsrest.db import get_connection
from gsrest.service.common_service import get_address
from gsrest.service.rates_service import get_rates
from openapi_server.models.entity import Entity
from openapi_server.models.entities import Entities
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.txs import Txs
from gsrest.util.values import compute_balance, convert_value, to_values
from openapi_server.models.entity_tag import EntityTag
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.tags import Tags
from openapi_server.models.search_result_level1 import SearchResultLevel1
from gsrest.util.tag_coherence import compute_tag_coherence
from flask import Response, stream_with_context
from gsrest.util.csvify import create_download_header, to_csv
from openapi_server.models.address import Address
from openapi_server.models.entity_addresses import EntityAddresses
import gsrest.service.common_service as common
import importlib

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
        balance=convert_value(
                currency,
                compute_balance(
                    row['total_received'].value,
                    row['total_spent'].value,
                ),
                rates),
        tags=tags
        )


def list_tags_by_entity(currency, entity, tag_coherence):
    entity_tags = list_entity_tags_by_entity(currency, entity)
    address_tags = list_address_tags_by_entity(currency, entity)
    tag_coherence = compute_tag_coherence(tag.label for tag in address_tags) \
        if tag_coherence else None
    return Tags(entity_tags=entity_tags,
                address_tags=address_tags,
                tag_coherence=tag_coherence)


def list_tags_by_entity_by_level_csv(currency, entity, level):
    def query_function(_):
        tags = list_entity_tags_by_entity(currency, entity) \
            if level == 'entity' \
            else list_address_tags_by_entity(currency, entity)
        return (None, tags)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                        '{} tags of entity {} ({}).csv'
                        .format(level, entity, currency.upper())))


def list_entity_tags_by_entity(currency, entity):
    db = get_connection()
    entity_tags = db.list_entity_tags_by_entity(currency, entity)
    return [EntityTag(label=row['label'],
                      entity=row['cluster_id'],
                      category=row['category'],
                      abuse=row['abuse'],
                      tagpack_uri=row['tagpack_uri'],
                      source=row['source'],
                      lastmod=row['lastmod'],
                      active=True,
                      currency=currency)
            for row in entity_tags]


def list_address_tags_by_entity(currency, entity):
    db = get_connection()
    address_tags = db.list_address_tags_by_entity(currency, entity)
    return [AddressTag(label=row['label'],
                       address=row['address'],
                       category=row['category'],
                       abuse=row['abuse'],
                       tagpack_uri=row['tagpack_uri'],
                       source=row['source'],
                       lastmod=row['lastmod'],
                       active=True,
                       currency=currency)
            for row in address_tags]


def get_entity(currency, entity, include_tags, tag_coherence):
    db = get_connection()
    result = db.get_entity(currency, entity)

    if result is None:
        raise RuntimeError("Entity {} not found".format(entity))

    tags = list_tags_by_entity(currency, result['cluster_id'], tag_coherence) \
        if include_tags else None
    return from_row(currency, result, get_rates(currency)['rates'], tags)


def list_entities(currency, ids=None, page=None, pagesize=None):
    db = get_connection()
    result, next_page = db.list_entities(currency, ids, page, pagesize)
    rates = get_rates(currency)['rates']
    return Entities(entities=[from_row(currency, row, rates)
                              for row in result],
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
                          include_labels=False, page=None, pagesize=None):
    return common.list_neighbors(currency, entity, direction, 'entity',
                                 ids, include_labels, page, pagesize)


def list_entity_neighbors_csv(currency, entity, direction,
                              include_labels=False):
    def query_function(page_state):
        result = list_entity_neighbors(currency, entity, direction,
                                       include_labels=include_labels,
                                       page=page_state)
        return (result.next_page, result.neighbors)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                            '{} neighbors of entity {} ({}).csv'
                            .format(direction, entity, currency.upper())))


async def list_entity_addresses(currency, entity, page=None, pagesize=None):
    db = get_connection()
    addresses, paging_state = \
        await db.list_entity_addresses(currency, entity, page, pagesize)

    rates = get_rates(currency)['rates']
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
            balance=convert_value(
                    currency,
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
        min_value = float(min_value)
        max_value = float(max_value[0]) if len(max_value) > 0 else None
        if max_value is not None and min_value > max_value:
            raise ValueError('Min must not be greater than max')
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
        props = cached(int(neighbor.id), 'props',
                       lambda: get_entity(currency, int(neighbor.id),
                                          True, False))
        if props is None:
            continue

        if 'category' in params:
            # find first occurrence of category in tags
            tags = props.tags.entity_tags + props.tags.address_tags
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
            subpaths = recursive_search(currency, int(neighbor.id),
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


def list_entity_txs(currency, entity, page=None, pagesize=None):
    db = get_connection()
    results, paging_state = \
        db.list_entity_txs(currency, entity, page, pagesize)
    entity_txs = common.txs_from_rows(currency, results)
    return Txs(next_page=paging_state, txs=entity_txs)


def list_entity_txs_csv(currency, entity):
    def query_function(page_state):
        result = list_entity_txs(currency, entity, page_state)
        return (result.next_page, result.txs)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                            'transactions of entity {} ({}).csv'
                            .format(entity, currency.upper())))


def list_entity_links(currency, entity, neighbor,
                      page=None, pagesize=None):
    db = get_connection()
    result = db.list_entity_links(currency, entity, neighbor,
                                  page=page, pagesize=pagesize)

    return common.links_response(currency, result)


def list_entity_links_csv(currency, entity, neighbor):
    def query_function(page_state):
        result = list_entity_links(currency, entity, neighbor,
                                   page=page_state)
        return (result.next_page, result.links)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                            'transactions between {} and {} ({}).csv'
                            .format(entity, neighbor, currency.upper())))
