from gsrest.model.blacklist import BlacklistToken


def test_blacklist_token():
    blacklist = BlacklistToken("some token")
    assert blacklist.token is not None
    assert blacklist.blacklisted_on is not None


def test_print_token():
    blacklist = BlacklistToken("some token")
    assert 'some token' in str(blacklist)
