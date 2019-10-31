class Block(object):
    """ Block model for storing block related details """

    def __init__(self, height, blockHash, noTransactions, timestamp):
        self.height = height
        self.blockHash = blockHash
        self.noTransactions = noTransactions
        self.timestamp = timestamp

    @staticmethod
    def from_row(row):
        return Block(row.height, row.block_hash.hex(),
                     row.no_transactions, row.timestamp)
