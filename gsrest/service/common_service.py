import asyncio
from typing import Optional

import graphsenselib.utils.address
from graphsenselib.utils.address import address_to_user_format
from tagstore.db import TagstoreDbAsync

from gsrest.db.node_type import NodeType
from gsrest.errors import (
    AddressNotFoundException,
    BadUserInputException,
    NetworkNotFoundException,
)
from gsrest.service.rates_service import get_rates, list_rates
from gsrest.service.txs_service import tx_account_from_row
from gsrest.util import get_first_key_present, is_eth_like
from gsrest.util.values import (
    convert_token_values_map,
    convert_value,
    to_values,
    to_values_tokens,
)
from openapi_server.models.address import Address
from openapi_server.models.address_tx_utxo import AddressTxUtxo
from openapi_server.models.labeled_item_ref import LabeledItemRef
from openapi_server.models.link_utxo import LinkUtxo
from openapi_server.models.links import Links
from openapi_server.models.tx_summary import TxSummary


def get_request_cache(request):
    if not hasattr(request, "_cache"):
        request._cache = {}
    return request._cache


def cannonicalize_address(currency, address):
    try:
        return graphsenselib.utils.address.cannonicalize_address(currency, address)
    except ValueError:
        raise BadUserInputException(
            "The address provided does not look"
            f" like a {currency.upper()} address: {address}"
        )


async def try_get_cluster_id(db, network, address, cache=None) -> Optional[int]:
    key = f"cluster_id_{network}_{address}"
    if cache is not None and key in cache:
        return cache[key]

    try:
        network = network.lower()
        address_canonical = cannonicalize_address(network, address)
        returnv = await db.get_address_entity_id(network, address_canonical)
    except (AddressNotFoundException, NetworkNotFoundException, BadUserInputException):
        returnv = None

    if cache is not None:
        cache[key] = returnv

    return returnv


def get_user_tags_acl_group(request) -> str:
    return request.app["config"].get("user-tag-reporting-acl-group", "develop")


def get_tagstore_access_groups(request):
    return (
        ["public"]
        if not request.app["request_config"]["show_private_tags"]
        else ["public", "private"]
    ) + [get_user_tags_acl_group(request)]


def address_from_row(currency, row, rates, token_config, actors):
    return Address(
        currency=currency,
        address=address_to_user_format(currency, row["address"]),
        entity=row["cluster_id"],
        first_tx=TxSummary(
            row["first_tx"].height,
            row["first_tx"].timestamp,
            row["first_tx"].tx_hash.hex(),
        ),
        last_tx=TxSummary(
            row["last_tx"].height,
            row["last_tx"].timestamp,
            row["last_tx"].tx_hash.hex(),
        ),
        no_incoming_txs=row["no_incoming_txs"],
        no_outgoing_txs=row["no_outgoing_txs"],
        total_received=to_values(row["total_received"]),
        total_tokens_received=to_values_tokens(row.get("total_tokens_received", None)),
        total_spent=to_values(row["total_spent"]),
        total_tokens_spent=to_values_tokens(row.get("total_tokens_spent", None)),
        in_degree=row["in_degree"],
        out_degree=row["out_degree"],
        balance=convert_value(currency, row["balance"], rates),
        token_balances=convert_token_values_map(
            currency, row.get("token_balances", None), rates, token_config
        ),
        is_contract=row.get("is_contract", None),
        actors=actors if actors else None,
        status=row["status"],
    )


async def txs_from_rows(request, currency, rows, token_config):
    height_keys = ["height", "block_id"]
    heights = [get_first_key_present(row, height_keys) for row in rows]
    rates = await list_rates(request, currency, heights)
    if is_eth_like(currency):
        return [tx_account_from_row(currency, row, rates, token_config) for row in rows]

    return [
        AddressTxUtxo(
            currency=currency,
            height=row["height"],
            timestamp=row["timestamp"],
            coinbase=row["coinbase"],
            tx_hash=row["tx_hash"].hex(),
            value=convert_value(currency, row["value"], rates[row["height"]]),
        )
        for row in rows
    ]


async def get_address(request, currency, address, include_actors=True):
    address_canonical = cannonicalize_address(currency, address)

    if len(address_canonical) == 0:
        raise BadUserInputException(
            f"{address} does not look like a valid {currency} address"
        )

    db = request.app["db"]
    try:
        result = await db.get_address(currency, address_canonical)
    except AddressNotFoundException:
        result = await db.new_address(currency, address_canonical)

    actors = None
    if include_actors:
        tsdb = TagstoreDbAsync(request.app["gs-tagstore"])
        actor_res = await tsdb.get_actors_by_subjectid(
            address, get_tagstore_access_groups(request)
        )
        actors = [LabeledItemRef(id=a.id, label=a.label) for a in actor_res]

    return address_from_row(
        currency,
        result,
        (await get_rates(request, currency))["rates"],
        db.get_token_configuration(currency),
        actors,
    )


async def list_neighbors(
    request,
    currency,
    id,
    direction,
    node_type: NodeType,
    ids=None,
    include_labels=False,
    page=None,
    pagesize=None,
):
    is_outgoing = "out" in direction
    db = request.app["db"]
    results, paging_state = await db.list_neighbors(
        currency, id, is_outgoing, node_type, targets=ids, page=page, pagesize=pagesize
    )

    if results is not None:
        for row in results:
            row["labels"] = row["labels"] if "labels" in row else None
            row["value"] = to_values(row["value"])
            row["token_values"] = to_values_tokens(row.get("token_values", None))

    dst = "dst" if is_outgoing else "src"

    if results and include_labels:
        await add_labels(request, currency, node_type, dst, results)

    return results, paging_state


async def add_labels(request, currency, node_type: NodeType, that, nodes):
    tsdb = TagstoreDbAsync(request.app["gs-tagstore"])
    tsgroups = get_tagstore_access_groups(request)

    def identity(x, y):
        return y

    (field, tfield, fun, fmt) = (
        ("address", "address", "list_labels_for_addresses", address_to_user_format)
        if node_type == NodeType.ADDRESS
        else ("cluster_id", "gs_cluster_id", "list_labels_for_entities", identity)
    )
    thatfield = that + "_" + field
    ids = tuple((fmt(currency, node[thatfield]) for node in nodes))

    if node_type == NodeType.ADDRESS:
        tstasks = [tsdb.get_labels_by_subjectid(addr, tsgroups) for addr in ids]
    else:
        tstasks = [
            tsdb.get_labels_by_clusterid(cluster_id, tsgroups) for cluster_id in ids
        ]

    tsresults = {k: v for k, v in zip(ids, await asyncio.gather(*tstasks))}

    # print(ids)

    for node in nodes:
        nid = node[thatfield]
        node["labels"] = tsresults.get(nid, [])

    return nodes


async def links_response(request, currency, result):
    links, next_page = result
    if is_eth_like(currency):
        db = request.app["db"]
        token_config = db.get_token_configuration(currency)
        return Links(
            links=await txs_from_rows(request, currency, links, token_config),
            next_page=next_page,
        )

    heights = [row["block_id"] for row in links]
    rates = await list_rates(request, currency, heights)

    return Links(
        links=[
            LinkUtxo(
                tx_hash=e["tx_hash"].hex(),
                height=e["block_id"],
                currency=currency,
                timestamp=e["timestamp"],
                input_value=convert_value(
                    currency, e["input_value"], rates[e["block_id"]]
                ),
                output_value=convert_value(
                    currency, e["output_value"], rates[e["block_id"]]
                ),
            )
            for e in links
        ],
        next_page=next_page,
    )
