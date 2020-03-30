from gsrest.model.addresses import Address
from gsrest.model.common import Values, compute_balance
from gsrest.model.txs import TxSummary


class Entity(object):
    """ Model representing an entity """

    def __init__(self, entity, first_tx, in_degree,
                 last_tx, no_addresses, no_incoming_txs, no_outgoing_txs,
                 out_degree, total_received, total_spent, rates):
        self.entity = entity
        self.first_tx = TxSummary(first_tx.height, first_tx.timestamp,
                                  first_tx.tx_hash.hex()).to_dict()
        self.last_tx = TxSummary(last_tx.height, last_tx.timestamp,
                                 last_tx.tx_hash.hex()).to_dict()
        self.in_degree = in_degree
        self.no_addresses = no_addresses
        self.no_incoming_txs = no_incoming_txs
        self.no_outgoing_txs = no_outgoing_txs
        self.out_degree = out_degree
        self.total_received = Values(**total_received._asdict()).to_dict()
        self.total_spent = Values(**total_spent._asdict()).to_dict()
        self.balance = compute_balance(total_received.value,
                                       total_spent.value,
                                       rates)

    @staticmethod
    def from_row(row, rates):
        return Entity(row.cluster, row.first_tx,
                      row.in_degree, row.last_tx, row.no_addresses,
                      row.no_incoming_txs, row.no_outgoing_txs, row.out_degree,
                      row.total_received, row.total_spent, rates)

    def to_dict(self):
        return self.__dict__


class EntityIncomingRelations(object):
    def __init__(self, estimated_value, no_txs, tx_list, src_properties, rate,
                 src_cluster, dst_cluster, labels, from_search=False):
        self.id = src_cluster
        self.node_type = 'entity'
        self.received = Values(**src_properties.total_received._asdict())\
            .to_dict()
        self.balance = compute_balance(src_properties.total_received.value,
                                       src_properties.total_received.value,
                                       rate)
        self.no_txs = no_txs
        self.tx_list = None
        if tx_list:
            self.tx_list = [tx_hash.hex() for tx_hash in tx_list]
        self.estimated_value = Values(**estimated_value._asdict()).to_dict()
        self.labels = labels
        if from_search:
            self.src_entity = src_cluster
            self.dst_entity = dst_cluster

    @staticmethod
    def from_row(row, rates, from_search=False):
        return EntityIncomingRelations(row.value, row.no_transactions,
                                       row.tx_list, row.src_properties, rates,
                                       row.src_cluster, row.dst_cluster,
                                       row.src_labels, from_search)

    def to_dict(self):
        return self.__dict__


class EntityOutgoingRelations(object):
    def __init__(self, estimated_value, no_txs, tx_list, dst_properties, rates,
                 dst_cluster, src_cluster, labels, from_search=False):
        self.id = dst_cluster
        self.node_type = 'entity'
        self.received = Values(**dst_properties.total_received._asdict())\
            .to_dict()
        self.balance = compute_balance(dst_properties.total_received.value,
                                       dst_properties.total_received.value,
                                       rates)
        self.no_txs = no_txs
        self.tx_list = None
        if tx_list:
            self.tx_list = [tx_hash.hex() for tx_hash in tx_list]
        self.estimated_value = Values(**estimated_value._asdict()).to_dict()
        self.labels = labels
        if from_search:
            self.dst_entity = dst_cluster
            self.src_entity = src_cluster

    @staticmethod
    def from_row(row, rates, from_search=False):
        return EntityOutgoingRelations(row.value, row.no_transactions,
                                       row.tx_list, row.dst_properties, rates,
                                       row.dst_cluster, row.src_cluster,
                                       row.dst_labels, from_search)

    def to_dict(self):
        return self.__dict__


class EntityAddress(Address):
    def __init__(self, entity, address, first_tx, last_tx, no_incoming_txs,
                 no_outgoing_txs, total_received, total_spent, in_degree,
                 out_degree, rates):
        super().__init__(address, first_tx, last_tx, no_incoming_txs,
                         no_outgoing_txs, total_received, total_spent,
                         in_degree, out_degree, rates)

        self.entity = entity

    @staticmethod
    def from_entity_row(row, address, rates):
        return EntityAddress(row.cluster, address, row.first_tx, row.last_tx,
                             row.no_incoming_txs, row.no_outgoing_txs,
                             row.total_received, row.total_spent,
                             row.in_degree, row.out_degree, rates)
