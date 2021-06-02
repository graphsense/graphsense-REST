import openapi_server.models.values as v


def make_values(value, eur, usd):
    return v.Values(
            value=value,
            eur=round(eur, 2),
            usd=round(usd, 2)
            )


def compute_balance(total_received_value, total_spent_value):
    return total_received_value - total_spent_value


def convert_value(currency, value, rates):
    if currency == 'eth':
        factor = 1e-18
    else:
        factor = 1e-8

    values = v.Values(
            value=value,
            eur=round(value * rates['eur'] * factor, 2),
            usd=round(value * rates['usd'] * factor, 2))
    return values
