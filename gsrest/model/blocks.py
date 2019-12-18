from gsrest.model.common import ConvertedValues


class Block(object):
    """ Model representing block header fields and summary statistics """

    def __init__(self, height, block_hash, no_txs, timestamp):
        self.height = height
        self.block_hash = block_hash
        self.no_txs = no_txs
        self.timestamp = timestamp

    @staticmethod
    def from_row(row):
        return Block(row.height, row.block_hash.hex(),
                     row.no_transactions, row.timestamp)

    def to_dict(self):
        return self.__dict__


class BlockTxSummary(object):
    """ Model representing block transaction summary statistics  """

    def __init__(self, tx_hash, no_inputs, no_outputs, total_input,
                 total_output):
        self.tx_hash = tx_hash
        self.no_inputs = no_inputs
        self.no_outputs = no_outputs
        self.total_input = total_input
        self.total_output = total_output

    @staticmethod
    def from_row(row, exchange_rates):
        return BlockTxSummary(row.tx_hash.hex(),
                              row.no_inputs,
                              row.no_outputs,
                              ConvertedValues(row.total_input,
                                              exchange_rates).to_dict(),
                              ConvertedValues(row.total_output,
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
