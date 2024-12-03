import pytest

from gsrest.util.address import address_to_user_format, cannonicalize_address


def test_address_conversions():
    addr = "TAzsQ9Gx8eqFNFSKbeXrbi45CuVPHzA8wr"

    assert (
        cannonicalize_address("trx", addr).hex()
        == "0b48984414cc0c6a8e599fb6e3bc11e599de2e24"
    )

    assert address_to_user_format("trx", cannonicalize_address("trx", addr)) == addr

    assert address_to_user_format("trx", addr) == addr

    eaddr = "0x0b48984414cc0c6a8e599fb6e3bc11e599de2e24"

    assert address_to_user_format("eth", cannonicalize_address("eth", eaddr)) == eaddr

    assert (
        cannonicalize_address("eth", eaddr).hex()
        == "0b48984414cc0c6a8e599fb6e3bc11e599de2e24"
    )

    with pytest.raises(ValueError):
        cannonicalize_address("eth", addr).hex()
