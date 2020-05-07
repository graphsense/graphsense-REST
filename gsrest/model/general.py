from datetime import datetime


class Statistics(object):
    """ Model representing summary statistics of a cryptocurrency """

    def __init__(self, no_blocks, no_address_relations, no_addresses,
                 no_clusters, no_txs, no_tags, timestamp, currency):
        ledger = {'visible_name': currency.upper() + ' Blockchain',
                  'id': currency + '_ledger',
                  'version': {'nr': str(no_blocks),
                              'timestamp': datetime.utcfromtimestamp(timestamp)
                              .strftime("%Y-%m-%d %H:%M:%S")},
                  'report_uuid': currency + '_ledger'}
        self.no_blocks = no_blocks
        self.no_address_relations = no_address_relations
        self.no_addresses = no_addresses
        self.no_entities = no_clusters
        self.no_txs = no_txs
        self.no_labels = no_tags
        self.timestamp = timestamp
        self.tools = []
        self.data_sources = [ledger]
        self.notes = []

    @staticmethod
    def from_row(row, currency):
        return Statistics(row.no_blocks, row.no_address_relations,
                          row.no_addresses, row.no_clusters,
                          row.no_transactions, row.no_tags, row.timestamp,
                          currency)

    def to_dict(self):
        return self.__dict__


class Concept(object):
    """Concept Definition.
    This class serves as a proxy for a concept that is defined
    in some remote taxonomy. It just provides the most essential properties.
    A concept can be viewed as an idea or notion; a unit of thought.
    See: https://www.w3.org/TR/skos-reference/#concepts
    """

    def __init__(self, taxonomy, id, uri, label, description):
        self.taxonomy = taxonomy
        self.id = id
        self.uri = uri
        self.label = label
        self.description = description

    @staticmethod
    def from_row(row):
        return Concept(row.taxonomy, row.id, row.uri, row.label,
                       row.description)

    def to_dict(self):
        return self.__dict__


class Taxonomy(object):
    """ Model representing a taxonomy """

    def __init__(self, taxonomy, uri):
        self.taxonomy = taxonomy
        self.uri = uri

    @staticmethod
    def from_row(row):
        return Taxonomy(row.key, row.uri)

    def to_dict(self):
        return self.__dict__
