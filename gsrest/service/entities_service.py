from gsrest.db import get_connection
from gsrest.service.common_service import get_address_with_tags
from gsrest.service.rates_service import get_rates
from openapi_server.models.entity import Entity
from openapi_server.models.tx_summary import TxSummary
from gsrest.util.values import compute_balance, convert_value, make_values
from openapi_server.models.tag import Tag
from openapi_server.models.entity_with_tags import EntityWithTags
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.search_paths import SearchPaths
from gsrest.util.tag_coherence import compute_tag_coherence
from flask import Response, stream_with_context
from gsrest.util.csvify import create_download_header, to_csv
from openapi_server.models.address import Address
from openapi_server.models.entity_addresses import EntityAddresses


def list_entity_tags(currency, entity):
    db = get_connection()
    tags = db.list_entity_tags(currency, entity)
    return [Tag(label=row.label,
                address=row.address,
                category=row.category,
                abuse=row.abuse,
                tagpack_uri=row.tagpack_uri,
                source=row.source,
                lastmod=row.lastmod,
                active=True,
                currency=currency)
            for row in tags]


def list_entity_tags_csv(currency, entity):
    def query_function(_):
        tags = list_entity_tags(currency, entity)
        return (None, tags)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                        'tags of entity {} ({}).csv'
                        .format(entity,
                                currency.upper())))


def get_entity_with_tags(currency, entity):
    result = get_entity(currency, entity)
    tags = list_entity_tags(currency, result.entity)
    return EntityWithTags(
        entity=result.entity,
        first_tx=result.first_tx,
        last_tx=result.last_tx,
        no_addresses=result.no_addresses,
        no_incoming_txs=result.no_incoming_txs,
        no_outgoing_txs=result.no_outgoing_txs,
        total_received=result.total_received,
        total_spent=result.total_spent,
        in_degree=result.in_degree,
        out_degree=result.out_degree,
        balance=result.balance,
        tags=tags,
        tag_coherence=compute_tag_coherence(tag.label for tag in tags)
        )


def get_entity(currency, entity):
    db = get_connection()
    result = db.get_entity(currency, entity)

    if result is None:
        raise RuntimeError("Entity {} not found".format(entity))
    return Entity(
        entity=result.cluster,
        first_tx=TxSummary(
            result.first_tx.height,
            result.first_tx.timestamp,
            result.first_tx.tx_hash.hex()),
        last_tx=TxSummary(
            result.last_tx.height,
            result.last_tx.timestamp,
            result.last_tx.tx_hash.hex()),
        no_addresses=result.no_addresses,
        no_incoming_txs=result.no_incoming_txs,
        no_outgoing_txs=result.no_outgoing_txs,
        total_received=make_values(
            value=result.total_received.value,
            eur=result.total_received.eur,
            usd=result.total_received.usd),
        total_spent=make_values(
            eur=result.total_spent.eur,
            usd=result.total_spent.usd,
            value=result.total_spent.value),
        in_degree=result.in_degree,
        out_degree=result.out_degree,
        balance=convert_value(
                compute_balance(
                    result.total_received.value,
                    result.total_spent.value,
                ),
                get_rates(currency)['rates'])
        )


def list_entity_neighbors(currency, entity, direction, targets=None,
                          page=None, pagesize=None):
    db = get_connection()
    is_outgoing = "out" in direction
    results, paging_state = db.list_entity_neighbors(
                                currency,
                                entity,
                                is_outgoing,
                                targets,
                                page,
                                pagesize)

    rates = get_rates(currency)['rates']
    relations = []
    dst = 'dst' if is_outgoing else 'src'
    for row in results:
        balance = compute_balance(
                    getattr(row, dst+'_properties').total_received.value,
                    getattr(row, dst+'_properties').total_spent.value)
        relations.append(
            Neighbor(
                id=getattr(row, dst+'_cluster'),
                node_type='entity',
                labels=getattr(row, dst+'_labels')
                if getattr(row, dst+'_labels') is not None else [],
                received=make_values(
                    value=getattr(row, dst+'_properties').total_received.value,
                    eur=getattr(row, dst+'_properties').total_received.eur,
                    usd=getattr(row, dst+'_properties').total_received.usd),
                estimated_value=make_values(
                    value=row.value.value,
                    eur=row.value.eur,
                    usd=row.value.usd),
                balance=convert_value(balance, rates),
                no_txs=row.no_transactions))
    return Neighbors(next_page=paging_state, neighbors=relations)


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

    result = \
        recursive_search(currency, entity, params,
                         breadth, depth, skip_num_addresses,
                         direction)

    def add_tag_coherence(paths):
        if not paths:
            return
        for path in paths:
            path.node.tag_coherence = compute_tag_coherence(
                t.label for t in path.node.tags)
            add_tag_coherence(path.paths)

    add_tag_coherence(result)

    return SearchPaths(paths=result)


def recursive_search(currency, entity, params, breadth, depth,
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
                       lambda: get_entity_with_tags(currency, neighbor.id))
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

        if 'field' in params:
            (field, fieldcurrency, min_value, max_value) = params['field']
            v = getattr(getattr(props, field), fieldcurrency)
            match = v >= min_value and (max_value is None or max_value >= v)

        subpaths = False
        if match:
            subpaths = True
        elif props.no_addresses is not None and \
                (skip_num_addresses is None or
                 props.no_addresses <= skip_num_addresses):
            subpaths = recursive_search(currency, neighbor.id,
                                        params, breadth,
                                        depth - 1,
                                        skip_num_addresses,
                                        direction, cache)

        if not subpaths:
            continue

        obj = SearchPaths(node=props, relation=neighbor,
                          matching_addresses=[])
        if subpaths is True:
            addresses_with_tags = [get_address_with_tags(currency, address)
                                   for address in matching_addresses]
            obj.matching_addresses = [address for address in
                                      addresses_with_tags
                                      if address is not None]
            subpaths = None
        obj.paths = subpaths
        paths.append(obj)
    return paths
