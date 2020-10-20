from cassandra.query import SimpleStatement, ValueSequence

from gsrest.db.cassandra import get_session
from openapi_server.models.address_tx import AddressTx
from openapi_server.models.address_txs import AddressTxs
from gsrest.model.addresses import AddressOutgoingRelations, \
    AddressIncomingRelations, Link
from gsrest.service.entities_service import get_entity, get_id_group
from gsrest.service.common_service import get_address_by_id_group, \
    ADDRESS_PREFIX_LENGTH
from gsrest.service.rates_service import get_rates, list_rates
import gsrest.service.common_service as commonDAO
from gsrest.model.common import convert_value
from flask import Response, stream_with_context, abort
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


def list_address_outgoing_relations(currency, address, paging_state=None,
                                    page_size=None):
    session = get_session(currency, 'transformed')

    address_id, address_id_group = get_address_id_id_group(currency, address)
    if address_id:
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
        relations = []
        for row in results.current_rows:
            dst_address_id_group = get_id_group(row.dst_address_id)
            dst_address = get_address_by_id_group(currency,
                                                  dst_address_id_group,
                                                  row.dst_address_id)

            relations.append(AddressOutgoingRelations.from_row(row,
                                                               dst_address,
                                                               rates)
                             .to_dict())
        return paging_state, relations
    return None, None


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


def list_addresses_links(currency, address, neighbor):
    session = get_session(currency, 'transformed')

    address_id, address_id_group = get_address_id_id_group(currency, address)
    neighbor_id, neighbor_id_group = get_address_id_id_group(currency,
                                                             neighbor)
    if address_id and neighbor_id:
        query = "SELECT tx_list FROM address_outgoing_relations WHERE " \
                "src_address_id_group = %s AND src_address_id = %s AND " \
                "dst_address_id = %s"
        results = session.execute(query, [address_id_group, address_id,
                                          neighbor_id])
        if results.current_rows:
            txs = [tx_hash for tx_hash in
                   results.current_rows[0].tx_list]
            query = "SELECT * FROM address_transactions WHERE " \
                    "address_id_group = %s AND address_id = %s AND " \
                    "tx_hash IN %s"
            results1 = session.execute(query, [address_id_group, address_id,
                                               ValueSequence(txs)])
            results2 = session.execute(query, [neighbor_id_group, neighbor_id,
                                               ValueSequence(txs)])
            if results1.current_rows and results2.current_rows:
                links = dict()
                for row in results1.current_rows:
                    hsh = row.tx_hash.hex()
                    links[hsh] = dict()
                    links[hsh]['tx_hash'] = hsh
                    links[hsh]['height'] = row.height
                    links[hsh]['timestamp'] = row.timestamp
                    links[hsh]['input_value'] = row.value
                for row in results2.current_rows:
                    hsh = row.tx_hash.hex()
                    links[hsh]['output_value'] = row.value
                heights = [e['height'] for e in links.values()]
                rates = list_rates(currency, heights)
                return [Link.from_dict(e, rates[e['height']]).to_dict()
                        for e in links.values()]
    return []


def get_address_entity(currency, address):
    # from address to complete entity stats
    entity_id = get_address_entity_id(currency, address)
    if isinstance(entity_id, int):
        return get_entity(currency, entity_id)
    return None


def get_address_entity_id(currency, address):
    # from address to entity id only
    session = get_session(currency, 'transformed')
    address_id, address_id_group = get_address_id_id_group(currency, address)
    if isinstance(address_id, int):
        query = "SELECT cluster FROM address_cluster WHERE " \
                "address_id_group = %s AND address_id = %s "
        result = session.execute(query, [address_id_group, address_id])
        if result:
            return result[0].cluster
    return None


def list_matching_addresses(currency, expression):
    # TODO: rather slow with bech32 address (loop through pages instead)
    session = get_session(currency, 'transformed')
    query = "SELECT address FROM address WHERE address_prefix = %s"
    statement = SimpleStatement(query, fetch_size=ADDRESS_PAGE_SIZE)
    result = session.execute(statement, [expression[:ADDRESS_PREFIX_LENGTH]])
    return [row.address for row in result
            if row.address.startswith(expression)]
