from cassandra.query import SimpleStatement, ValueSequence

from gsrest.db.cassandra import get_session
from openapi_server.models.address_tx import AddressTx
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.link import Link
from gsrest.service.entities_service import get_entity_with_tags, get_id_group
from gsrest.service.common_service import get_address_by_id_group, \
    ADDRESS_PREFIX_LENGTH, get_address_id_id_group, get_address_entity_id
from gsrest.service.rates_service import get_rates, list_rates
import gsrest.service.common_service as commonDAO
from gsrest.model.common import convert_value, compute_balance, make_values
from flask import Response, stream_with_context
from gsrest.util.csvify import create_download_header, to_csv

ADDRESS_PAGE_SIZE = 100


def get_address_with_tags(currency, address):
    return commonDAO.get_address_with_tags(currency, address)


def list_address_tags(currency, address):
    return commonDAO.list_address_tags(currency, address)


def list_address_tags_csv(currency, address):
    def query_function(_):
        tags = commonDAO.list_address_tags(currency, address)
        return (None, tags)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                        'tags of address {} ({}).csv'
                        .format(address,
                                currency.upper())))


def list_address_txs(currency, address, page=None, pagesize=None):
    session = get_session(currency, 'transformed')

    address_id, address_id_group = get_address_id_id_group(currency, address)
    if address_id:
        query = "SELECT * FROM address_transactions WHERE address_id = %s " \
                "AND address_id_group = %s"
        fetch_size = ADDRESS_PAGE_SIZE
        if pagesize:
            fetch_size = pagesize
        statement = SimpleStatement(query, fetch_size=fetch_size)
        results = session.execute(statement, [address_id, address_id_group],
                                  paging_state=page)
        print('result {}'.format(results.current_rows))
        paging_state = results.paging_state
        if results:
            heights = [row.height for row in results.current_rows]
            rates = list_rates(currency, heights)
            address_txs = [AddressTx(
                            address=address,
                            height=row.height,
                            timestamp=row.timestamp,
                            tx_hash=row.tx_hash.hex(),
                            value=convert_value(row.value, rates[row.height])
                            )
                           for row in results.current_rows]
            return AddressTxs(next_page=paging_state, address_txs=address_txs)
    return None, None


def list_address_neighbors(currency, address, direction, page=None,
                           pagesize=None):
    paging_state = bytes.fromhex(page) if page else None
    paging_state, neighbors = \
        list_address_incoming_relations(currency,
                                        address,
                                        paging_state,
                                        pagesize) \
        if "in" in direction else \
        list_address_outgoing_relations(currency,
                                        address,
                                        paging_state,
                                        pagesize)
    return Neighbors(next_page=paging_state.hex() if paging_state else None,
                     neighbors=neighbors)


def list_address_neighbors_csv(currency, address, direction):
    def query_function(page_state):
        result = list_address_neighbors(currency, address, direction,
                                        page_state)
        return (result.next_page, result.neighbors)
    return Response(stream_with_context(to_csv(query_function)),
                    mimetype="text/csv",
                    headers=create_download_header(
                            '{} neighbors of address {} ({}).csv'
                            .format(direction, address, currency.upper())))


def list_address_outgoing_relations(currency, address, page=None,
                                    pagesize=None):
    session = get_session(currency, 'transformed')

    address_id, address_id_group = get_address_id_id_group(currency, address)
    if not address_id:
        raise RuntimeError("Address {} not found in currency {}"
                           .format(address, currency))
    query = "SELECT * FROM address_outgoing_relations WHERE " \
            "src_address_id_group = %s AND src_address_id = %s"
    fetch_size = ADDRESS_PAGE_SIZE
    if pagesize:
        fetch_size = pagesize
    statement = SimpleStatement(query, fetch_size=fetch_size)
    results = session.execute(statement, [address_id_group, address_id],
                              paging_state=page)
    paging_state = results.paging_state
    rates = get_rates(currency)['rates']
    relations = []
    for row in results.current_rows:
        dst_address_id_group = get_id_group(row.dst_address_id)
        dst_address = get_address_by_id_group(currency,
                                              dst_address_id_group,
                                              row.dst_address_id)

        balance = compute_balance(row.dst_properties.total_received.value,
                                  row.dst_properties.total_spent.value)
        relations.append(Neighbor(
                            id=dst_address,
                            node_type='address',
                            labels=row.dst_labels
                            if row.dst_labels is not None else [],
                            received=make_values(
                                value=row.dst_properties.total_received.value,
                                eur=row.dst_properties.total_received.eur,
                                usd=row.dst_properties.total_received.usd),
                            estimated_value=make_values(
                                value=row.estimated_value.value,
                                eur=row.estimated_value.eur,
                                usd=row.estimated_value.usd),
                            balance=convert_value(balance, rates),
                            no_txs=row.no_transactions))
    return paging_state, relations


def list_address_incoming_relations(currency, address, page=None,
                                    pagesize=None):
    session = get_session(currency, 'transformed')

    address_id, address_id_group = get_address_id_id_group(currency, address)
    if not address_id:
        raise RuntimeError("Address {} not found in currency {}"
                           .format(address, currency))
    query = "SELECT * FROM address_incoming_relations WHERE " \
            "dst_address_id_group = %s AND dst_address_id = %s"
    fetch_size = ADDRESS_PAGE_SIZE
    if pagesize:
        fetch_size = pagesize
    statement = SimpleStatement(query, fetch_size=fetch_size)
    results = session.execute(statement, [address_id_group, address_id],
                              paging_state=page)
    paging_state = results.paging_state
    rates = get_rates(currency)['rates']
    relations = []
    for row in results.current_rows:
        src_address_id_group = get_id_group(row.src_address_id)
        src_address = get_address_by_id_group(currency,
                                              src_address_id_group,
                                              row.src_address_id)

        balance = compute_balance(row.src_properties.total_received.value,
                                  row.src_properties.total_spent.value)
        relations.append(Neighbor(
                            id=src_address,
                            node_type='address',
                            labels=row.src_labels
                            if row.src_labels is not None else [],
                            received=make_values(
                                value=row.src_properties.total_received.value,
                                eur=row.src_properties.total_received.eur,
                                usd=row.src_properties.total_received.usd),
                            estimated_value=make_values(
                                value=row.estimated_value.value,
                                eur=row.estimated_value.eur,
                                usd=row.estimated_value.usd),
                            balance=convert_value(balance, rates),
                            no_txs=row.no_transactions))
    return paging_state, relations


def list_address_links(currency, address, neighbor):
    session = get_session(currency, 'transformed')

    address_id, address_id_group = get_address_id_id_group(currency, address)
    neighbor_id, neighbor_id_group = get_address_id_id_group(currency,
                                                             neighbor)
    if address_id is None or neighbor_id is None:
        raise RuntimeError("Links between {} and {} not found"
                           .format(address, neighbor))

    query = "SELECT tx_list FROM address_outgoing_relations WHERE " \
            "src_address_id_group = %s AND src_address_id = %s AND " \
            "dst_address_id = %s"
    results = session.execute(query, [address_id_group, address_id,
                                      neighbor_id])
    if not results.current_rows:
        return []

    txs = [tx_hash for tx_hash in
           results.current_rows[0].tx_list]
    query = "SELECT * FROM address_transactions WHERE " \
            "address_id_group = %s AND address_id = %s AND " \
            "tx_hash IN %s"
    results1 = session.execute(query, [address_id_group, address_id,
                                       ValueSequence(txs)])
    results2 = session.execute(query, [neighbor_id_group, neighbor_id,
                                       ValueSequence(txs)])

    if not results1.current_rows or not results2.current_rows:
        return []

    links = dict()
    heights = [row.height for row in results1.current_rows]
    rates = list_rates(currency, heights)
    for row in results1.current_rows:
        hsh = row.tx_hash.hex()
        links[hsh] = dict()
        links[hsh]['tx_hash'] = hsh
        links[hsh]['height'] = row.height
        links[hsh]['timestamp'] = row.timestamp
        links[hsh]['input_value'] = convert_value(row.value, rates[row.height])
    for row in results2.current_rows:
        hsh = row.tx_hash.hex()
        height = links[hsh]['height']
        links[hsh]['output_value'] = convert_value(row.value, rates[height])
    print('links {}'.format(links))
    return [Link(tx_hash=e['tx_hash'],
                 height=e['height'],
                 timestamp=e['timestamp'],
                 input_value=e['input_value'],
                 output_value=e['output_value']
                 ) for e in links.values()]


def get_address_entity(currency, address):
    # from address to complete entity stats
    e = RuntimeError('Entity for address {} not found'.format(address))

    entity_id = get_address_entity_id(currency, address)
    if entity_id is None:
        raise e

    result = get_entity_with_tags(currency, entity_id)
    if result is None:
        raise e

    return result


def list_matching_addresses(currency, expression):
    session = get_session(currency, 'transformed')
    query = "SELECT address FROM address WHERE address_prefix = %s"
    result = None
    paging_state = None
    statement = SimpleStatement(query, fetch_size=ADDRESS_PAGE_SIZE)
    rows = []
    while result is None or paging_state is not None:
        result = session.execute(
                    statement,
                    [expression[:ADDRESS_PREFIX_LENGTH]],
                    paging_state=paging_state)
        rows += [row.address for row in result
                 if row.address.startswith(expression)]
    return rows
