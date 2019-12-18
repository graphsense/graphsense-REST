from gsrest.model.common import ConvertedValues


class Tx(object):
    """ Model representing a transaction """

    def __init__(self, tx_hash, coinbase, height, inputs, outputs, timestamp,
                 total_input, total_output, exchange_rates):
        self.tx_hash = tx_hash.hex()
        self.coinbase = coinbase
        self.height = height
        if inputs:
            self.inputs = [TxInputOutput(i.address,
                                         ConvertedValues(i.value,
                                                         exchange_rates)
                                         .to_dict()).to_dict()
                           for i in inputs]
        else:
            self.inputs = []
        self.outputs = [TxInputOutput(output.address,
                                      ConvertedValues(output.value,
                                                      exchange_rates)
                                      .to_dict()).to_dict()
                        for output in outputs if output.address]
        self.timestamp = timestamp
        self.total_input = ConvertedValues(total_input,
                                           exchange_rates).to_dict()
        self.total_output = ConvertedValues(total_output,
                                            exchange_rates).to_dict()

    @staticmethod
    def from_row(row, rates):
        return Tx(row.tx_hash, row.coinbase, row.height, row.inputs,
                  row.outputs, row.timestamp, row.total_input,
                  row.total_output, rates)

    def to_dict(self):
        return self.__dict__


class TxInputOutput(object):
    def __init__(self, address, value):
        self.address = address[0]
        self.value = value

    def to_dict(self):
        return self.__dict__


class TxSummary(object):
    def __init__(self, height, timestamp, tx_hash):
        self.height = height
        self.timestamp = timestamp
        self.tx_hash = tx_hash

    def to_dict(self):
        return self.__dict__
