from gsrest.util.bch import try_bch_address_to_legacy
from gsrest.util.evm import (
    eth_address_to_hex,
    hex_str_to_bytes,
    is_hex_string,
    strip_0x,
)
from gsrest.util.tron import evm_to_tron_address_string, tron_address_to_evm


def cannonicalize_address(currency, address: str):
    if currency == "trx":
        return tron_address_to_evm(address, validate=False)
    elif currency == "bch":
        return try_bch_address_to_legacy(address)
    elif currency == "eth":
        return hex_str_to_bytes(strip_0x(address))
    elif isinstance(address, str):
        return address
    else:
        raise ValueError()


def address_to_user_format(currency, db_address) -> str:
    if currency == "eth":
        if isinstance(db_address, bytes):
            return eth_address_to_hex(db_address)
        else:
            return db_address.lower()
    elif currency == "trx":
        if isinstance(db_address, bytes):
            return evm_to_tron_address_string(eth_address_to_hex(db_address))
        else:
            if is_hex_string(db_address):
                return evm_to_tron_address_string(db_address)
            else:
                return db_address
    elif isinstance(db_address, str):
        return db_address
    else:
        raise Exception(f"Don't know how to decode db address, {db_address} {currency}")
