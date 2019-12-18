class ExchangeRate(object):
    """ Model representing exchange rate for a given height """

    def __init__(self, height, rates):
        self.height = height
        self.rates = rates

    def to_dict(self):
        return {'height': self.height, 'rates': self.rates}
