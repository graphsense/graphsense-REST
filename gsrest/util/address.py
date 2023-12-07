from gsrest.util.tron import tron_address_to_evm_string, evm_to_tron_address_string, partial_tron_to_partial_evm
from gsrest.util.bch import try_bch_address_to_legacy
from gsrest.util.evm import eth_address_to_hex, is_hex_string


def cannonicalize_address(currency, address, partial=False) -> str:
    try:
        if currency == "trx":
            if partial:
                return partial_tron_to_partial_evm(address)
            else:
                return tron_address_to_evm_string(address, validate=False)
        elif currency == "bch":
            return try_bch_address_to_legacy(address)
        elif isinstance(address, str):
            return address
        else:
            raise Exception(
                f"Don't know how to encode address, {address} {currency}")
    except ValueError:
        return address


def address_to_user_format(currency, db_address) -> str:
    if currency == "eth":
        if isinstance(db_address, bytes):
            return eth_address_to_hex(db_address)
        else:
            return db_address
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
        raise Exception(
            f"Don't know how to decode db address, {db_address} {currency}")
