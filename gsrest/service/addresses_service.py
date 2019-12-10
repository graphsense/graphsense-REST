from cassandra.query import SimpleStatement

from gsrest.db.cassandra import get_session
from gsrest.model.addresses import AddressTx, \
    AddressOutgoingRelations, AddressIncomingRelations
from gsrest.service.rates_service import get_exchange_rate
from gsrest.service.entities_service import get_entity, get_id_group
from gsrest.service.common_service import get_address_by_id_group, \
    ADDRESS_PREFIX_LENGTH

# TODO: handle failing queries

ADDRESS_PAGE_SIZE = 100


def get_address_id(currency, address):
    session = get_session(currency, 'transformed')
    query = "SELECT address_id FROM address WHERE address_prefix = %s " \
            "AND address = %s"
    result = session.execute(query, [address[:ADDRESS_PREFIX_LENGTH], address])
    return result[0].address_id if result else None


def list_address_txs(currency, address, paging_state=None):
    session = get_session(currency, 'transformed')

    address_id = get_address_id(currency, address)
    address_id_group = get_id_group(address_id)
    query = "SELECT * FROM address_transactions WHERE address_id = %s " \
            "AND address_id_group = %s"
    statement = SimpleStatement(query, fetch_size=ADDRESS_PAGE_SIZE)
    results = session.execute(statement, [address_id, address_id_group],
                              paging_state=paging_state)
    paging_state = results.paging_state
    address_txs = [AddressTx.from_row(row,
                                      address,
                                      get_exchange_rate(currency,
                                                        row.height)['rates'])
                   .to_dict() for row in results.current_rows]

    return paging_state, address_txs


def list_address_outgoing_relations(currency, address, paging_state=None,
                                    page_size=None):
    session = get_session(currency, 'transformed')

    address_id = get_address_id(currency, address)
    address_id_group = get_id_group(address_id)
    query = "SELECT * FROM address_outgoing_relations WHERE " \
            "src_address_id_group = %s AND src_address_id = %s"
    fetch_size = ADDRESS_PAGE_SIZE
    if page_size:
        fetch_size = page_size
    statement = SimpleStatement(query, fetch_size=fetch_size)
    results = session.execute(statement, [address_id_group, address_id],
                              paging_state=paging_state)
    paging_state = results.paging_state
    exchange_rate = get_exchange_rate(currency)['rates']  # TODO: implement default (-1)
    relations = []
    for row in results.current_rows:
        dst_address_id_group = get_id_group(row.dst_address_id)
        dst_address = get_address_by_id_group(currency, dst_address_id_group,
                                              row.dst_address_id)

        relations.append(AddressOutgoingRelations.from_row(row, dst_address,
                                                           exchange_rate)
                         .to_dict())
    return paging_state, relations


def list_address_incoming_relations(currency, address, paging_state=None,
                                    page_size=None):
    session = get_session(currency, 'transformed')

    address_id = get_address_id(currency, address)
    address_id_group = get_id_group(address_id)
    query = "SELECT * FROM address_incoming_relations WHERE " \
            "dst_address_id_group = %s AND dst_address_id = %s"
    fetch_size = ADDRESS_PAGE_SIZE
    if page_size:
        fetch_size = page_size
    statement = SimpleStatement(query, fetch_size=fetch_size)
    results = session.execute(statement, [address_id_group, address_id],
                              paging_state=paging_state)
    paging_state = results.paging_state
    exchange_rate = get_exchange_rate(currency)['rates']  # TODO: implement default (-1)
    relations = []
    for row in results.current_rows:
        src_address_id_group = get_id_group(row.src_address_id)
        src_address = get_address_by_id_group(currency, src_address_id_group,
                                              row.src_address_id)

        relations.append(AddressIncomingRelations.from_row(row, src_address,
                                                           exchange_rate)
                         .to_dict())
    return paging_state, relations


def get_address_entity(currency, address):
    # from address to complete entity stats
    entity_id = get_address_entity_id(currency, address)
    return get_entity(currency, entity_id)


def get_address_entity_id(currency, address):
    # from address to entity id only
    session = get_session(currency, 'transformed')
    address_id = get_address_id(currency, address)
    address_id_group = get_id_group(address_id)
    query = "SELECT cluster FROM address_cluster WHERE address_id_group = %s" \
            " AND address_id = %s "
    result = session.execute(query, [address_id_group, address_id])
    return result[0].cluster if result else None


def list_matching_addresses(currency, expression):
    # TODO: rather slow with bech32 address (loop through pages instead)
    session = get_session(currency, 'transformed')
    query = "SELECT address FROM address WHERE address_prefix = %s"
    statement = SimpleStatement(query, fetch_size=ADDRESS_PAGE_SIZE)
    result = session.execute(statement, [expression[:ADDRESS_PREFIX_LENGTH]])
    return [row.address for row in result
            if row.address.startswith(expression)]
