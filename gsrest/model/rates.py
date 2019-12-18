class ExchangeRate(object):
    """ Model representing exchange rate for a given height """

    def __init__(self, height, exchange_rates):
        self.height = height
        self.exchange_rates = exchange_rates

    def to_dict(self):
        return {'height': self.height, 'rates': self.exchange_rates}
