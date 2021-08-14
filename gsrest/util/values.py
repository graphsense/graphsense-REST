from openapi_server.models.values import Values
from openapi_server.models.rate import Rate


def make_values(value, eur, usd):
    return Values(
            value=value,
            fiat_values=[
                Rate('eur', round(eur, 2)),
                Rate('usd', round(usd, 2))]
            )


def compute_balance(total_received_value, total_spent_value):
    return total_received_value - total_spent_value


def convert_value(currency, value, rates):
    if currency == 'eth':
        factor = 1e-18
    else:
        factor = 1e-8

    return Values(
            value=value,
            fiat_values=[
                Rate(r['code'], round(value * r['value'] * factor, 2))
                for r in rates])


def to_values(value):
    return Values(value=value.value,
                  fiat_values=[Rate(r['code'], round(r['value'], 2))
                               for r in value.fiat_values])
