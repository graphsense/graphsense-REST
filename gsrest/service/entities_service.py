from cassandra.query import SimpleStatement

from gsrest.db.cassandra import get_session
from gsrest.service.rates_service import get_exchange_rate
from gsrest.model.tags import Tag
from gsrest.model.entities import Entity, EntityIncomingRelations, \
    EntityOutgoingRelations, EntityAddress
from gsrest.service.common_service import get_address_by_id_group

from math import floor

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
    results = session.execute(query, [entity_group, entity_id])
    entity_tags = []
    for row in results.current_rows:
        address_id_group = get_id_group(row.address_id)
        address = get_address_by_id_group(currency, address_id_group,
                                          row.address_id)
        entity_tags.append(Tag.from_entity_row(row, address, currency)
                           .to_dict())
    return entity_tags


def get_entity(currency, entity_id):
    # from entity id to complete entity stats
    session = get_session(currency, 'transformed')
    entity_id_group = get_id_group(entity_id)
    query = "SELECT * FROM cluster WHERE cluster_group = %s AND cluster = %s "
    result = session.execute(query, [entity_id_group, entity_id])
    exchange_rate = get_exchange_rate(currency)['rates']
    return Entity.from_row(result[0], exchange_rate).to_dict() if result \
        else None


def list_entity_outgoing_relations(currency, entity_id, paging_state=None,
                                   page_size=None):
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
    exchange_rate = get_exchange_rate(currency)['rates']  # TODO: implement default (-1)
    relations = []
    for row in results.current_rows:
        dst_entity = get_entity(currency, row.dst_cluster)
        relations.append(EntityOutgoingRelations.from_row(row, dst_entity,
                                                           exchange_rate)
                         .to_dict())
    return paging_state, relations


def list_entity_incoming_relations(currency, entity_id, paging_state=None,
                                   page_size=None):
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
    exchange_rate = get_exchange_rate(currency)['rates']  # TODO: implement default (-1)
    relations = []
    for row in results.current_rows:
        src_entity = get_entity(currency, row.src_cluster)
        relations.append(EntityIncomingRelations.from_row(row, src_entity,
                                                           exchange_rate)
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
    paging_state = results.paging_state
    exchange_rate = get_exchange_rate(currency)['rates']  # TODO: implement default (-1)
    addresses = []
    for row in results.current_rows:
        address_id_group = get_id_group(row.address_id)
        address = get_address_by_id_group(currency, address_id_group,
                                          row.address_id)
        addresses.append(EntityAddress.from_entity_row(row, address,
                                                       exchange_rate)
                         .to_dict())
    return paging_state, addresses
