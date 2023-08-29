from openapi_server.models.address import Address
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.address_tags import AddressTags
from gsrest.util.values import (convert_value, convert_token_values_map,
                                to_values, to_values_tokens,
                                convert_token_value)
from gsrest.service.rates_service import get_rates
from openapi_server.models.link_utxo import LinkUtxo
from openapi_server.models.links import Links
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.address_tx_utxo import AddressTxUtxo
from openapi_server.models.labeled_item_ref import LabeledItemRef
from gsrest.service.rates_service import list_rates
from gsrest.db.util import tagstores, tagstores_with_paging
from gsrest.service.tags_service import address_tag_from_row
from gsrest.util import get_first_key_present
from psycopg2.errors import InvalidTextRepresentation


def address_from_row(currency, row, rates, token_config, actors):
    return Address(
        currency=currency,
        address=row['address'],
        entity=row['cluster_id'],
        first_tx=TxSummary(row['first_tx'].height, row['first_tx'].timestamp,
                           row['first_tx'].tx_hash.hex()),
        last_tx=TxSummary(row['last_tx'].height, row['last_tx'].timestamp,
                          row['last_tx'].tx_hash.hex()),
        no_incoming_txs=row['no_incoming_txs'],
        no_outgoing_txs=row['no_outgoing_txs'],
        total_received=to_values(row['total_received']),
        total_tokens_received=to_values_tokens(
            row.get("total_tokens_received", None)),
        total_spent=to_values(row['total_spent']),
        total_tokens_spent=to_values_tokens(row.get("total_tokens_spent",
                                                    None)),
        in_degree=row['in_degree'],
        out_degree=row['out_degree'],
        balance=convert_value(currency, row['balance'], rates),
        token_balances=convert_token_values_map(
            currency, row.get('token_balances', None), rates, token_config),
        is_contract=row.get("is_contract", None),
        actors=actors if actors else None,
        status=row['status'])


async def txs_from_rows(request, currency, rows, token_config):
    height_keys = ["height", "block_id"]
    timestamp_keys = ["timestamp", "block_timestamp"]
    heights = [get_first_key_present(row, height_keys) for row in rows]
    rates = await list_rates(request, currency, heights)
    if currency == 'eth':
        return [
            TxAccount(
                currency=currency
                if "token_tx_id" not in row else row["currency"].lower(),
                tx_hash=row['tx_hash'].hex(),
                timestamp=get_first_key_present(row, timestamp_keys),
                height=get_first_key_present(row, height_keys),
                from_address=row['from_address'],
                to_address=row['to_address'],
                token_tx_id=row.get("token_tx_id", None),
                contract_creation=row.get("contract_creation", None),
                value=convert_value(
                    currency, row['value'], rates[get_first_key_present(
                        row, height_keys)])
                if "token_tx_id" not in row else convert_token_value(
                    row['value'], rates[get_first_key_present(
                        row, height_keys)], token_config[row["currency"]]))
            for row in rows
        ]

    return [
        AddressTxUtxo(currency=currency,
                      height=row['height'],
                      timestamp=row['timestamp'],
                      coinbase=row['coinbase'],
                      tx_hash=row['tx_hash'].hex(),
                      value=convert_value(currency, row['value'],
                                          rates[row['height']]))
        for row in rows
    ]


async def get_address(request, currency, address):
    db = request.app['db']
    result = await db.get_address(currency, address)

    if not result:
        raise RuntimeError("Address {} not found in currency {}".format(
            address, currency))

    actors = tagstores(
        request.app['tagstores'],
        lambda row: LabeledItemRef(id=row["id"], label=row["label"]),
        'list_actors_address', currency, address,
        request.app['request_config']['show_private_tags'])

    return address_from_row(currency, result,
                            (await get_rates(request, currency))['rates'],
                            db.get_token_configuration(currency), await actors)


async def list_tags_by_address(request,
                               currency,
                               address,
                               page=None,
                               pagesize=None):

    try:
        address_tags, next_page = \
            await tagstores_with_paging(
                request.app['tagstores'],
                address_tag_from_row,
                'list_tags_by_address',
                page, pagesize, currency, address,
                request.app['request_config']['show_private_tags'])
    except InvalidTextRepresentation as e:
        if currency.upper() in str(e):
            raise ValueError(f"Currency {currency} currently not supported")
        else:
            raise e

    return AddressTags(address_tags=address_tags, next_page=next_page)


async def list_neighbors(request,
                         currency,
                         id,
                         direction,
                         node_type,
                         ids=None,
                         include_labels=False,
                         page=None,
                         pagesize=None):
    if node_type not in ['address', 'entity']:
        raise RuntimeError(f'Unknown node type {node_type}')
    is_outgoing = "out" in direction
    db = request.app['db']
    results, paging_state = await db.list_neighbors(currency,
                                                    id,
                                                    is_outgoing,
                                                    node_type,
                                                    targets=ids,
                                                    page=page,
                                                    pagesize=pagesize)

    if results is not None:
        for row in results:
            row['labels'] = row['labels'] if 'labels' in row else None
            row['value'] = to_values(row['value'])
            row["token_values"] = to_values_tokens(
                row.get("token_values", None))

    dst = 'dst' if is_outgoing else 'src'

    if results and include_labels:
        await add_labels(request, currency, node_type, dst, results)

    return results, paging_state


async def add_labels(request, currency, node_type, that, nodes):
    (field, tfield, fun) = \
        ('address', 'address', 'list_labels_for_addresses') \
        if node_type == 'address' else \
        ('cluster_id', 'gs_cluster_id', 'list_labels_for_entities')
    thatfield = that + '_' + field
    ids = tuple((node[thatfield] for node in nodes))

    result = await tagstores(
        request.app['tagstores'], lambda row: row, fun, currency, ids,
        request.app['request_config']['show_private_tags'])
    iterator = iter(result)
    if node_type == 'address':
        nodes = sorted(nodes, key=lambda node: node[thatfield])

    stop_iteration = False
    try:
        row = next(iterator)
    except StopIteration:
        stop_iteration = True
    for node in nodes:
        if stop_iteration or node[thatfield] != row[tfield]:
            node['labels'] = []
            continue
        node['labels'] = row['labels']
        try:
            row = next(iterator)
        except StopIteration:
            stop_iteration = True

    return nodes


async def links_response(request, currency, result):

    links, next_page = result
    if currency == 'eth':
        db = request.app['db']
        token_config = db.get_token_configuration(currency)
        heights = [row['block_id'] for row in links]
        rates = await list_rates(request, currency, heights)
        return Links(links=[
            TxAccount(tx_hash=row['tx_hash'].hex(),
                      currency=currency
                      if "token_tx_id" not in row else row["currency"].lower(),
                      timestamp=row['block_timestamp'],
                      height=row['block_id'],
                      token_tx_id=row.get("token_tx_id", None),
                      from_address=row['from_address'],
                      to_address=row['to_address'],
                      contract_creation=row.get("contract_creation", None),
                      value=convert_value(currency, row['value'],
                                          rates[row['block_id']])
                      if "token_tx_id" not in row else convert_token_value(
                          row['value'], rates[row['block_id']],
                          token_config[row["currency"]])) for row in links
        ],
                     next_page=next_page)

    heights = [row['height'] for row in links]
    rates = await list_rates(request, currency, heights)

    return Links(links=[
        LinkUtxo(
            tx_hash=e['tx_hash'].hex(),
            height=e['height'],
            currency=currency,
            timestamp=e['timestamp'],
            input_value=convert_value(currency, e['input_value'],
                                      rates[e['height']]),
            output_value=convert_value(currency, e['output_value'],
                                       rates[e['height']]),
        ) for e in links
    ],
                 next_page=next_page)
