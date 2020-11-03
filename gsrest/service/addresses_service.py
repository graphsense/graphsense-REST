from cassandra.query import SimpleStatement, ValueSequence

from gsrest.db.cassandra import get_session
from openapi_server.models.address_tx import AddressTx
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
from openapi_server.models.entity_with_tags import EntityWithTags
from openapi_server.models.link import Link
from gsrest.model.addresses import AddressIncomingRelations
from gsrest.service.entities_service import get_entity, get_id_group, \
        list_entity_tags
from gsrest.service.common_service import get_address_by_id_group, \
    ADDRESS_PREFIX_LENGTH
from gsrest.service.rates_service import get_rates, list_rates
import gsrest.service.common_service as commonDAO
from gsrest.model.common import convert_value, compute_balance, make_values
from flask import Response, stream_with_context
from gsrest.util.csvify import create_download_header, to_csv
from gsrest.service.problems import notfound
from gsrest.util.tag_coherence import compute_tag_coherence

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


def get_address_id(currency, address):
    session = get_session(currency, 'transformed')
    query = "SELECT address_id FROM address WHERE address_prefix = %s " \
            "AND address = %s"
    result = session.execute(query, [address[:ADDRESS_PREFIX_LENGTH], address])
    if result:
        return result[0].address_id
    return None


def get_address_id_id_group(currency, address):
    address_id = get_address_id(currency, address)
    if isinstance(address_id, int):
        id_group = get_id_group(address_id)
        return address_id, id_group
    return None, None


def list_address_txs(currency, address, paging_state=None, pagesize=None):
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
                                  paging_state=paging_state)
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


def list_address_neighbors(currency, address, direction, paging_state=None,
                           pagesize=None):
    paging_state = bytes.fromhex(paging_state) if paging_state else None
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


def list_address_outgoing_relations(currency, address, paging_state=None,
                                    page_size=None):
    session = get_session(currency, 'transformed')

    address_id, address_id_group = get_address_id_id_group(currency, address)
    if not address_id:
        notfound("Address {} not found in currency {}".format(address,
                                                              currency))
    query = "SELECT * FROM address_outgoing_relations WHERE " \
            "src_address_id_group = %s AND src_address_id = %s"
    fetch_size = ADDRESS_PAGE_SIZE
    if page_size:
        fetch_size = page_size
    statement = SimpleStatement(query, fetch_size=fetch_size)
    results = session.execute(statement, [address_id_group, address_id],
                              paging_state=paging_state)
    paging_state = results.paging_state
    rates = get_rates(currency)['rates']
    print('rates {}'.format(rates))
    relations = []
    for row in results.current_rows:
        dst_address_id_group = get_id_group(row.dst_address_id)
        dst_address = get_address_by_id_group(currency,
                                              dst_address_id_group,
                                              row.dst_address_id)

        balance = compute_balance(row.dst_properties.total_received.value,
                                  row.dst_properties.total_spent.value)
        print('balance {}'.format(balance))
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


def list_address_incoming_relations(currency, address, paging_state=None,
                                    page_size=None):
    session = get_session(currency, 'transformed')

    address_id, address_id_group = get_address_id_id_group(currency, address)
    if address_id:
        query = "SELECT * FROM address_incoming_relations WHERE " \
                "dst_address_id_group = %s AND dst_address_id = %s"
        fetch_size = ADDRESS_PAGE_SIZE
        if page_size:
            fetch_size = page_size
        statement = SimpleStatement(query, fetch_size=fetch_size)
        results = session.execute(statement, [address_id_group, address_id],
                                  paging_state=paging_state)
        paging_state = results.paging_state
        rates = get_rates(currency)['rates']
        relations = []
        for row in results.current_rows:
            src_address_id_group = get_id_group(row.src_address_id)
            src_address = get_address_by_id_group(currency,
                                                  src_address_id_group,
                                                  row.src_address_id)

            relations.append(AddressIncomingRelations.from_row(row,
                                                               src_address,
                                                               rates)
                             .to_dict())
        return paging_state, relations
    return None, None


def list_address_links(currency, address, neighbor):
    session = get_session(currency, 'transformed')

    address_id, address_id_group = get_address_id_id_group(currency, address)
    neighbor_id, neighbor_id_group = get_address_id_id_group(currency,
                                                             neighbor)
    if address_id is None or neighbor_id is None:
        return notfound("Links between {} and {} not found".format(address,
                                                                   neighbor))

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
    nf = notfound('Entity for address {} not found'.format(address))

    entity_id = get_address_entity_id(currency, address)
    if entity_id is None:
        return nf

    result = get_entity(currency, entity_id)
    if result is None:
        return nf

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


def get_address_entity_id(currency, address):
    # from address to entity id only
    session = get_session(currency, 'transformed')
    address_id, address_id_group = get_address_id_id_group(currency, address)
    if not isinstance(address_id, int):
        return None

    query = "SELECT cluster FROM address_cluster WHERE " \
            "address_id_group = %s AND address_id = %s "
    result = session.execute(query, [address_id_group, address_id])
    print('ROWOW {}'.format(result))
    if result is None or result.one() is None:
        return None

    return result.one().cluster


def list_matching_addresses(currency, expression):
    # TODO: rather slow with bech32 address (loop through pages instead)
    session = get_session(currency, 'transformed')
    query = "SELECT address FROM address WHERE address_prefix = %s"
    statement = SimpleStatement(query, fetch_size=ADDRESS_PAGE_SIZE)
    result = session.execute(statement, [expression[:ADDRESS_PREFIX_LENGTH]])
    return [row.address for row in result
            if row.address.startswith(expression)]
