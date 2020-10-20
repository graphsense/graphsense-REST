import openapi_server.models.values as v


class Values:
    """ Model representing values in different crypto- and fiat-currencies."""

    def __init__(self, **values):
        self.values = {k: round(v, 2) for k, v in values.items()}

    def to_dict(self):
        return self.values


class ConvertedValues(Values):
    """ Model representing a crypto value and converted fiat values """

    def __init__(self, value, rates):
        Values.__init__(self)
        self.values = self._convert_values(value, rates)

    def _convert_values(self, value, rates):
        values = dict()
        values['value'] = value
        for currency, rate in rates.items():
            values[currency] = round(value * rate * 1e-8, 2)
        return values


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
