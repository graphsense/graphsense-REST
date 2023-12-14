from gsrest.util.string_edit import remove_prefix


def eth_address_to_hex(address):
    if not isinstance(address, bytes):
        return address
    return '0x' + bytes_to_hex(address)


def is_hex_string(string: str) -> bool:
    return string is not None and string.startswith("0x") and len(string) >= 2


def bytes_to_hex(b: bytes) -> str:
    return b.hex()


def hex_str_to_bytes(hex_str: str) -> bytes:
    return bytes.fromhex(hex_str)


def strip_0x(string: str) -> str:
    return remove_prefix(string, "0x") if is_hex_string(string) else string
