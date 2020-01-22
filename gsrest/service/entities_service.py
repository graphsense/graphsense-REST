from cassandra.query import SimpleStatement
from cassandra.concurrent import execute_concurrent
from math import floor

from gsrest.db.cassandra import get_session
from gsrest.model.entities import Entity, EntityIncomingRelations, \
    EntityOutgoingRelations, EntityAddress
from gsrest.model.tags import Tag
from gsrest.service.common_service import get_address_by_id_group, \
    get_address_with_tags
from gsrest.service.rates_service import get_rates

BUCKET_SIZE = 25000  # TODO: get BUCKET_SIZE from cassandra
ENTITY_PAGE_SIZE = 100
ENTITY_ADDRESSES_PAGE_SIZE = 100


def get_id_group(id):
    # if BUCKET_SIZE depends on the currency, we need session = ... here
    return floor(id / BUCKET_SIZE)


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
        entity_tags.append(Tag.from_entity_row(row, id_address[row.address_id],
                                               currency).to_dict())

    return entity_tags


def get_entity(currency, entity_id):
    # from entity id to complete entity stats
    session = get_session(currency, 'transformed')
    entity_id_group = get_id_group(entity_id)
    query = "SELECT * FROM cluster WHERE cluster_group = %s AND cluster = %s "
    result = session.execute(query, [entity_id_group, entity_id])
    rates = get_rates(currency)['rates']
    if result:
        return Entity.from_row(result[0], rates).to_dict()
    return None


def list_entity_outgoing_relations(currency, entity_id, paging_state=None,
                                   page_size=None, from_search=False):
    session = get_session(currency, 'transformed')
    entity_id_group = get_id_group(entity_id)
    query = "SELECT * FROM cluster_outgoing_relations WHERE " \
            "src_cluster_group = %s AND src_cluster = %s"
    fetch_size = ENTITY_PAGE_SIZE
    if page_size:
        fetch_size = page_size
    statement = SimpleStatement(query, fetch_size=fetch_size)
    results = session.execute(statement, [entity_id_group, entity_id],
                              paging_state=paging_state)
    paging_state = results.paging_state
    rates = get_rates(currency)['rates']
    relations = []
    for row in results.current_rows:
        relations.append(EntityOutgoingRelations.from_row(row,
                                                          rates,
                                                          from_search)
                         .to_dict())
    return paging_state, relations


def list_entity_incoming_relations(currency, entity_id, paging_state=None,
                                   page_size=None, from_search=False):
    session = get_session(currency, 'transformed')
    entity_id_group = get_id_group(entity_id)
    query = "SELECT * FROM cluster_incoming_relations WHERE " \
            "dst_cluster_group = %s AND dst_cluster = %s"
    fetch_size = ENTITY_PAGE_SIZE
    if page_size:
        fetch_size = page_size
    statement = SimpleStatement(query, fetch_size=fetch_size)
    results = session.execute(statement, [entity_id_group, entity_id],
                              paging_state=paging_state)
    paging_state = results.paging_state
    rates = get_rates(currency)['rates']
    relations = []
    for row in results.current_rows:
        relations.append(EntityIncomingRelations.from_row(row,
                                                          rates,
                                                          from_search)
                         .to_dict())
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


def list_entity_search_neighbors(currency, entity, category, ids, breadth,
                                 depth, skipNumAddresses, cache, outgoing):
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

    if outgoing:
        (_, rows) = cached(entity, 'rows',
                           lambda: list_entity_outgoing_relations(
                               currency, entity, paging_state=None,
                               page_size=breadth, from_search=True))
    else:
        (_, rows) = cached(entity, 'rows',
                           lambda: list_entity_incoming_relations(
                               currency, entity, paging_state=None,
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
            print("empty entity result for " + str(subentity))
            continue

        tags = cached(subentity, 'tags', lambda: list_entity_tags(currency,
                                                                  subentity))

        if category:
            # find first occurrence of category in tags
            match = next((True for t in tags if t["category"] and
                          t["category"].lower() == category.lower()), False)

        matching_addresses = []
        if match and ids:
            matching_addresses = [id["address"] for id in ids
                                  if str(id["entity"]) == str(subentity)]
            match = len(matching_addresses) > 0

        subpaths = False
        if match:
            subpaths = True
        elif 'no_addresses' in props \
                and props['no_addresses'] <= skipNumAddresses:
            subpaths = list_entity_search_neighbors(currency, subentity,
                                                    category, ids, breadth,
                                                    depth - 1,
                                                    skipNumAddresses,
                                                    cache, outgoing)

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
