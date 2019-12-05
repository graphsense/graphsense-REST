from gsrest.model.txs import TxSummary
from gsrest.model.common import Values, compute_balance
from gsrest.model.addresses import Address


class Entity(object):
    """ Model representing an entity """

    def __init__(self, entity, first_tx, in_degree,
                 last_tx, no_addresses, no_incoming_txs, no_outgoing_txs,
                 out_degree, total_received, total_spent, exchange_rates):
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
                                       exchange_rates)

    @staticmethod
    def from_row(row, exchange_rates):
        return Entity(row.cluster, row.first_tx,
                      row.in_degree, row.last_tx, row.no_addresses,
                      row.no_incoming_txs, row.no_outgoing_txs, row.out_degree,
                      row.total_received, row.total_spent, exchange_rates)

    def to_dict(self):
        return self.__dict__


class EntityIncomingRelations(object):
    def __init__(self, estimated_value, src_entity,
                 no_txs, src_properties, exchange_rate):
        self.id = src_entity
        self.node_type = 'entity'
        self.received = Values(**src_properties.total_received._asdict())\
            .to_dict()
        self.balance = compute_balance(src_properties.total_received.value,
                                       src_properties.total_received.value,
                                       exchange_rate)
        self.no_txs = no_txs
        self.estimated_value = Values(**estimated_value._asdict()).to_dict()

    @staticmethod
    def from_row(row, src_entity, exchange_rate):
        return EntityIncomingRelations(row.value, src_entity,
                                       row.no_transactions, row.src_properties,
                                       exchange_rate)

    def to_dict(self):
        return self.__dict__


class EntityOutgoingRelations(object):
    def __init__(self, estimated_value, dst_entity,
                 no_txs, dst_properties, exchange_rate):
        self.id = dst_entity
        self.node_type = 'entity'
        self.received = Values(**dst_properties.total_received._asdict())\
            .to_dict()
        self.balance = compute_balance(dst_properties.total_received.value,
                                       dst_properties.total_received.value,
                                       exchange_rate)
        self.no_txs = no_txs
        self.estimated_value = Values(**estimated_value._asdict()).to_dict()

    @staticmethod
    def from_row(row, dst_entity, exchange_rate):
        return EntityOutgoingRelations(row.value,
                                        dst_entity, row.no_transactions,
                                        row.dst_properties, exchange_rate)

    def to_dict(self):
        return self.__dict__


class EntityAddress(Address):
    def __init__(self, entity, address, first_tx, last_tx, no_incoming_txs,
                 no_outgoing_txs, total_received, total_spent, in_degree,
                 out_degree, exchange_rates):
        super().__init__(address, first_tx, last_tx, no_incoming_txs,
                         no_outgoing_txs, total_received, total_spent,
                         in_degree, out_degree, exchange_rates)

        self.entity = entity

    @staticmethod
    def from_entity_row(row, address, exchange_rates):
        return EntityAddress(row.cluster, address, row.first_tx, row.last_tx,
                             row.no_incoming_txs, row.no_outgoing_txs,
                             row.total_received, row.total_spent,
                             row.in_degree, row.out_degree, exchange_rates)
