from gsrest.db.cassandra import get_session
from gsrest.model.addresses import Address
from gsrest.model.tags import Tag
from gsrest.service.rates_service import get_rates

ADDRESS_PREFIX_LENGTH = 5


def get_address_by_id_group(currency, address_id_group, address_id):
    session = get_session(currency, 'transformed')
    query = "SELECT address FROM address_by_id_group WHERE " \
            "address_id_group = %s and address_id = %s"
    result = session.execute(query, [address_id_group, address_id])
    return result[0].address if result else None


def get_address(currency, address):
    session = get_session(currency, 'transformed')

    query = "SELECT * FROM address WHERE address_prefix = %s AND address = %s"
    result = session.execute(query, [address[:ADDRESS_PREFIX_LENGTH], address])
    if result:
        return Address.from_row(result[0],
                                get_rates(currency)['rates']).to_dict()
    return None


def list_address_tags(currency, address):
    session = get_session(currency, 'transformed')

    query = "SELECT * FROM address_tags WHERE address = %s"
    results = session.execute(query, [address])
    address_tags = [Tag.from_address_row(row, currency, True).to_dict()
                    for row in results.current_rows]

    return address_tags


def get_address_with_tags(currency, address):
    result = get_address(currency, address)
    if result:
        result['tags'] = list_address_tags(currency, address)
    return result
