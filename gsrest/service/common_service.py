from gsrest.db import get_connection
from openapi_server.models.address import Address
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
from gsrest.util.values import compute_balance, convert_value, make_values
from gsrest.service.rates_service import get_rates


def address_from_row(row, rates, tags=None):
    return Address(
        address=row['address'],
        first_tx=TxSummary(
            row['first_tx'].height,
            row['first_tx'].timestamp,
            row['first_tx'].tx_hash.hex()),
        last_tx=TxSummary(
            row['last_tx'].height,
            row['last_tx'].timestamp,
            row['last_tx'].tx_hash.hex()),
        no_incoming_txs=row['no_incoming_txs'],
        no_outgoing_txs=row['no_outgoing_txs'],
        total_received=make_values(
            value=row['total_received'].value,
            eur=row['total_received'].eur,
            usd=row['total_received'].usd),
        total_spent=make_values(
            eur=row['total_spent'].eur,
            usd=row['total_spent'].usd,
            value=row['total_spent'].value),
        in_degree=row['in_degree'],
        out_degree=row['out_degree'],
        balance=convert_value(
                compute_balance(
                    row['total_received'].value,
                    row['total_spent'].value,
                ),
                rates),
        tags=tags
        )


def get_address(currency, address, include_tags=False):
    db = get_connection()
    result = db.get_address(currency, address)

    tags = None
    if include_tags:
        tags = list_tags_by_address(currency, address)

    if not result:
        raise RuntimeError("Address {} not found in currency {}".format(
            address, currency))
    return address_from_row(result, get_rates(currency)['rates'], tags)


def list_tags_by_address(currency, address):
    db = get_connection()
    results = db.list_tags_by_address(currency, address)

    if results is None:
        return []
    address_tags = [AddressTag(
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
                    for row in results]

    return address_tags


def get_address_entity_id(currency, address):
    db = get_connection()
    result = db.get_address_entity_id(currency, address)

    # from address to entity id only
    if result is None:
        raise RuntimeError('cluster for address {} in currency {} not found'
                           .format(address, currency))
    return result.cluster


def list_neighbors(currency, id, direction, node_type,
                   ids=None, page=None, pagesize=None):
    if node_type not in ['address', 'entity']:
        raise RuntimeError(f'Unknown node type {node_type}')
    is_outgoing = "out" in direction
    db = get_connection()
    results, paging_state = db.list_neighbors(
                                    currency,
                                    id,
                                    is_outgoing,
                                    node_type,
                                    targets=ids,
                                    page=page,
                                    pagesize=pagesize)
    dst = 'dst' if is_outgoing else 'src'
    rates = get_rates(currency)['rates']
    relations = []
    if results is None:
        return Neighbors()
    ntype = node_type if node_type == 'address' else 'cluster'
    for row in results:
        balance = compute_balance(row[dst+'_properties'].total_received.value,
                                  row[dst+'_properties'].total_spent.value)
        relations.append(Neighbor(
            id=row[f'{dst}_{ntype}'],
            node_type=node_type,
            has_labels=row[f'has_{dst}_labels']
            if row[f'has_{dst}_labels'] is not None else False,
            received=make_values(
                value=row[dst+'_properties'].total_received.value,
                eur=row[dst+'_properties'].total_received.eur,
                usd=row[dst+'_properties'].total_received.usd),
            estimated_value=make_values(
                value=row['estimated_value'].value,
                eur=row['estimated_value'].eur,
                usd=row['estimated_value'].usd),
            balance=convert_value(balance, rates),
            no_txs=row['no_transactions']))
    return Neighbors(next_page=paging_state,
                     neighbors=relations)
