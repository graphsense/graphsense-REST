from gsrest.db.cassandra import get_session


def get_address_by_id_group(currency, address_id_group, address_id):
    session = get_session(currency, 'transformed')
    query = "SELECT address FROM address_by_id_group WHERE " \
            "address_id_group = %s and address_id = %s"
    result = session.execute(query, [address_id_group, address_id])
    return result[0].address if result else None


