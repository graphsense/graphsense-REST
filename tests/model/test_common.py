from gsrest.model.common import Values, ConvertedValues


def test_normal_value():
    value = Values(value=0.1, usd=2, eur=4)

    value_dict = value.to_dict()

    assert len(value_dict) == 3

    assert value_dict['value'] == 0.1
    assert value_dict['usd'] == 2
    assert value_dict['eur'] == 4


def test_converted_value():
    exchange_rates = {'eur': 0.4, 'usd': 0.7}

    value = ConvertedValues(175000000000, exchange_rates)

    value_dict = value.to_dict()

    assert len(value_dict) == 3

    assert value_dict['value'] == 175000000000
    assert value_dict['eur'] == 700
    assert value_dict['usd'] == 1225
