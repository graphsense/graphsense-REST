from math import floor
from gsrest.db.cassandra import get_session
from openapi_server.models.address import Address
from openapi_server.models.address_with_tags import AddressWithTags
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.tag import Tag
from gsrest.util.values import compute_balance, convert_value, make_values
from gsrest.service.rates_service import get_rates
from gsrest.service.problems import notfound

ADDRESS_PREFIX_LENGTH = 5
BUCKET_SIZE = 25000  # TODO: get BUCKET_SIZE from cassandra


def get_address_by_id_group(currency, address_id_group, address_id):
    session = get_session(currency, 'transformed')
    query = "SELECT address FROM address_by_id_group WHERE " \
            "address_id_group = %s and address_id = %s"
    result = session.execute(query, [address_id_group, address_id])
    return result[0].address if result else None


def get_address(currency, address):
    session = get_session(currency, 'transformed')

    query = "SELECT * FROM address WHERE address_prefix = %s AND address = %s"
    result = session.execute(
        query, [address[:ADDRESS_PREFIX_LENGTH], address]).one()
    if not result:
        raise RuntimeError("Address {} not found in currency {}".format(
            address, currency))
    return Address(
        address=result.address,
        first_tx=TxSummary(
            result.first_tx.height,
            result.first_tx.timestamp,
            result.first_tx.tx_hash.hex()),
        last_tx=TxSummary(
            result.last_tx.height,
            result.last_tx.timestamp,
            result.last_tx.tx_hash.hex()),
        no_incoming_txs=result.no_incoming_txs,
        no_outgoing_txs=result.no_outgoing_txs,
        total_received=make_values(
            value=result.total_received.value,
            eur=result.total_received.eur,
            usd=result.total_received.usd),
        total_spent=make_values(
            eur=result.total_spent.eur,
            usd=result.total_spent.usd,
            value=result.total_spent.value),
        in_degree=result.in_degree,
        out_degree=result.out_degree,
        balance=convert_value(
                compute_balance(
                    result.total_received.value,
                    result.total_spent.value,
                ),
                get_rates(currency)['rates'])
        )


def list_address_tags(currency, address):
    session = get_session(currency, 'transformed')

    query = "SELECT * FROM address_tags WHERE address = %s"
    results = session.execute(query, [address])
    if results is None:
        return notfound("Address {} not found in currency {}".format(
            address, currency))
    address_tags = [Tag(
                    label=row.label,
                    address=row.address,
                    category=row.category,
                    abuse=row.abuse,
                    tagpack_uri=row.tagpack_uri,
                    source=row.source,
                    lastmod=row.lastmod,
                    active=True,
                    currency=currency
                    )
                    for row in results.current_rows]

    return address_tags


def get_address_with_tags(currency, address):
    result = get_address(currency, address)
    return AddressWithTags(
        address=result.address,
        first_tx=result.first_tx,
        last_tx=result.last_tx,
        no_incoming_txs=result.no_incoming_txs,
        no_outgoing_txs=result.no_outgoing_txs,
        total_received=result.total_received,
        total_spent=result.total_spent,
        in_degree=result.in_degree,
        out_degree=result.out_degree,
        balance=result.balance,
        tags=list_address_tags(currency, address)
        )
    return result


def get_id_group(id_):
    # if BUCKET_SIZE depends on the currency, we need session = ... here
    return floor(id_ / BUCKET_SIZE)


def get_address_id(currency, address):
    session = get_session(currency, 'transformed')
    query = "SELECT * FROM address WHERE address_prefix = %s " \
            "AND address = %s"
    result = session.execute(query, [address[:ADDRESS_PREFIX_LENGTH], address])
    if result:
        return result[0].address_id
    raise RuntimeError('address_id for {} in currency {} not found'
                       .format(address, currency))


def get_address_id_id_group(currency, address):
    address_id = get_address_id(currency, address)
    id_group = get_id_group(address_id)
    return address_id, id_group


def get_address_entity_id(currency, address):
    # from address to entity id only
    session = get_session(currency, 'transformed')
    address_id, address_id_group = get_address_id_id_group(currency, address)

    query = "SELECT cluster FROM address_cluster WHERE " \
            "address_id_group = %s AND address_id = %s "
    result = session.execute(query, [address_id_group, address_id])
    if result is None or result.one() is None:
        raise RuntimeError('cluster for address {} in currency {} not found'
                           .format(address, currency))
    return result.one().cluster
