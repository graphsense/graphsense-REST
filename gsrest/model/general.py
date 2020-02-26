class Statistics(object):
    """ Model representing summary statistics of a cryptocurrency """

    def __init__(self, no_blocks, no_address_relations, no_addresses,
                 no_clusters, no_txs, no_tags, timestamp):
        version = '0.4.3.dev'
        self.no_blocks = no_blocks
        self.no_address_relations = no_address_relations
        self.no_addresses = no_addresses
        self.no_entities = no_clusters
        self.no_txs = no_txs
        self.no_labels = no_tags
        self.timestamp = timestamp
        self.tools = [{'visible_name': 'GraphSense',
                       'id': 'ait:graphsense',
                       'version': version,
                       'titanium_replayable': True,
                       'responsible_for': []}]
        self.data_sources = [{'visible_name': 'Bitcoin Blockchain',
                              'id': 'bitcoin_ledger',
                              'version': {'blocks': no_blocks,
                                          'timestamp': timestamp},
                              'report_uuid': 'btc_ledger'
                              },
                             {'visible_name': 'GraphSense attribution tags',
                              'id': 'graphsense_tags',
                              'version': version}]
        self.notes = [{'note': 'Please **note** that the clustering dataset '
                               'is build with multi input address clustering'
                               'to avoid false '
                               'clustering results due to coin joins (see '
                               'titanium glossary http://titanium-project.eu/'
                               'glossary/#coinjoin), we exclude coin joins '
                               'prior to clustering. This does not eliminate '
                               'the risk of false results, since coin join '
                               'detection is also heuristic in nature, but it'
                               ' should decrease the potential for wrong '
                               'cluster merges.'},
                      {'note': 'Our tags are all manually crawled or from '
                               'credible sources, we do not use tags that'
                               ' where automatically extracted without human'
                               ' interaction. Origins of the tags have been'
                               ' saved for reproducibility please contact'
                               ' the GraphSense team for '
                               'more insight.'}]

    @staticmethod
    def from_row(row):
        return Statistics(row.no_blocks, row.no_address_relations,
                          row.no_addresses, row.no_clusters,
                          row.no_transactions, row.no_tags, row.timestamp)

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
