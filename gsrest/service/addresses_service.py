from cassandra.query import SimpleStatement

from gsrest.db.cassandra import get_session
from gsrest.model.addresses import Address, AddressTx
from gsrest.model.tags import Tag
from gsrest.service.rates_service import get_exchange_rate
from math import floor
# TODO: handle failing queries

ADDRESS_PREFIX_LENGTH = 5
ADDRESS_PAGE_SIZE = 100
bucket_size = 25000  # TODO: get bucket_size from cassandra


def get_address_id_group(address_id):
    return floor(address_id / bucket_size)


def get_address_id(currency, address):
    session = get_session(currency, 'transformed')
    query = "SELECT address_id FROM address WHERE address_prefix = %s " \
            "AND address = %s"
    result = session.execute(query, [address[:ADDRESS_PREFIX_LENGTH], address])
    return result[0].address_id if result else None


def get_address(currency, address):
    session = get_session(currency, 'transformed')

    query = "SELECT * FROM address WHERE address_prefix = %s AND address = %s"
    result = session.execute(query, [address[:ADDRESS_PREFIX_LENGTH], address])
    return Address.from_row(result[0], get_exchange_rate(currency)['rates'])\
        .to_dict() if result else None


def list_address_txs(currency, address, paging_state=None):
    session = get_session(currency, 'transformed')

    address_id = get_address_id(currency, address)
    address_id_group = get_address_id_group(address_id)
    query = "SELECT * FROM address_transactions WHERE address_id = %s " \
            "AND address_id_group = %s"
    # TODO: add paging_state
    # statement = SimpleStatement(query, fetch_size=ADDRESS_PAGE_SIZE)
    # results = session.execute(statement, paging_state=paging_state)
    results = session.execute(query, [address_id, address_id_group])
    address_txs = [AddressTx.from_row(row,
                                      address,
                                      get_exchange_rate(currency,
                                                        row.height)['rates'])
                   .to_dict() for row in results.current_rows]

    return paging_state, address_txs


def list_address_tags(currency, address):
    session = get_session(currency, 'transformed')

    query = "SELECT * FROM address_tags WHERE address = %s"
    results = session.execute(query, [address])
    address_tags = [Tag.from_row(row, currency).to_dict()
                    for row in results.current_rows]

    return address_tags

