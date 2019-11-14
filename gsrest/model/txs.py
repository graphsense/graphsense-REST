from gsrest.model.blocks import Value

# TODO: add exchange rates


def byte_to_hex(buffer):
    return "".join(("%02x" % a) for a in buffer)


class Tx(object):
    """ Model representing a transaction """

    def __init__(self, txHash, coinbase, height, inputs, outputs, timestamp,
                 totalInput, totalOutput):
        self.txHash = byte_to_hex(txHash)
        self.coinbase = coinbase
        self.height = height
        if inputs:
            self.inputs = [TxInputOutput(i.address,
                                         Value(i.value, 0, 0)
                                         .to_dict()).to_dict()
                           for i in inputs]
        else:
            self.inputs = []
        self.outputs = [TxInputOutput(output.address,
                                      Value(output.value, 0, 0)
                                      .to_dict()).to_dict()
                        for output in outputs if output.address]
        self.timestamp = timestamp
        self.totalInput = Value(totalInput,
                                0,
                                0).to_dict()
        self.totalOutput = Value(totalOutput,
                                 0,
                                 0).to_dict()

    @staticmethod
    def from_row(row):
        return Tx(row.tx_hash, row.coinbase, row.height, row.inputs,
                  row.outputs, row.timestamp, row.total_input,
                  row.total_output)

    def to_dict(self):
        return self.__dict__


class TxInputOutput(object):
    def __init__(self, address, value):
        self.address = address[0]
        self.value = value

    def to_dict(self):
        return self.__dict__
