import asyncio

import aiohttp
from async_lru import alru_cache
from graphsenselib.utils.accountmodel import eth_address_to_hex, strip_0x


def create_token_request(contract_address: str, account: str, block: str = "latest"):
    return {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [
            {
                "to": contract_address,
                "data": f"0x70a08231000000000000000000000000{strip_0x(account)}",
            },
            block,
        ],
        "id": 1,
    }


def create_base_request(account: str, block: str = "latest"):
    return {
        "method": "eth_getBalance",
        "params": [account, block],
        "id": 1,
        "jsonrpc": "2.0",
    }


async def send_node_request(node_url: str, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(node_url, json=payload) as resp:
            return await resp.json()


@alru_cache(maxsize=1000)
async def get_token_balance(
    node_url: str, contract_address: str, account: str, block: str = "latest"
):
    resp = await send_node_request(
        node_url, payload=create_token_request(contract_address, account, block)
    )

    return int(resp["result"], 16)


@alru_cache(maxsize=1000)
async def get_base_balance(node_url: str, account: str, block: str = "latest"):
    resp = await send_node_request(
        node_url, payload=create_base_request(account, block)
    )

    return int(resp["result"], 16)


async def get_balances(
    node_url: str, network: str, account: str, tokenConfigs, block: str = "latest"
):
    bb = get_base_balance(node_url, eth_address_to_hex(account), block)

    tbs = [
        get_token_balance(
            node_url,
            eth_address_to_hex(tk["token_address"]),
            eth_address_to_hex(account),
            block,
        )
        for k, tk in tokenConfigs.items()
    ]

    balances = await asyncio.gather(bb, *tbs)

    return {
        k.upper(): {"balance": v}
        for k, v in zip([network, *tokenConfigs.keys()], balances)
    }
