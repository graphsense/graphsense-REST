from openapi_server.models.address import Address
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.address_tags import AddressTags
from gsrest.util.values import convert_value, to_values
from gsrest.service.rates_service import get_rates
from openapi_server.models.link_utxo import LinkUtxo
from openapi_server.models.links import Links
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.address_tx_utxo import AddressTxUtxo
from gsrest.service.rates_service import list_rates
from gsrest.db.util import tagstores, tagstores_with_paging
from gsrest.service.tags_service import address_tag_from_row


def address_from_row(currency, row, rates):
    return Address(
        currency=currency,
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
        balance=convert_value(currency, row['balance'], rates)
        )


async def txs_from_rows(request, currency, rows):
    heights = [row['height'] for row in rows]
    rates = await list_rates(request, currency, heights)
    if currency == 'eth':
        return [TxAccount(
                currency=currency,
                height=row['height'],
                timestamp=row['timestamp'],
                tx_hash=row['tx_hash'].hex(),
                from_address=row['from_address'],
                to_address=row['to_address'],
                value=convert_value(currency, row['value'],
                                    rates[row['height']]))
                for row in rows]
    return [AddressTxUtxo(
            currency=currency,
            height=row['height'],
            timestamp=row['timestamp'],
            coinbase=row['coinbase'],
            tx_hash=row['tx_hash'].hex(),
            value=convert_value(currency, row['value'], rates[row['height']]))
            for row in rows]


async def get_address(request, currency, address):
    db = request.app['db']
    result = await db.get_address(currency, address)

    if not result:
        raise RuntimeError("Address {} not found in currency {}".format(
            address, currency))
    return address_from_row(currency, result,
                            (await get_rates(request, currency)
                             )['rates'])


async def list_tags_by_address(request, currency, address,
                               page=None, pagesize=None):
    address_tags, next_page = \
        await tagstores_with_paging(
            request.app['tagstores'],
            address_tag_from_row,
            'list_tags_by_address',
            page, pagesize, currency, address,
            request.app['show_private_tags'])

    return AddressTags(address_tags=address_tags, next_page=next_page)


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
                                    page=page,
                                    pagesize=pagesize)

    for row in results:
        row['labels'] = row['labels'] if 'labels' in row else None
        row['value'] = to_values(row['value'])

    dst = 'dst' if is_outgoing else 'src'

    print(f'result {results}')

    if include_labels:
        await add_labels(request, currency, node_type, dst, results)

    return results, paging_state


async def add_labels(request, currency, node_type, that, nodes):
    (field, tfield, fun) = \
        ('address', 'address', 'list_labels_for_addresses') \
        if node_type == 'address' else \
        ('cluster_id', 'gs_cluster_id', 'list_labels_for_entities')
    thatfield = that + '_' + field
    ids = tuple((node[thatfield] for node in nodes))

    result = await tagstores(request.app['tagstores'],
                             lambda row: row, fun, currency, ids,
                             request.app['show_private_tags'])
    iterator = iter(result)
    if node_type == 'address':
        nodes = sorted(nodes, key=lambda node: node[thatfield])
    for node in nodes:
        try:
            row = next(iterator)
            if node[thatfield] != row[tfield]:
                node['labels'] = []
                continue
            node['labels'] = row['labels']
        except StopIteration:
            node['labels'] = []

    return nodes


async def links_response(request, currency, result):
    links, next_page = result
    if currency == 'eth':
        heights = [row['block_id'] for row in links]
        rates = await list_rates(request, currency, heights)
        return Links(links=[TxAccount(
                            tx_hash=row['tx_hash'].hex(),
                            currency=currency,
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
                        currency=currency,
                        timestamp=e['timestamp'],
                        input_value=convert_value(
                            currency, e['input_value'], rates[e['height']]),
                        output_value=convert_value(
                            currency, e['output_value'], rates[e['height']]),
                        ) for e in links],
                 next_page=next_page)
