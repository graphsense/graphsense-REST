import openapi_server.models.values as v


def make_values(value, eur, usd):
    return v.Values(
            value=value,
            eur=round(eur, 2),
            usd=round(usd, 2)
            )


def compute_balance(total_received_value, total_spent_value):
    return total_received_value - total_spent_value


def convert_value(value, rates):
    values = v.Values(
            value=value,
            eur=round(value * rates['eur'] * 1e-8, 2),
            usd=round(value * rates['usd'] * 1e-8, 2))
    return values
