from gsrest.db.cassandra import get_session
from gsrest.model.addresses import Address

# TODO: handle failing queries

TXS_PAGE_SIZE = 100


def get_address(currency, address):
    session = get_session(currency, 'transformed')

    query = "SELECT * FROM address WHERE address_prefix = %s AND address = %s"
    result = session.execute(query, [address[:5], address])

    return Address.from_row(result[0]).to_dict() if result else None
