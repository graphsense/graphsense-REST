from openapi_server.models.values import Values
from openapi_server.models.rate import Rate


def make_values(value, eur, usd):
    return Values(
            value=value,
            fiat_values=[
                Rate('eur', round(eur, 2)),
                Rate('usd', round(usd, 2))]
            )


def catchNaN(v):
    if v != v:
        return None
    return v


def convert_value(currency, value, rates):
    if currency == 'eth':
        factor = 1e-18
    else:
        factor = 1e-8

    def make(v):
        return catchNaN()

    return Values(
            value=catchNaN(value),
            fiat_values=[
                Rate(r['code'], catchNaN(round(
                                         value * r['value'] * factor, 2)))
                for r in rates])


def to_values(value):
    return Values(value=catchNaN(value.value),
                  fiat_values=[Rate(r['code'], catchNaN(round(r['value'], 2)))
                               for r in value.fiat_values])
