from openapi_server.models.address import Address
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.neighbor import Neighbor
from gsrest.util.values import compute_balance, convert_value, to_values
from gsrest.service.rates_service import get_rates
from openapi_server.models.link_utxo import LinkUtxo
from openapi_server.models.links import Links
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.address_tx_utxo import AddressTxUtxo
from gsrest.service.rates_service import list_rates


def address_from_row(currency, row, rates, tags=None):
    return Address(
        address=row['address'],
        entity=row['cluster_id'],
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
        total_received=to_values(row['total_received']),
        total_spent=to_values(row['total_spent']),
        in_degree=row['in_degree'],
        out_degree=row['out_degree'],
        balance=convert_value(
                currency,
                compute_balance(
                    row['total_received'].value,
                    row['total_spent'].value,
                ),
                rates),
        tags=tags
        )


async def txs_from_rows(request, currency, rows):
    heights = [row['height'] for row in rows]
    rates = await list_rates(request, currency, heights)
    if currency == 'eth':
        return [TxAccount(
                height=row['height'],
                timestamp=row['timestamp'],
                tx_hash=row['tx_hash'].hex(),
                from_address=row['from_address'],
                to_address=row['to_address'],
                value=convert_value(currency, row['value'],
                                    rates[row['height']]))
                for row in rows]
    return [AddressTxUtxo(
            height=row['height'],
            timestamp=row['timestamp'],
            coinbase=row['coinbase'],
            tx_hash=row['tx_hash'].hex(),
            value=convert_value(currency, row['value'], rates[row['height']]))
            for row in rows]


async def get_address(request, currency, address, include_tags=False):
    db = request.app['db']
    result = await db.get_address(currency, address)

    tags = None
    if include_tags:
        tags = await list_tags_by_address(request, currency, address)

    if not result:
        raise RuntimeError("Address {} not found in currency {}".format(
            address, currency))
    return address_from_row(currency, result,
                            (await get_rates(request, currency)
                             )['rates'], tags)


async def list_tags_by_address(request, currency, address):
    db = request.app['db']
    results = await db.list_tags_by_address(currency, address)

    if results is None:
        return []
    address_tags = [AddressTag(
                    label=row['label'],
                    address=row['address'],
                    category=row['category'],
                    abuse=row['abuse'],
                    tagpack_uri=row['tagpack_uri'],
                    source=row['source'],
                    lastmod=row['lastmod'],
                    active=True,
                    currency=currency
                    )
                    for row in results]

    return address_tags


async def list_neighbors(request, currency, id, direction, node_type, ids=None,
                         include_labels=False, page=None, pagesize=None):
    if node_type not in ['address', 'entity']:
        raise RuntimeError(f'Unknown node type {node_type}')
    is_outgoing = "out" in direction
    db = request.app['db']
    results, paging_state = await db.list_neighbors(
                                    currency,
                                    id,
                                    is_outgoing,
                                    node_type,
                                    targets=ids,
                                    include_labels=include_labels,
                                    page=page,
                                    pagesize=pagesize)
    dst = 'dst' if is_outgoing else 'src'
    rates = (await get_rates(request, currency))['rates']
    relations = []
    if results is None:
        return Neighbors()
    ntype, suffix = (node_type, '') \
        if node_type == 'address' else ('cluster', '_id')
    for row in results:
        relations.append(Neighbor(
            id=str(row[f'{dst}_{ntype}{suffix}']),
            node_type=node_type,
            labels=row['labels'] if 'labels' in row else None,
            received=to_values(row['total_received']),
            value=to_values(row['value']),
            balance=convert_value(
                currency,
                compute_balance(
                    row['total_received'].value,
                    row['total_spent'].value,
                ),
                rates),
            no_txs=row['no_transactions']))
    return Neighbors(next_page=paging_state,
                     neighbors=relations)


async def links_response(request, currency, result):
    links, next_page = result
    if currency == 'eth':
        heights = [row['block_id'] for row in links]
        rates = await list_rates(request, currency, heights)
        return Links(links=[TxAccount(
                            tx_hash=row['tx_hash'].hex(),
                            timestamp=row['block_timestamp'],
                            height=row['block_id'],
                            from_address=row['from_address'],
                            to_address=row['to_address'],
                            value=convert_value(currency,
                                                row['value'],
                                                rates[row['block_id']]))
                            for row in links],
                     next_page=next_page)

    heights = [row['height'] for row in links]
    rates = await list_rates(request, currency, heights)

    return Links(links=[LinkUtxo(tx_hash=e['tx_hash'].hex(),
                        height=e['height'],
                        timestamp=e['timestamp'],
                        input_value=convert_value(
                            currency, e['input_value'], rates[e['height']]),
                        output_value=convert_value(
                            currency, e['output_value'], rates[e['height']]),
                        ) for e in links],
                 next_page=next_page)
