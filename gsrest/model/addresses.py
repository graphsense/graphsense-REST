from gsrest.model.blocks import ConvertedValues
from gsrest.model.common import Values, compute_balance
from gsrest.model.txs import TxSummary


class Address(object):
    """ Model representing an address """

    def __init__(self, address, first_tx, last_tx, no_incoming_txs,
                 no_outgoing_txs, total_received, total_spent, in_degree,
                 out_degree, rates):
        self.address = address
        self.first_tx = TxSummary(first_tx.height, first_tx.timestamp,
                                  first_tx.tx_hash.hex()).to_dict()
        self.last_tx = TxSummary(last_tx.height, last_tx.timestamp,
                                 last_tx.tx_hash.hex()).to_dict()
        self.no_incoming_txs = no_incoming_txs
        self.no_outgoing_txs = no_outgoing_txs
        self.total_received = Values(**total_received._asdict()).to_dict()
        self.total_spent = Values(**total_spent._asdict()).to_dict()
        self.in_degree = in_degree
        self.out_degree = out_degree
        self.balance = compute_balance(total_received.value,
                                       total_spent.value,
                                       rates)

    @staticmethod
    def from_row(row, rates):
        return Address(row.address, row.first_tx, row.last_tx,
                       row.no_incoming_txs, row.no_outgoing_txs,
                       row.total_received, row.total_spent,
                       row.in_degree, row.out_degree, rates)

    def to_dict(self):
        return self.__dict__


class AddressTx(object):
    def __init__(self, address, height, timestamp, tx_hash, value,
                 rates):
        self.address = address
        self.height = height
        self.timestamp = timestamp
        self.tx_hash = tx_hash
        self.value = ConvertedValues(value, rates).to_dict()

    @staticmethod
    def from_row(row, address, rates):
        return AddressTx(address, row.height, row.timestamp, row.tx_hash.hex(),
                         row.value, rates)

    def to_dict(self):
        return self.__dict__


class ReceivedSpent(object):
    def __init__(self, total_received, total_spent):
        self.total_received = total_received
        self.total_spent = total_spent

    def to_dict(self):
        return self.__dict__


class AddressOutgoingRelations(object):
    def __init__(self, estimated_value, dst_address, no_txs, tx_list,
                 dst_properties, labels, rates):
        self.id = dst_address
        self.node_type = 'address'
        self.labels = labels
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

    @staticmethod
    def from_row(row, dst_address, rates):
        return AddressOutgoingRelations(row.estimated_value,
                                        dst_address, row.no_transactions,
                                        row.tx_list, row.dst_properties,
                                        row.dst_labels, rates)

    def to_dict(self):
        return self.__dict__


class AddressIncomingRelations(object):
    def __init__(self, estimated_value, src_address, no_txs, tx_list,
                 src_properties, labels, rates):
        self.id = src_address
        self.node_type = 'address'
        self.labels = labels
        self.received = Values(**src_properties.total_received._asdict())\
            .to_dict()
        self.balance = compute_balance(src_properties.total_received.value,
                                       src_properties.total_received.value,
                                       rates)
        self.no_txs = no_txs
        self.tx_list = None
        if tx_list:
            self.tx_list = [tx_hash.hex() for tx_hash in tx_list]
        self.estimated_value = Values(**estimated_value._asdict()).to_dict()

    @staticmethod
    def from_row(row, src_address, rates):
        return AddressIncomingRelations(row.estimated_value,
                                        src_address, row.no_transactions,
                                        row.tx_list, row.src_properties,
                                        row.src_labels, rates)

    def to_dict(self):
        return self.__dict__
