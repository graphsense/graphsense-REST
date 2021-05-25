from gsrest.util.values import convert_value


def test_converted_value():
    rates = {'eur': 0.4, 'usd': 0.7}

    value = convert_value('btc', 175000000000, rates)

    assert value.value == 175000000000
    assert value.eur == 700
    assert value.usd == 1225

    value = convert_value('eth', 1750000000000000000000, rates)

    assert value.value == 1750000000000000000000
    assert value.eur == 700
    assert value.usd == 1225
