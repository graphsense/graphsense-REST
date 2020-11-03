from math import floor
from cassandra.query import SimpleStatement
from cassandra.concurrent import execute_concurrent

from gsrest.db.cassandra import get_session
from gsrest.model.entities import EntityIncomingRelations, \
    EntityOutgoingRelations, EntityAddress
from gsrest.service.common_service import get_address_by_id_group, \
    get_address_with_tags
from gsrest.service.rates_service import get_rates
from openapi_server.models.entity import Entity
from openapi_server.models.tx_summary import TxSummary
from gsrest.model.common import compute_balance, convert_value, make_values
from openapi_server.models.tag import Tag
from openapi_server.models.entity_with_tags import EntityWithTags
from gsrest.util.tag_coherence import compute_tag_coherence

BUCKET_SIZE = 25000  # TODO: get BUCKET_SIZE from cassandra
ENTITY_PAGE_SIZE = 100
ENTITY_ADDRESSES_PAGE_SIZE = 100


def get_id_group(id_):
    # if BUCKET_SIZE depends on the currency, we need session = ... here
    return floor(id_ / BUCKET_SIZE)


def list_entity_tags(currency, entity_id):
    # from entity id to list of tags
    session = get_session(currency, 'transformed')
    entity_group = get_id_group(entity_id)
    query = "SELECT * FROM cluster_tags WHERE cluster_group = %s and cluster" \
            " = %s"
    concurrent_query = "SELECT * FROM address_by_id_group WHERE " \
                       "address_id_group = %s and address_id = %s"

    results = session.execute(query, [entity_group, entity_id])

    # concurrent queries
    statements_and_params = []
    for row in results.current_rows:
        address_id_group = get_id_group(row.address_id)
        params = (address_id_group, row.address_id)
        statements_and_params.append((concurrent_query, params))
    addresses = execute_concurrent(session, statements_and_params,
                                   raise_on_first_error=False)
    id_address = dict()  # to temporary store the id-address mapping
    for (success, address) in addresses:
        if not success:
            pass
        else:
            id_address[address.one().address_id] = address.one().address
    entity_tags = []
    for row in results.current_rows:
        entity_tags.append(Tag(
                    label=row.label,
                    address=row.address,
                    category=row.category,
                    abuse=row.abuse,
                    tagpack_uri=row.tagpack_uri,
                    source=row.source,
                    lastmod=row.lastmod,
                    active=True,
                    currency=currency
                    ))
    return entity_tags


def get_entity_with_tags(currency, entity_id):
    result = get_entity(currency, entity_id)
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


def get_entity(currency, entity_id):
    # from entity id to complete entity stats
    session = get_session(currency, 'transformed')
    entity_id_group = get_id_group(entity_id)
    query = "SELECT * FROM cluster WHERE cluster_group = %s AND cluster = %s "
    result = session.execute(query, [entity_id_group, entity_id])
    if result is None:
        raise RuntimeError("Entity {} not found".format(entity_id))
    result = result.one()
    print('result {}'.format(result))
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


def list_entity_relations(currency, entity_id, is_outgoing, targets=None,
                          paging_state=None, page_size=None,
                          from_search=False):
    if is_outgoing:
        table, this, that = ('outgoing', 'src', 'dst')
        cls = EntityOutgoingRelations
    else:
        table, this, that = ('incoming', 'dst', 'src')
        cls = EntityIncomingRelations

    session = get_session(currency, 'transformed')
    entity_id_group = get_id_group(entity_id)
    has_targets = isinstance(targets, list)
    parameters = [entity_id_group, entity_id]
    basequery = "SELECT * FROM cluster_{}_relations WHERE " \
                "{}_cluster_group = %s AND " \
                "{}_cluster = %s".format(table, this, this)
    if has_targets:
        if len(targets) == 0:
            return None
        query = basequery.replace('*', '{}_cluster'.format(that))
        query += " AND {}_cluster in ({})".format(that, ','.join(targets))
    else:
        query = basequery
    fetch_size = ENTITY_PAGE_SIZE
    if page_size:
        fetch_size = page_size
    statement = SimpleStatement(query, fetch_size=fetch_size)
    results = session.execute(statement, parameters,
                              paging_state=paging_state)
    paging_state = results.paging_state
    current_rows = results.current_rows
    if has_targets:
        statements_and_params = []
        query = basequery + " AND {}_cluster = %s".format(that)
        for row in results.current_rows:
            params = parameters.copy()
            params.append(getattr(row, "{}_cluster".format(that)))
            statements_and_params.append((query, params))
        results = execute_concurrent(session, statements_and_params,
                                     raise_on_first_error=False)
        current_rows = []
        for (success, row) in results:
            if not success:
                pass
            else:
                current_rows.append(row.one())

    rates = get_rates(currency)['rates']
    relations = []
    for row in current_rows:
        relations.append(cls.from_row(row, rates, from_search).to_dict())
    return paging_state, relations


def list_entity_addresses(currency, entity_id, paging_state, page_size):
    session = get_session(currency, 'transformed')
    entity_id_group = get_id_group(entity_id)
    query = "SELECT * FROM cluster_addresses WHERE cluster_group = %s AND " \
            "cluster = %s"
    fetch_size = ENTITY_ADDRESSES_PAGE_SIZE
    if page_size:
        fetch_size = page_size
    statement = SimpleStatement(query, fetch_size=fetch_size)
    results = session.execute(statement, [entity_id_group, entity_id],
                              paging_state=paging_state)
    if results:
        paging_state = results.paging_state
        rates = get_rates(currency)['rates']
        addresses = []
        for row in results.current_rows:
            address_id_group = get_id_group(row.address_id)
            address = get_address_by_id_group(currency, address_id_group,
                                              row.address_id)
            addresses.append(EntityAddress.from_entity_row(row, address,
                                                           rates)
                             .to_dict())
        return paging_state, addresses
    return paging_state, None


def list_entity_search_neighbors(currency, entity, params, breadth, depth,
                                 skip_num_addresses, outgoing, cache=None):
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

    (_, rows) = cached(entity, 'rows',
                       lambda: list_entity_relations(
                           currency, entity, outgoing, paging_state=None,
                           page_size=breadth, from_search=True))

    paths = []

    for row in rows:
        subentity = row['dst_entity'] if outgoing else row['src_entity']
        if not isinstance(subentity, int):
            continue
        match = True
        props = cached(subentity, 'props', lambda: get_entity(currency,
                                                              subentity))
        if props is None:
            continue

        tags = cached(subentity, 'tags', lambda: list_entity_tags(currency,
                                                                  subentity))
        if 'category' in params:
            # find first occurrence of category in tags
            match = next((True for t in tags if t["category"] and
                          t["category"].lower() == params['category'].lower()),
                         False)

        matching_addresses = []
        if 'addresses' in params:
            matching_addresses = [id["address"] for id in params['addresses']
                                  if str(id["entity"]) == str(subentity)]
            match = len(matching_addresses) > 0

        if 'field' in params:
            (field, fieldcurrency, min_value, max_value) = params['field']
            if field == 'final_balance':
                v = props['balance'][fieldcurrency]
            elif field == 'total_received':
                v = props['total_received'][fieldcurrency]
            else:
                v = -1
            match = v >= min_value and (max_value is None or max_value >= v)

        subpaths = False
        if match:
            subpaths = True
        elif 'no_addresses' in props and \
             props['no_addresses'] <= skip_num_addresses:
            subpaths = list_entity_search_neighbors(currency, subentity,
                                                    params, breadth,
                                                    depth - 1,
                                                    skip_num_addresses,
                                                    outgoing, cache)

        if not subpaths:
            continue
        # re-create the right neighbor to respect the model
        row_neighbor = row.copy()
        row_neighbor.pop('src_entity', None)
        row_neighbor.pop('dst_entity', None)

        props["tags"] = tags
        obj = {"node": props, "relation": row_neighbor,
               "matching_addresses": []}
        if subpaths is True:
            addresses_with_tags = [get_address_with_tags(currency, address)
                                   for address in matching_addresses]
            obj["matching_addresses"] = [address for address in
                                         addresses_with_tags
                                         if address is not None]
            subpaths = None
        obj["paths"] = subpaths
        paths.append(obj)
    return paths
