class Statistics(object):
    """ Model representing summary statistics of a cryptocurrency """

    def __init__(self, no_blocks, no_address_relations, no_addresses,
                 no_clusters, no_txs, no_tags, timestamp, currency):
        self.no_blocks = no_blocks
        self.no_address_relations = no_address_relations
        self.no_addresses = no_addresses
        self.no_entities = no_clusters
        self.no_txs = no_txs
        self.no_labels = no_tags
        self.timestamp = timestamp
        self.tools = []
        self.data_sources = [{'visible_name': currency.upper() + ' Blockchain',
                              'id': currency + '_ledger',
                              'version': {'nr': str(no_blocks),
                                          'timestamp': str(timestamp)},
                              'report_uuid': currency + '_ledger'
                              }]
        self.notes = []

    @staticmethod
    def from_row(row, currency):
        return Statistics(row.no_blocks, row.no_address_relations,
                          row.no_addresses, row.no_clusters,
                          row.no_transactions, row.no_tags, row.timestamp,
                          currency)

    def to_dict(self):
        return self.__dict__


class Category(object):
    """ Model representing a category of an entity """

    def __init__(self, category, id):
        self.category = category
        self.id = id

    @staticmethod
    def from_row(row):
        return Category(row.category, row.id)

    def to_dict(self):
        return self.__dict__


class Abuse(object):
    """ Model representing the abuse of an entity """

    def __init__(self, abuse, id):
        self.abuse = abuse
        self.id = id

    @staticmethod
    def from_row(row):
        return Abuse(row.abuse, row.id)

    def to_dict(self):
        return self.__dict__
