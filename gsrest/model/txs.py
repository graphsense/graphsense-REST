from gsrest.model.common import ConvertedValue


class Tx(object):
    """ Model representing a transaction """

    def __init__(self, txHash, coinbase, height, inputs, outputs, timestamp,
                 totalInput, totalOutput, rates):
        self.txHash = txHash.hex()
        self.coinbase = coinbase
        self.height = height
        if inputs:
            self.inputs = [TxInputOutput(i.address,
                                         ConvertedValue(i.value, rates)
                                         .to_dict()).to_dict()
                           for i in inputs]
        else:
            self.inputs = []
        self.outputs = [TxInputOutput(output.address,
                                      ConvertedValue(output.value, rates)
                                      .to_dict()).to_dict()
                        for output in outputs if output.address]
        self.timestamp = timestamp
        self.totalInput = ConvertedValue(totalInput, rates).to_dict()
        self.totalOutput = ConvertedValue(totalOutput, rates).to_dict()

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
    def __init__(self, height, timestamp, txHash):
        self.height = height
        self.timestamp = timestamp
        self.txHash = txHash
