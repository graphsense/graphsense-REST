class Block(object):
    """ Block model for storing block related details """

    def __init__(self, row):
        self.height = row.height
        self.blockHash = row.block_hash.hex()
        self.noTransactions = row.no_transactions
        self.timestamp = row.timestamp
