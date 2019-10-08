

def byte_to_hex(bytebuffer):
    return "".join(("%02x" % a) for a in bytebuffer)


# CASSSANDRA TYPES
class TxInputOutput(object):
    def __init__(self, address, value):
        self.address = address[0]
        self.value = value


class Value(object):
    def __init__(self, satoshi, eur, usd):
        self.satoshi = satoshi
        self.eur = round(eur, 2)
        self.usd = round(usd, 2)

    def __sub__(self, other):
        return Value(self.satoshi-other.satoshi,
                     round(self.eur-other.eur, 2),
                     round(self.usd-other.usd, 2))


class TxIdTime(object):
    def __init__(self, height, tx_hash, timestamp):
        self.height = height
        self.tx_hash = tx_hash
        self.timestamp = timestamp

    def serialize(self):
        return {
            "height": self.height,
            "tx_hash": self.tx_hash,
            "timestamp": self.timestamp,
        }


class AddressSummary(object):
    def __init__(self, total_received, total_spent):
        self.totalReceived = total_received
        self.totalSpent = total_spent


# CASSSANDRA TABLES
class ExchangeRate(object):
    def __init__(self, d):
        self.eur = d["eur"]
        self.usd = d["usd"]


class Statistics(object):
    def __init__(self, row):
        self.no_blocks = row.no_blocks
        self.no_address_relations = row.no_address_relations
        self.no_addresses = row.no_addresses
        self.no_clusters = row.no_clusters
        self.no_transactions = row.no_transactions
        self.no_labels = row.no_tags
        self.timestamp = row.timestamp


class Tag(object):
    def __init__(self, row):
        self.address = row.address
        self.label = row.label
        self.category = row.category
        self.tagpack_uri = row.tagpack_uri
        self.source = row.source
        self.lastmod = row.lastmod


class Label(object):
    def __init__(self, row):
        self.label_norm_prefix = row.label_norm_prefix
        self.label_norm = row.label_norm
        self.label = row.label
        self.address_count = row.address_count

class Transaction(object):
    def __init__(self, row, rates):
        self.txHash = byte_to_hex(row.tx_hash)
        self.coinbase = row.coinbase
        self.height = row.height
        if row.inputs:
            self.inputs = [TxInputOutput(input.address,
                                         Value(input.value,
                                               round(input.value*rates.eur*1e-8, 2),
                                               round(input.value*rates.usd*1e-8, 2)).__dict__).__dict__
                           for input in row.inputs]
        else:
            self.inputs = []
        self.outputs = [TxInputOutput(output.address,
                                      Value(output.value,
                                            round(output.value*rates.eur*1e-8, 2),
                                            round(output.value*rates.usd*1e-8, 2)).__dict__).__dict__
                        for output in row.outputs if output.address]
        self.timestamp = row.timestamp
        self.totalInput = Value(row.total_input,
                                round(row.total_input*rates.eur*1e-8, 2),
                                round(row.total_input*rates.usd*1e-8, 2)).__dict__
        self.totalOutput = Value(row.total_output,
                                 round(row.total_output*rates.eur*1e-8, 2),
                                 round(row.total_output*rates.usd*1e-8, 2)).__dict__


class BlockTransaction(object):
    def __init__(self, row, rates):
        self.txHash = byte_to_hex(row.tx_hash)
        self.noInputs = row.no_inputs
        self.noOutputs = row.no_outputs
        self.totalInput = Value(row.total_input,
                                round(row.total_input*rates.eur*1e-8, 2),
                                round(row.total_input*rates.usd*1e-8, 2)).__dict__
        self.totalOutput = Value(row.total_output,
                                 round(row.total_output*rates.eur*1e-8, 2),
                                 round(row.total_output*rates.usd*1e-8, 2)).__dict__


class Block(object):
    def __init__(self, row):
        self.height = row.height
        self.blockHash = byte_to_hex(row.block_hash)
        self.noTransactions = row.no_transactions
        self.timestamp = row.timestamp


class BlockWithTransactions(object):
    def __init__(self, row, rates):
        self.height = row.height
        self.txs = [BlockTransaction(tx, rates).__dict__ for tx in row.txs]


class Address(object):
    def __init__(self, row, exchange_rate):
        self.address_prefix = row.address_prefix
        self.address = row.address
        self.firstTx = TxIdTime(row.first_tx.height,
                                byte_to_hex(row.first_tx.tx_hash),
                                row.first_tx.timestamp).__dict__
        self.lastTx = TxIdTime(row.last_tx.height,
                               byte_to_hex(row.last_tx.tx_hash),
                               row.last_tx.timestamp).__dict__
        self.noIncomingTxs = row.no_incoming_txs
        self.noOutgoingTxs = row.no_outgoing_txs
        received = Value(row.total_received.satoshi,
                         round(row.total_received.eur, 2),
                         round(row.total_received.usd, 2))
        self.totalReceived = received.__dict__
        spent = Value(row.total_spent.satoshi,
                      round(row.total_spent.eur, 2),
                      round(row.total_spent.usd, 2))
        self.totalSpent = spent.__dict__
        balance = compute_balance(row.total_received.satoshi,
                                  row.total_spent.satoshi,
                                  exchange_rate)
        self.balance = balance.__dict__
        self.inDegree = row.in_degree
        self.outDegree = row.out_degree


def compute_balance(total_received_satoshi, total_spent_satoshi,
                    exchange_rate):
    balance_satoshi = total_received_satoshi - total_spent_satoshi
    balance = Value(balance_satoshi,
                    round(balance_satoshi*exchange_rate.eur*1e-8, 2),
                    round(balance_satoshi*exchange_rate.usd*1e-8, 2))
    return balance


def compute_exchanged_value(value, exchange_rate):
    return Value(value,
                 round(value*exchange_rate.eur*1e-8, 2),
                 round(value*exchange_rate.usd*1e-8, 2))


class AddressTransactions(object):
    def __init__(self, row, rates):
        self.address = row.address
        self.address_prefix = row.address_prefix
        self.txHash = byte_to_hex(row.tx_hash)
        self.value = Value(row.value,
                           round(row.value*rates.eur*1e-8, 2),
                           round(row.value*rates.usd*1e-8, 2)).__dict__
        self.height = row.height
        self.timestamp = row.timestamp
        self.txIndex = row.tx_index


class Cluster(object):
    def __init__(self, row, exchange_rate):
        self.cluster = int(row.cluster)
        self.firstTx = TxIdTime(row.first_tx.height,
                                byte_to_hex(row.first_tx.tx_hash),
                                row.first_tx.timestamp).__dict__
        self.lastTx = TxIdTime(row.last_tx.height,
                               byte_to_hex(row.last_tx.tx_hash),
                               row.last_tx.timestamp).__dict__
        self.noAddresses = row.no_addresses
        self.noIncomingTxs = row.no_incoming_txs
        self.noOutgoingTxs = row.no_outgoing_txs
        received = Value(row.total_received.satoshi,
                         round(row.total_received.eur, 2),
                         round(row.total_received.usd, 2))
        self.totalReceived = received.__dict__
        spent = Value(row.total_spent.satoshi,
                      round(row.total_spent.eur, 2),
                      round(row.total_spent.usd, 2))
        self.totalSpent = spent.__dict__
        balance = compute_balance(row.total_received.satoshi,
                                  row.total_spent.satoshi,
                                  exchange_rate)
        self.balance = balance.__dict__
        self.inDegree = row.in_degree
        self.outDegree = row.out_degree


class AddressIncomingRelations(object):
    def __init__(self, row, exchange_rate):
        self.dstAddressPrefix = row.dst_address_prefix
        self.dstAddress = row.dst_address
        self.estimatedValue = Value(row.estimated_value.satoshi,
                                    round(row.estimated_value.eur, 2),
                                    round(row.estimated_value.usd, 2)).__dict__
        self.srcAddress = row.src_address
        self.noTransactions = row.no_transactions
        self.srcBalance = compute_balance(row.src_properties.total_received,
                                          row.src_properties.total_spent,
                                          exchange_rate)
        self.srcTotalReceived = compute_exchanged_value(row.src_properties.total_received,
                                                        exchange_rate)
        self.srcProperties = AddressSummary(row.src_properties.total_received,
                                            row.src_properties.total_spent)

    def id(self):
        return self.srcAddress

    def toJsonNode(self):
        node = {"id": self.id(),
                "nodeType": "address",
                "received": self.srcProperties.totalReceived,
                "balance": (self.srcProperties.totalReceived -
                            self.srcProperties.totalSpent)  # satoshi
                }
        return node

    def toJsonEdge(self):
        edge = {"source": self.srcAddress,
                "target": self.dstAddress,
                "transactions": self.noTransactions,
                "estimatedValue": self.estimatedValue}
        return edge

    def toJson(self):
        return {
            "id": self.id(),
            "nodeType": "address",
            "received": self.srcTotalReceived.__dict__,
            "balance": self.srcBalance.__dict__,
            "noTransactions": self.noTransactions,
            "estimatedValue": self.estimatedValue
        }


class AddressOutgoingRelations(object):
    def __init__(self, row, exchange_rate):
        self.srcAddressPrefix = row.src_address_prefix
        self.srcAddress = row.src_address
        self.estimatedValue = Value(row.estimated_value.satoshi,
                                    round(row.estimated_value.eur, 2),
                                    round(row.estimated_value.usd, 2)).__dict__
        self.dstAddress = row.dst_address
        self.noTransactions = row.no_transactions
        self.dstBalance = compute_balance(row.dst_properties.total_received,
                                          row.dst_properties.total_spent,
                                          exchange_rate)
        self.dstTotalReceived = compute_exchanged_value(row.dst_properties.total_received,
                                                        exchange_rate)
        self.dstProperties = AddressSummary(row.dst_properties.total_received,
                                            row.dst_properties.total_spent)

    def id(self):
        return self.dstAddress

    def toJsonNode(self):
        node = {"id": self.id(),
                "nodeType": "address",
                "received": self.dstProperties.totalReceived,
                "balance": (self.dstProperties.totalReceived -
                            self.dstProperties.totalSpent)  # satoshi
                }
        return node

    def toJsonEdge(self):
        edge = {"source": self.srcAddress,
                "target": self.dstAddress,
                "transactions": self.noTransactions,
                "estimatedValue": self.estimatedValue}
        return edge

    def toJson(self):
        return {
            "id": self.id(),
            "nodeType": "address",
            "received": self.dstTotalReceived.__dict__,
            "balance": self.dstBalance.__dict__,
            "noTransactions": self.noTransactions,
            "estimatedValue": self.estimatedValue
        }


class ClusterSummary(object):
    def __init__(self, no_addresses, total_received, total_spent):
        self.noAddresses = no_addresses
        self.totalReceived = total_received
        self.totalSpent = total_spent


class ClusterIncomingRelations(object):
    def __init__(self, row, exchange_rate):
        self.dstCluster = row.dst_cluster
        self.srcCluster = row.src_cluster
        self.srcProperties = ClusterSummary(row.src_properties.no_addresses,
                                            row.src_properties.total_received,
                                            row.src_properties.total_spent)
        self.value = Value(row.value.satoshi,
                           round(row.value.eur, 2),
                           round(row.value.usd, 2)).__dict__
        self.noTransactions = row.no_transactions
        self.srcBalance = compute_balance(row.src_properties.total_received,
                                          row.src_properties.total_spent,
                                          exchange_rate)
        self.srcTotalReceived = compute_exchanged_value(row.src_properties.total_received,
                                                        exchange_rate)

    def id(self):
        return self.srcCluster

    def toJsonNode(self):
        node = {"id": self.id(),
                "nodeType": "cluster" if isinstance(self.id(), int) else "address",
                "received": self.srcProperties.totalReceived,
                "balance": (self.srcProperties.totalReceived -
                            self.srcProperties.totalSpent)  # satoshi
                }
        return node

    def toJsonEdge(self):
        edge = {"source": self.srcCluster,
                "target": self.dstCluster,
                "transactions": self.noTransactions,
                "estimatedValue": self.value}
        return edge

    def toJson(self):
        return {
            "id": self.id(),
            "nodeType": "cluster" if isinstance(self.id(), int) else "address",
            "received": self.srcTotalReceived.__dict__,
            "balance": self.srcBalance.__dict__,
            "noTransactions": self.noTransactions,
            "estimatedValue": self.value
        }


class ClusterOutgoingRelations(object):
    def __init__(self, row, exchange_rate):
        self.srcCluster = row.src_cluster
        self.dstCluster = row.dst_cluster
        self.dstProperties = ClusterSummary(row.dst_properties.no_addresses,
                                            row.dst_properties.total_received,
                                            row.dst_properties.total_spent)
        self.value = Value(row.value.satoshi,
                           round(row.value.eur, 2),
                           round(row.value.usd, 2)).__dict__
        self.noTransactions = row.no_transactions
        self.dstBalance = compute_balance(row.dst_properties.total_received,
                                          row.dst_properties.total_spent,
                                          exchange_rate)
        self.dstTotalReceived = compute_exchanged_value(row.dst_properties.total_received,
                                                        exchange_rate)

    def id(self):
        return self.dstCluster

    def toJsonNode(self):
        node = {"id": self.id(),
                "nodeType": "cluster" if isinstance(self.id(), int) else "address",
                "received": self.dstProperties.totalReceived,
                "balance": (self.dstProperties.totalReceived -
                            self.dstProperties.totalSpent),  # satoshi
                }
        return node

    def toJsonEdge(self):
        edge = {"source": self.srcCluster,
                "target": self.dstCluster,
                "transactions": self.noTransactions,
                "estimatedValue": self.value}
        return edge

    def toJson(self):
        return {
            "id": self.id(),
            "nodeType": "cluster" if isinstance(self.id(), int) else "address",
            "received": self.dstTotalReceived.__dict__,
            "balance": self.dstBalance.__dict__,
            "noTransactions": self.noTransactions,
            "estimatedValue": self.value
        }


class ClusterAddresses(object):
    def __init__(self, row, exchange_rate):
        self.cluster = row.cluster
        self.address = row.address
        self.noIncomingTxs = row.no_incoming_txs
        self.noOutgoingTxs = row.no_outgoing_txs
        self.firstTx = TxIdTime(row.first_tx.height,
                                byte_to_hex(row.first_tx.tx_hash),
                                row.first_tx.timestamp).__dict__
        self.lastTx = TxIdTime(row.last_tx.height,
                               byte_to_hex(row.last_tx.tx_hash),
                               row.last_tx.timestamp).__dict__
        totalReceived = Value(row.total_received.satoshi,
                              round(row.total_received.eur, 2),
                              round(row.total_received.usd, 2))
        self.totalReceived = totalReceived.__dict__
        totalSpent = Value(row.total_spent.satoshi,
                           round(row.total_spent.eur, 2),
                           round(row.total_spent.usd, 2))
        self.totalSpent = totalSpent.__dict__
        balance = compute_balance(row.total_received.satoshi,
                                  row.total_spent.satoshi,
                                  exchange_rate)
        self.balance = balance.__dict__
        self.inDegree = row.in_degree
        self.outDegree = row.out_degree
