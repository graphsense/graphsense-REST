import cassandra.cluster
from cassandra.query import SimpleStatement
from graphsensemodel import (Block, Tag, Transaction, ExchangeRate, Address, Cluster, AddressIncomingRelations, AddressOutgoingRelations, AddressEgoNet, ClusterEgoNet, ClusterIncomingRelations, ClusterOutgoingRelations, ClusterAddresses, AddressTransactions, BlockWithTransactions)
from flask import abort

session = None
tx_query = None
txs_query = None
block_query = None
block_transactions_query = None
blocks_query = None
exchange_rates_query = None
exchange_rate_for_height_query = None
address_query = None
address_transactions_query = None
address_tags_query = None
address_search_query = None
transaction_search_query = None
address_cluster_query = None
cluster_tags_query = None
cluster_query = None
address_incoming_relations_query = None
address_outgoing_relations_query = None
cluster_incoming_relations_query = None
cluster_outgoing_relations_query = None
cluster_addresses_query = None
block_height_query = None
currency_mapping = None
exchange_rates = {}
last_height = {}

def query_exchange_rates(currency, page_state):
    set_keyspace(session, currency)
    if page_state:
        page_state = bytes.fromhex(page_state)
        results = session.execute(exchange_rates_query, paging_state=page_state)
    else:
        results = session.execute(exchange_rates_query)
    page_state = results.paging_state
    exchange_rates = [ExchangeRate(row).__dict__ for row in results.current_rows]
    return page_state, exchange_rates

def query_block(currency, height):
    set_keyspace(session, currency)
    if height > last_height[currency]:
        abort(404, 'Block not available yet')
    result = session.execute(block_query, [height])
    return Block(result[0]).__dict__ if result else None

def query_block_transactions(currency, height):
    set_keyspace(session, currency)
    if height > last_height[currency]:
        abort(404, 'Block not available yet')
    result = session.execute(block_transactions_query, [height])
    return BlockWithTransactions(result[0], query_exchange_rate_for_height(currency, height)).__dict__ if result else None

def query_blocks(currency, page_state):
    set_keyspace(session, currency)
    if page_state is not None:
        page_state = bytes.fromhex(page_state)
        results = session.execute(blocks_query, paging_state=page_state)
    else:
        results = session.execute(blocks_query)
    page_state = results.paging_state
    blocks = [Block(row).__dict__ for row in results.current_rows]
    return page_state, blocks

def query_transaction(currency, txHash):
    set_keyspace(session, currency)
    try:
        rows = session.execute(tx_query, [txHash[0:5], bytearray.fromhex(txHash)])
    except:
        abort(404, 'Transaction hash is not hex')
    return Transaction(rows[0], query_exchange_rate_for_height(currency, rows[0].height)).__dict__ if rows else None

def query_transactions(currency, page_state):
    set_keyspace(session, currency)
    if page_state is not None:
        page_state = bytes.fromhex(page_state)
        results = session.execute(txs_query, paging_state=page_state)
    else:
        results = session.execute(txs_query)
    page_state = results.paging_state
    transactions = [Transaction(row, currency).__dict__ for row in results.current_rows]
    return page_state, transactions

def query_transaction_search(currency, expression):
    set_keyspace(session, currency)
    transactions = session.execute(transaction_search_query, [expression])
    transactions._fetch_all()
    return transactions

def query_address_search(currency, expression):
    set_keyspace(session, currency)
    addresses = session.execute(address_search_query, [expression])
    addresses._fetch_all()
    return addresses

def query_address(currency, address):
    set_keyspace(session, currency)
    rows = session.execute(address_query, [address, address[0:5]])
    return Address(rows[0], exchange_rates[currency]) if rows else None

def query_address_cluster(currency, address):
    set_keyspace(session, currency)
    clusterids = session.execute(address_cluster_query, [address, address[0:5]])
    ret = {}
    if clusterids:
        clusterid = clusterids[0].cluster
        cluster_obj = query_cluster(currency, clusterid)
        ret = cluster_obj.__dict__
    return ret

def query_address_transactions(currency, address, limit):
    set_keyspace(session, currency)
    rows = session.execute(address_transactions_query, [address, address[0:5], int(limit)])
    return [row for (row) in rows]

def query_address_tags(currency, address):
    set_keyspace(session, currency)
    tags = session.execute(address_tags_query, [address])
    return [Tag(row).__dict__ for (row) in tags.current_rows]

def query_implicit_tags(currency, address):
    set_keyspace(session, currency)
    clusters = session.execute(address_cluster_query, [address, address[0:5]])
    implicit_tags = []
    for (clusterrow) in clusters:
        clustertags = query_cluster_tags(currency, clusterrow.cluster)
        if clustertags:
            implicit_tags.extend(clustertags)
    return implicit_tags

def query_address_incoming_relations(currency, address, limit):
    set_keyspace(session, currency)
    rows = session.execute(address_incoming_relations_query, [address[0:5], address, limit])
    relations = [AddressIncomingRelations(row) for row in rows.current_rows]
    return relations

def query_address_outgoing_relations(currency, address, limit):
    set_keyspace(session, currency)
    rows = session.execute(address_outgoing_relations_query, [address[0:5], address, limit])
    relations = [AddressOutgoingRelations(row) for row in rows.current_rows]
    return relations

def query_cluster(currency, cluster):
    set_keyspace(session, currency)
    rows = session.execute(cluster_query, [int(cluster)])
    return Cluster(rows.current_rows[0], exchange_rates[currency]) if rows else None

def query_cluster_tags(currency, cluster):
    set_keyspace(session, currency)
    tags = session.execute(cluster_tags_query, [int(cluster)])
    clustertags = [Tag(tagrow).__dict__ for (tagrow) in tags]
    return clustertags

def query_cluster_addresses(currency, cluster, limit):
    set_keyspace(session, currency)
    rows = session.execute(cluster_addresses_query, [int(cluster), limit])
    clusteraddresses = [ClusterAddresses(row, exchange_rates[currency]).__dict__ for (row) in rows]
    return clusteraddresses

def query_cluster_incoming_relations(currency, cluster, limit):
    set_keyspace(session, currency)
    rows = session.execute(cluster_incoming_relations_query, [cluster, limit])
    relations = [ClusterIncomingRelations(row) for row in rows.current_rows]
    return relations

def query_cluster_outgoing_relations(currency, cluster, limit):
    set_keyspace(session, currency)
    rows = session.execute(cluster_outgoing_relations_query, [cluster, limit])
    relations = [ClusterOutgoingRelations(row) for row in rows.current_rows]
    return relations

def set_keyspace(session, currency):
    if currency in currency_mapping:
        session.set_keyspace(currency_mapping[currency])
    else:
        abort(404, "Currency %s does not exist" % currency)

def query_last_block_height(currency):
    set_keyspace(session, currency)
    block_max = 0
    block_inc = 100000
    while True:
        rs = session.execute(block_height_query, [block_max])
        if not rs:
            if block_max == 0:
                return 0
            if block_inc == 1:
                return block_max-1
            else:
                block_max -= block_inc
                block_inc //= 10
        else:
            block_max += block_inc

def query_exchange_rate_for_height(currency, height):
    set_keyspace(session, currency)
    rows = session.execute(exchange_rate_for_height_query, [height])
    return ExchangeRate(rows[0])#.__dict__


def connect(app):
    global session, currency_mapping, tx_query, txs_query, block_query, blocks_query, exchange_rates_query, \
        address_query, address_transactions_query, address_tags_query, address_search_query, transaction_search_query, \
        address_cluster_query, address_incoming_relations_query, address_outgoing_relations_query, \
        cluster_tags_query, cluster_query, cluster_incoming_relations_query, cluster_outgoing_relations_query, \
        cluster_addresses_query, block_height_query, exchange_rate_for_height_query, block_transactions_query

    cluster = cassandra.cluster.Cluster(app.config['CASSANDRA_NODES'])
    app.logger.debug("Created new Cassandra cluster.")

    # set the first keyspace in mapping to the default in order to be able to create the prepared statements
    # alternative strategy is to not use prepared statements and specify the keyspace in the query string
    currency_mapping = app.config['MAPPING']
    session = cluster.connect(currency_mapping['btc'])

    session.default_fetch_size = 10
    app.logger.debug("Created new Cassandra session.")
    tx_query = session.prepare('SELECT * FROM transaction WHERE tx_prefix = ? AND tx_hash = ?')
    txs_query = session.prepare('SELECT * FROM transaction')
    block_query = session.prepare('SELECT * FROM block WHERE height = ?')
    block_transactions_query = session.prepare('SELECT * FROM block_transactions WHERE height = ?')
    blocks_query = session.prepare('SELECT * FROM block')
    exchange_rates_query = session.prepare('SELECT * FROM exchange_rates')
    exchange_rate_for_height_query = session.prepare('SELECT * FROM exchange_rates WHERE height = ?')
    address_query = session.prepare('SELECT * FROM address WHERE address = ? AND address_prefix = ?')
    address_transactions_query = session.prepare('SELECT * FROM address_transactions WHERE address = ? AND address_prefix = ? LIMIT ?')
    address_tags_query = session.prepare('SELECT * FROM address_tags WHERE address = ?')
    address_search_query = session.prepare('SELECT address FROM address WHERE address_prefix = ?')
    address_cluster_query = session.prepare('SELECT cluster FROM address_cluster WHERE address = ? AND address_prefix = ?')
    address_incoming_relations_query = session.prepare('SELECT * FROM address_incoming_relations WHERE dst_address_prefix = ? AND dst_address = ? LIMIT ?')
    address_outgoing_relations_query = session.prepare('SELECT * FROM address_outgoing_relations WHERE src_address_prefix = ? AND src_address = ? LIMIT ?')
    cluster_incoming_relations_query = session.prepare('SELECT * FROM cluster_incoming_relations WHERE dst_cluster = ? LIMIT ?')
    cluster_outgoing_relations_query = session.prepare('SELECT * FROM cluster_outgoing_relations WHERE src_cluster = ? LIMIT ?')
    cluster_tags_query = session.prepare('SELECT * FROM cluster_tags WHERE cluster = ?')
    cluster_query = session.prepare('SELECT * FROM cluster WHERE cluster = ?')
    cluster_addresses_query = session.prepare('SELECT * FROM cluster_addresses WHERE cluster = ? LIMIT ?')
    transaction_search_query = session.prepare('SELECT tx_hash from transaction where tx_prefix = ?')
    block_height_query = session.prepare('SELECT height FROM exchange_rates WHERE height = ?')
    for key in currency_mapping.keys():
        last_height[key] = query_last_block_height(key)
        exchange_rates[key] = query_exchange_rate_for_height(key, last_height[key])

    app.logger.debug("Created prepared statements")