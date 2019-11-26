class Values(object):
    """ Model representing values in different crypto- and fiat-currencies."""

    def __init__(self, **values):
        self.values = {k: round(v, 2) for k, v in values.items()}

    def to_dict(self):
        return self.values


class ConvertedValues(Values):
    """ Model representing a crypto value and converted fiat values """

    def __init__(self, value, exchange_rates):
        super(Values, self).__init__()
        self.values = self._convert_values(value, exchange_rates)

    def _convert_values(self, value, exchange_rates):
        values = dict()
        values['value'] = value
        for currency, rate in exchange_rates.items():
            values[currency] = round(value * rate * 1e-8, 2)
        return values


def compute_balance(total_received_value, total_spent_value, exchange_rates):
    balance_value = total_received_value - total_spent_value
    balance = ConvertedValues(balance_value, exchange_rates).to_dict()
    return balance
