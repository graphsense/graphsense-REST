from gsrest.db.cassandra import get_session
from openapi_server.models.address import Address
from openapi_server.models.values import Values
from openapi_server.models.tx_summary import TxSummary
from gsrest.model.tags import Tag
from gsrest.model.common import compute_balance
from gsrest.service.rates_service import get_rates
from gsrest.service.problems import notfound

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
    result = session.execute(
        query, [address[:ADDRESS_PREFIX_LENGTH], address]).one()
    if not result:
        return notfound("Address {} not found in currency {}".format(
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
        total_received=Values(
            result.total_received.eur,
            result.total_received.usd,
            result.total_received.value),
        total_spent=Values(
            result.total_spent.eur,
            result.total_spent.usd,
            result.total_spent.value),
        in_degree=result.in_degree,
        out_degree=result.out_degree,
        balance=compute_balance(
            result.total_received.value,
            result.total_spent.value,
            get_rates(currency)['rates'])
        )


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
