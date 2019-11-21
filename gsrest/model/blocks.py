from gsrest.model.common import ConvertedValue


class Block(object):
    """ Model representing block header fields and summary statistics """

    def __init__(self, height, blockHash, noTxs, timestamp):
        self.height = height
        self.blockHash = blockHash
        self.noTxs = noTxs
        self.timestamp = timestamp

    @staticmethod
    def from_row(row):
        return Block(row.height, row.block_hash.hex(),
                     row.no_transactions, row.timestamp)

    def to_dict(self):
        return self.__dict__


class BlockTxSummary(object):
    """ Model representing block transaction summary statistics  """

    def __init__(self, txHash, noInputs, noOutputs, totalInput, totalOutput):
        self.txHash = txHash
        self.noInputs = noInputs
        self.noOutputs = noOutputs
        self.totalInput = totalInput
        self.totalOutput = totalOutput

    @staticmethod
    def from_row(row, exchange_rates):
        return BlockTxSummary(row.tx_hash.hex(),
                              row.no_inputs,
                              row.no_outputs,
                              ConvertedValue(row.total_input,
                                             exchange_rates).to_dict(),
                              ConvertedValue(row.total_output,
                                             exchange_rates).to_dict()
                              )

    def to_dict(self):
        return self.__dict__


class BlockTxs(object):
    """ Model representing all transactions of a given block """

    def __init__(self, height, txs):
        self.height = height
        self.txs = txs

    @staticmethod
    def from_row(row, exchange_rates):
        tx_summaries = [BlockTxSummary.from_row(tx, exchange_rates).to_dict()
                        for tx in row.txs]

        return BlockTxs(row.height, tx_summaries)

    def to_dict(self):
        return self.__dict__
