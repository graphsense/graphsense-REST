class Value(object):
    """ Model representing values in different crypto- and fiat-currencies."""

    def __init__(self, **values):
        self.values = values

    def to_dict(self):
        return self.values


class ConvertedValue(Value):
    """ Model representing a crypto value and converted fiat values """

    def __init__(self, value, exchange_rates):
        super(Value, self).__init__()
        self.values = self._convert_values(value, exchange_rates)

    def _convert_values(self, value, exchange_rates):
        values = dict()
        values['value'] = value
        for currency, rate in exchange_rates.items():
            values[currency] = round(value * rate * 1e-8)
        return values
