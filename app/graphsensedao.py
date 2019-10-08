import cassandra.cluster
from cassandra.query import named_tuple_factory, dict_factory
from flask import abort
import graphsensemodel as gm


session = None
tx_query = {}
txs_query = {}
block_query = {}
block_transactions_query = {}
blocks_query = {}
exchange_rates_query = {}
exchange_rate_for_height_query = {}
address_query = {}
address_transactions_query = {}
address_transactions_without_limit_query = {}
address_tags_query = {}
address_search_query = {}
label_search_query = None
label_query = None
transaction_search_query = {}
address_entity_query = {}
entity_tags_query = {}
entity_query = {}
address_incoming_relations_query = {}
address_incoming_relations_without_limit_query = {}
address_outgoing_relations_query = {}
address_outgoing_relations_without_limit_query = {}
entity_incoming_relations_query = {}
entity_incoming_relations_without_limit_query = {}
entity_outgoing_relations_query = {}
entity_outgoing_relations_without_limit_query = {}
entity_addresses_query = {}
entity_addresses_without_limit_query = {}
last_block_height_query = {}
statistics_query = {}
keyspace_mapping = {}
all_exchange_rates = {}
last_height = {}
tags_query = {}


def query_exchange_rates(currency, offset, limit):
    if not offset:
        offset = 0
    if not limit:
        limit = 100
    start = last_height[currency] - limit*offset
    end = last_height[currency] - limit*(offset+1)
    exchange_rates = [gm.ExchangeRate(all_exchange_rates[currency][height]).__dict__
                      for height in range(start, end, -1)]
    return exchange_rates


def query_block(currency, height):
    set_keyspace(session, currency, space="raw")
    if height > last_height[currency]:
        abort(404, "Block not available yet")
    result = session.execute(block_query[currency], [height])
    return gm.Block(result[0]).__dict__ if result else None


def query_statistics(currency):
    set_keyspace(session, currency)
    result = session.execute(statistics_query[currency])
    return gm.Statistics(result[0]).__dict__ if result else None


def query_block_transactions(currency, height):
    set_keyspace(session, currency, space="raw")
    if height > last_height[currency]:
        abort(404, "Block not available yet")
    result = session.execute(block_transactions_query[currency], [height])
    return gm.BlockWithTransactions(result[0], query_exchange_rate_for_height(currency, height)).__dict__ if result else None


def query_blocks(currency, page_state):
    set_keyspace(session, currency, space="raw")
    if page_state:
        results = session.execute(blocks_query[currency], paging_state=page_state)
    else:
        results = session.execute(blocks_query[currency], [10])
    page_state = results.paging_state
    blocks = [gm.Block(row).__dict__ for row in results]
    return page_state, blocks


def query_transaction(currency, txHash):
    set_keyspace(session, currency, space="raw")
    try:
        rows = session.execute(tx_query[currency], [txHash[0:5], bytearray.fromhex(txHash)])
    except Exception:
        abort(404, "Transaction hash is not hex")
    return gm.Transaction(rows[0], query_exchange_rate_for_height(currency, rows[0].height)).__dict__ if rows else None


def query_transactions(currency, page_state):
    set_keyspace(session, currency, space="raw")
    if page_state:
        results = session.execute(txs_query[currency], paging_state=page_state)
    else:
        results = session.execute(txs_query[currency], [10])

    page_state = results.paging_state
    transactions = [gm.Transaction(row, query_exchange_rate_for_height(currency, row.height)).__dict__
                    for row in results]
    return page_state, transactions


def query_transaction_search(currency, expression):
    set_keyspace(session, currency, space="raw")
    transactions = session.execute(transaction_search_query[currency],
                                   [expression])
    transactions._fetch_all()
    return transactions


def query_address_search(currency, expression):
    set_keyspace(session, currency)
    addresses = session.execute(address_search_query[currency], [expression])
    addresses._fetch_all()
    return addresses


def query_label_search(expression_norm_prefix):
    set_keyspace(session, "", space="tagpacks")
    labels = session.execute(label_search_query, [expression_norm_prefix])
    labels._fetch_all()
    return labels


def query_tags(label_norm_prefix, label_norm):
    set_keyspace(session, "", space="tagpacks")
    labels = session.execute(tags_query, [label_norm_prefix, label_norm])
    labels._fetch_all()
    def makeTagWithCurrency(row):
        d = gm.Tag(row).__dict__
        d["currency"] = row.currency
        return d

    tags = [makeTagWithCurrency(row) for row in labels]
    return tags


def query_label(label_norm_prefix, label_norm):
    set_keyspace(session, "", space="tagpacks")
    label = session.execute(label_query, [label_norm_prefix, label_norm])
    return gm.Label(label[0]).__dict__ if label else None


def query_address(currency, address):
    set_keyspace(session, currency)
    rows = session.execute(address_query[currency], [address, address[0:5]])
    return gm.Address(rows[0], gm.ExchangeRate(all_exchange_rates[currency][last_height[currency]])) if rows else None


def query_address_entity(currency, address):
    set_keyspace(session, currency)
    entityid = query_address_entity_id(currency, address)
    ret = {}
    if entityid:
        entity_obj = query_entity(currency, entityid)
        ret = entity_obj.__dict__
    return ret


def query_address_entity_id(currency, address):
    set_keyspace(session, currency)
    entityids = session.execute(address_entity_query[currency],
                                 [address, address[0:5]])
    if entityids:
        return entityids[0].cluster
    return None


def query_address_transactions(currency, page_state, address, pagesize, limit):
    set_keyspace(session, currency)

    if limit is None:
        query = address_transactions_without_limit_query
        params = [address, address[0:5]]
    else:
        query = address_transactions_query
        params = [address, address[0:5], limit]

    if pagesize:
        query[currency].fetch_size = pagesize

    if page_state:
        rows = session.execute(query[currency], params, paging_state=page_state)
    else:
        rows = session.execute(query[currency], params)

    page_state = rows.paging_state
    return page_state, [row for row in rows.current_rows]


def query_address_tags(currency, address):
    set_keyspace(session, currency)
    tags = session.execute(address_tags_query[currency], [address])
    return [gm.Tag(row).__dict__ for row in tags]


def query_address_with_tags(currency, address):
    result = query_address(currency, address)
    if result:
        result.tags = query_address_tags(currency, address)
    return result


def query_address_incoming_relations(currency, page_state, address, pagesize, limit):
    set_keyspace(session, currency)
    if limit is None:
        query = address_incoming_relations_without_limit_query
        params = [address[0:5], address]
    else:
        query = address_incoming_relations_query
        params = [address[0:5], address, limit]

    if pagesize:
        query[currency].fetch_size = pagesize

    if page_state:
        rows = session.execute(query[currency], params, paging_state=page_state)
    else:
        rows = session.execute(query[currency], params)

    page_state = rows.paging_state
    exchange_rate = gm.ExchangeRate(all_exchange_rates[currency][last_height[currency]])
    relations = [gm.AddressIncomingRelations(row, exchange_rate)
                 for row in rows.current_rows]
    return page_state, relations


def query_address_outgoing_relations(currency, page_state, address, pagesize, limit):
    set_keyspace(session, currency)
    if limit is None:
        query = address_outgoing_relations_without_limit_query
        params = [address[0:5], address]
    else:
        query = address_outgoing_relations_query
        params = [address[0:5], address, limit]

    if pagesize is not None:
        query[currency].fetch_size = pagesize

    if page_state is not None:
        rows = session.execute(query[currency], params, paging_state=page_state)
    else:
        rows = session.execute(query[currency], params)

    page_state = rows.paging_state
    exchange_rate = gm.ExchangeRate(all_exchange_rates[currency][last_height[currency]])
    relations = [gm.AddressOutgoingRelations(row, exchange_rate)
                 for row in rows.current_rows]
    return page_state, relations


def query_entity(currency, entity):
    set_keyspace(session, currency)
    rows = session.execute(entity_query[currency], [int(entity)])
    return gm.Entity(rows.current_rows[0],
                      gm.ExchangeRate(all_exchange_rates[currency][last_height[currency]])) if rows else None


def query_entity_tags(currency, entity):
    set_keyspace(session, currency)
    tags = session.execute(entity_tags_query[currency], [int(entity)])
    entitytags = [gm.Tag(tagrow).__dict__ for (tagrow) in tags]
    return entitytags


def query_entity_addresses(currency, entity, page, pagesize, limit):
    set_keyspace(session, currency)
    if limit is None:
        query = entity_addresses_without_limit_query
        params = [int(entity)]
    else:
        query = entity_addresses_query
        params = [int(entity), limit]

    if pagesize is not None:
        query[currency].fetch_size = pagesize

    if page:
        rows = session.execute(query[currency], params, paging_state=page)
    else:
        rows = session.execute(query[currency], params)

    entityaddresses = [gm.EntityAddresses(row, gm.ExchangeRate(all_exchange_rates[currency][last_height[currency]])).__dict__
                        for row in rows.current_rows]
    page = rows.paging_state
    return page, entityaddresses


def query_entity_incoming_relations(currency, page_state, entity, pagesize, limit):
    set_keyspace(session, currency)
    if limit is None:
        query = entity_incoming_relations_without_limit_query
        params = [int(entity)]
    else:
        query = entity_incoming_relations_query
        params = [int(entity), limit]

    if pagesize:
        query[currency].fetch_size = pagesize

    if page_state:
        rows = session.execute(query[currency], params, paging_state=page_state)
    else:
        rows = session.execute(query[currency], params)

    page_state = rows.paging_state
    exchange_rate = gm.ExchangeRate(all_exchange_rates[currency][last_height[currency]])
    relations = [gm.EntityIncomingRelations(row, exchange_rate) for row in rows.current_rows]
    return page_state, relations


def query_entity_outgoing_relations(currency, page_state, entity, pagesize, limit):
    set_keyspace(session, currency)
    if limit is None:
        query = entity_outgoing_relations_without_limit_query
        params = [int(entity)]
    else:
        query = entity_outgoing_relations_query
        params = [int(entity), limit]

    if pagesize:
        query[currency].fetch_size = pagesize

    if page_state:
        rows = session.execute(query[currency], params, paging_state=page_state)
    else:
        rows = session.execute(query[currency], params)
    page_state = rows.paging_state
    exchange_rate = gm.ExchangeRate(all_exchange_rates[currency][last_height[currency]])
    relations = [gm.EntityOutgoingRelations(row, exchange_rate) for row in rows.current_rows]
    return page_state, relations


def query_entity_search_neighbors(currency, entity, isOutgoing, category, ids, breadth, depth, skipNumAddresses, cache):
    set_keyspace(session, currency)
    if depth <= 0:
        return []

    def getCached(cl, key):
        return (cache.get(cl) or {}).get(key)

    def setCached(cl, key, value):
        if cl not in cache:
            cache[cl] = {}
        cache[cl][key] = value
        return value

    def cached(cl, key, get):
        return getCached(cl, key) or setCached(cl, key, get())

    if isOutgoing:
        (_, rows) = cached(entity, 'rows', lambda : query_entity_outgoing_relations(currency, None, entity, breadth, breadth))
    else:
        (_, rows) = cached(entity, 'rows', lambda : query_entity_incoming_relations(currency, None, entity, breadth, breadth))

    paths = []

    for row in rows:
        subentity = row.dstEntity if isOutgoing else row.srcEntity
        if not isinstance(subentity, int):
            continue
        match = True
        props = cached(subentity, 'props', lambda : query_entity(currency, subentity))
        if props is None:
            print("empty entity result for " + str(subentity))
            continue

        props = props.__dict__
        tags = cached(subentity, 'tags', lambda : query_entity_tags(currency, subentity))

        if category is not None:
            # find first occurence of category in tags
            match = next((True for t in tags if t["category"] == category), False)

        matchingAddresses = []
        if match and ids is not None:
            matchingAddresses = [id["address"] for id in ids if str(id["entity"]) == str(subentity)]
            match = len(matchingAddresses) > 0

        subpaths = False
        if match:
            subpaths = True
        elif 'noAddresses' in props and props['noAddresses'] <= skipNumAddresses:
            subpaths = query_entity_search_neighbors(currency, subentity, isOutgoing, category, ids, breadth, depth - 1, skipNumAddresses, cache)

        if not subpaths:
            continue
        props["tags"] = tags
        obj = {"node": props, "relation": row.toJson(), "matchingAddresses": []}
        if subpaths == True:
            addresses_with_tags = [ query_address_with_tags(currency, address) for address in matchingAddresses ]
            obj["matchingAddresses"] = [ address for address in addresses_with_tags if address is not None ]
            subpaths = None
        obj["paths"] = subpaths
        paths.append(obj)
    return paths


def set_keyspace(session, currency=None, space="transformed"):
    if space == "tagpacks":
        session.set_keyspace(keyspace_mapping["tagpacks"])
        return

    if currency in keyspace_mapping:
        if space == "raw":
            session.set_keyspace(keyspace_mapping[currency][0])
        elif space == "transformed":
            session.set_keyspace(keyspace_mapping[currency][1])
        else:
            abort(404, "Keyspace %s not allowed" % space)
    else:
        abort(404, "Currency %s does not exist" % currency)


def query_all_exchange_rates(currency, h_max):
    try:
        set_keyspace(session, currency)
        session.row_factory = dict_factory
        session.default_fetch_size = None
        print("Loading exchange rates for %s ..." % currency)
        results = session.execute(exchange_rates_query[currency], [h_max + 1],
                                  timeout=180)
        d = {row["height"]: {"eur": row["eur"], "usd": row["usd"]}
             for row in results}
        print("Rates loaded.")
        session.row_factory = named_tuple_factory  # reset default
        return d
    except Exception as e:
        session.row_factory = named_tuple_factory
        print("Failed to query exchange rates. Cause: \n%s" % str(e))
        raise SystemExit


def query_last_block_height(currency):
    set_keyspace(session, currency, space="raw")
    res = session.execute(last_block_height_query[currency])
    h = int(res.current_rows[0].no_blocks) - 1
    return h


def query_exchange_rate_for_height(currency, height):
    if height <= last_height[currency]:
        res = gm.ExchangeRate(all_exchange_rates[currency][height])
    else:
        res = gm.ExchangeRate(all_exchange_rates[currency][last_height[currency]])
    return res


def connect(app):
    global address_entity_query, address_incoming_relations_query, \
           address_outgoing_relations_query, address_query, \
           address_search_query, address_tags_query, \
           address_transactions_query, all_exchange_rates, \
           last_block_height_query, block_query, block_transactions_query, \
           blocks_query, entity_addresses_query, \
           entity_incoming_relations_query, \
           entity_outgoing_relations_query, \
           entity_query, entity_tags_query, keyspace_mapping, \
           exchange_rate_for_height_query, exchange_rates_query, \
           last_height, session, statistics_query, transaction_search_query, \
           tx_query, txs_query, label_search_query, label_query, tags_query

    cluster = cassandra.cluster.Cluster(app.config["CASSANDRA_NODES"])
    app.logger.debug("Created new Cassandra cluster.")

    # set the first keyspace in mapping to the default in order to be able to
    # create the prepared statements; alternative strategy is to not use
    # prepared statements and specify the keyspace in the query string
    keyspace_mapping = app.config["MAPPING"]
    if "tagpacks" in keyspace_mapping.keys() and keyspace_mapping["tagpacks"] == "tagpacks":
        keyspace_name = "tagpacks"  # it must be "tagpacks"
    else:
        abort(404, "Tagpacks keyspace missing")

    session = cluster.connect(keyspace_mapping[keyspace_name])
    session.default_fetch_size = 10
    app.logger.debug("Created new Cassandra session.")
    label_search_query = session.prepare("SELECT label,label_norm FROM tag_by_label WHERE label_norm_prefix = ? GROUP BY label_norm_prefix, label_norm")
    label_query = session.prepare("SELECT label_norm, label_norm_prefix, label, COUNT(address) as address_count FROM tag_by_label WHERE label_norm_prefix = ? and label_norm = ? GROUP BY label_norm_prefix, label_norm")
    tags_query = session.prepare("SELECT * FROM tag_by_label WHERE label_norm_prefix = ? and label_norm = ?")
    for keyspace_name in keyspace_mapping.keys():
        if keyspace_name == "tagpacks":
            continue
        set_keyspace(session, keyspace_name)
        address_query[keyspace_name] = session.prepare("SELECT * FROM address WHERE address = ? AND address_prefix = ?")
        address_search_query[keyspace_name] = session.prepare("SELECT address FROM address WHERE address_prefix = ?")
        address_transactions_query[keyspace_name] = session.prepare("SELECT * FROM address_transactions WHERE address = ? AND address_prefix = ? LIMIT ?")
        address_transactions_without_limit_query[keyspace_name] = session.prepare("SELECT * FROM address_transactions WHERE address = ? AND address_prefix = ?")
        address_tags_query[keyspace_name] = session.prepare("SELECT * FROM address_tags WHERE address = ?")
        address_entity_query[keyspace_name] = session.prepare("SELECT cluster FROM address_cluster WHERE address = ? AND address_prefix = ?")
        address_incoming_relations_query[keyspace_name] = session.prepare("SELECT * FROM address_incoming_relations WHERE dst_address_prefix = ? AND dst_address = ? LIMIT ?")
        address_incoming_relations_without_limit_query[keyspace_name] = session.prepare("SELECT * FROM address_incoming_relations WHERE dst_address_prefix = ? AND dst_address = ?")
        address_outgoing_relations_query[keyspace_name] = session.prepare("SELECT * FROM address_outgoing_relations WHERE src_address_prefix = ? AND src_address = ? LIMIT ?")
        address_outgoing_relations_without_limit_query[keyspace_name] = session.prepare("SELECT * FROM address_outgoing_relations WHERE src_address_prefix = ? AND src_address = ?")
        entity_incoming_relations_query[keyspace_name] = session.prepare("SELECT * FROM cluster_incoming_relations WHERE dst_cluster = ? LIMIT ?")
        entity_incoming_relations_without_limit_query[keyspace_name] = session.prepare("SELECT * FROM cluster_incoming_relations WHERE dst_cluster = ?")
        entity_outgoing_relations_query[keyspace_name] = session.prepare("SELECT * FROM cluster_outgoing_relations WHERE src_cluster = ? LIMIT ?")
        entity_outgoing_relations_without_limit_query[keyspace_name] = session.prepare("SELECT * FROM cluster_outgoing_relations WHERE src_cluster = ?")
        entity_tags_query[keyspace_name] = session.prepare("SELECT * FROM cluster_tags WHERE cluster = ?")
        entity_query[keyspace_name] = session.prepare("SELECT * FROM cluster WHERE cluster = ?")
        entity_addresses_query[keyspace_name] = session.prepare("SELECT * FROM cluster_addresses WHERE cluster = ? LIMIT ?")
        entity_addresses_without_limit_query[keyspace_name] = session.prepare("SELECT * FROM cluster_addresses WHERE cluster = ?")
        exchange_rates_query[keyspace_name] = session.prepare("SELECT * FROM exchange_rates LIMIT ?")
        exchange_rate_for_height_query[keyspace_name] = session.prepare("SELECT * FROM exchange_rates WHERE height = ?")
        last_block_height_query[keyspace_name] = session.prepare("SELECT no_blocks FROM summary_statistics")
        last_height[keyspace_name] = query_last_block_height(keyspace_name)
        all_exchange_rates[keyspace_name] = query_all_exchange_rates(keyspace_name,
                                                                     last_height[keyspace_name])
        statistics_query[keyspace_name] = session.prepare("SELECT * FROM summary_statistics LIMIT 1")

        set_keyspace(session, keyspace_name, space="raw")
        tx_query[keyspace_name] = session.prepare("SELECT * FROM transaction WHERE tx_prefix = ? AND tx_hash = ?")
        txs_query[keyspace_name] = session.prepare("SELECT * FROM transaction LIMIT ?")
        transaction_search_query[keyspace_name] = session.prepare("SELECT tx_hash from transaction where tx_prefix = ?")
        block_transactions_query[keyspace_name] = session.prepare("SELECT * FROM block_transactions WHERE height = ?")
        block_query[keyspace_name] = session.prepare("SELECT * FROM block WHERE height = ?")
        blocks_query[keyspace_name] = session.prepare("SELECT * FROM block LIMIT ?")

    app.logger.debug("Created prepared statements")
