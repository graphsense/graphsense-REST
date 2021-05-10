from gsrest.db import get_connection
from openapi_server.models.address import Address
from openapi_server.models.address_with_tags import AddressWithTags
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
from gsrest.util.values import compute_balance, convert_value, make_values
from gsrest.service.rates_service import get_rates


def get_address(currency, address):
    db = get_connection()
    result = db.get_address(currency, address)

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
        tags=list_tags_by_address(currency, address)
        )
    return result


def get_address_entity_id(currency, address):
    db = get_connection()
    result = db.get_address_entity_id(currency, address)

    # from address to entity id only
    if result is None:
        raise RuntimeError('cluster for address {} in currency {} not found'
                           .format(address, currency))
    return result.cluster


def list_neighbors(currency, id, direction, node_type,
                   targets=None, page=None, pagesize=None):
    if node_type not in ['address', 'entity']:
        raise RuntimeError(f'Unknown node type {node_type}')
    is_outgoing = "out" in direction
    db = get_connection()
    results, paging_state = db.list_neighbors(
                                    currency,
                                    id,
                                    is_outgoing,
                                    node_type,
                                    targets=targets,
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
