# https://datastax.github.io/python-driver/
# https://speakerdeck.com/mitsuhiko/advanced-flask-patterns-1

# https://github.com/TerbiumLabs/flask-cassandra/blob/master/flask_cassandra.py
# https://github.com/tiangolo/uwsgi-nginx-flask-docker

from flask import Flask, jsonify, request, g, abort
from flask_cors import CORS
from graphsensedao import *

app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY='development key',
    CASSANDRA_NODES=['spark1', 'spark2'],
    MAPPING={'btc': 'btc_transformed_20180831',
             'ltc': 'ltc_transformed_20180430'}
))
app.config.from_envvar('GRAPHSENSE_REST_SETTINGS', silent=True)
currency_mapping = app.config['MAPPING']


@app.route('/')
def index():
    return "Graphsense REST"

@app.route('/<currency>/exchangerates')
def exchange_rates(currency):
    page_state = request.args.get('page')
    (page_state, exchange_rates) = query_exchange_rates(currency, page_state)
    return jsonify({
        "nextPage": page_state.hex() if page_state is not None else None,
        "exchangeRates": exchange_rates
    })

@app.route('/<currency>/block/<int:height>')
def block(currency, height):
    block = query_block(currency, height)
    if not block:
        abort(404, "Block height %d not found" % height)
    return jsonify(block)

@app.route('/<currency>/block/<int:height>/transactions')
def block_transactions(currency, height):
    block_transactions = query_block_transactions(currency, height)
    if not block_transactions:
        abort(404, "Block height %d not found" % height)
    return jsonify(block_transactions)

@app.route('/<currency>/blocks')
def blocks(currency):
    page_state = request.args.get('page')
    (page_state, blocks) = query_blocks(currency, page_state)
    return jsonify({
        "nextPage": page_state.hex() if page_state is not None else None,
        "blocks": blocks
    })

@app.route('/<currency>/tx/<txHash>')
def transaction(currency, txHash):
    transaction = query_transaction(currency, txHash)
    if not transaction:
        abort(404, "Transaction id %s not found" % txHash)
    return jsonify(transaction)

@app.route('/<currency>/transactions')
def transactions(currency):
    page_state = request.args.get('page')
    (page_state, transactions) = query_transactions(currency, page_state)
    return jsonify({
        "nextPage": page_state.hex() if page_state is not None else None,
        "transactions": transactions
    })

@app.route('/<currency>/search')
def search(currency):
    expression = request.args.get('q')
    if not expression:
        abort(404, "Expression parameter not provided")

    limit = request.args.get('limit')
    if not limit:
        limit = 50
    else:
        try:
            limit = int(limit)
        except:
            abort(404, 'Invalid limit value')
    if len(expression) >= 5:
        prefix = expression[:5]
    else:
        prefix = expression  # this will return an empty list because the user did not input enough chars
    transactions = query_transaction_search(currency, prefix)  # no limit here, else we miss the specified transaction
    addresses = query_address_search(currency, prefix)  # no limit here, else we miss the specified address
    return jsonify({
        'addresses': [row.address for row in addresses.current_rows if row.address.startswith(expression)][:limit],
        'transactions': [tx for tx in [str(hex(int.from_bytes(row.tx_hash, byteorder='big')))[2:]
                                       for row in transactions.current_rows] if tx.startswith(expression)][:limit]
    })

@app.route('/<currency>/address/<address>')
def address(currency, address):
    if not address:
        abort(404, "Address not provided")

    result = query_address(currency, address)
    return jsonify(result.__dict__) if result else jsonify({})

@app.route('/<currency>/address/<address>/transactions')
def address_transactions(currency, address):
    if not address:
        abort(404, "Address not provided")
    limit = request.args.get('limit')
    if not limit:
        limit = 100
    else:
        try:
            limit = int(limit)
        except:
            abort(404, 'Invalid limit value')
    rows = query_address_transactions(currency, address, limit)
    txs = [AddressTransactions(row, query_exchange_rate_for_height(currency, row.height)).__dict__ for row in rows]
    return jsonify(txs)

@app.route('/<currency>/address/<address>/tags')
def address_tags(currency, address):
    if not address:
        abort(404, "Address not provided")

    tags = query_address_tags(currency, address)
    return jsonify(tags)

@app.route('/<currency>/address/<address>/implicitTags')
def address_implicit_tags(currency, address):
    if not address:
        abort(404, "Address not provided")

    implicit_tags = query_implicit_tags(currency, address)
    return jsonify(implicit_tags)

@app.route('/<currency>/address/<address>/cluster')
def address_cluster(currency, address):
    if not address:
        abort(404, "Address not provided")

    address_cluster = query_address_cluster(currency, address)
    return jsonify(address_cluster)

@app.route('/<currency>/address/<address>/egonet')
def address_egonet(currency, address):
    direction = request.args.get('direction')
    if not direction:
        direction = ""

    limit = request.args.get('limit')
    if not limit:
        limit = 50
    else:
        limit = int(limit)
    try:
        egoNet = AddressEgoNet(
            query_address(currency, address),
            query_address_tags(currency, address),
            query_implicit_tags(currency, address),
            query_address_incoming_relations(currency, address, int(limit)),
            query_address_outgoing_relations(currency, address, int(limit))
        )
        ret = egoNet.construct(address, direction)
    except:
        ret = {}
    return jsonify(ret)

@app.route('/<currency>/cluster/<cluster>')
def cluster(currency, cluster):
    if not cluster:
        abort(404, "Cluster id not provided")
    cluster_obj = query_cluster(currency, cluster)
    return jsonify(cluster_obj.__dict__) if cluster_obj else jsonify({})

@app.route('/<currency>/cluster/<cluster>/tags')
def cluster_tags(currency, cluster):
    if not cluster:
        abort(404, "Cluster id not provided")
    tags = query_cluster_tags(currency, cluster)
    return jsonify(tags)

@app.route('/<currency>/cluster/<cluster>/addresses')
def cluster_addresses(currency, cluster):
    if not cluster:
        abort(404, "Cluster id not provided")
    limit = request.args.get('limit')
    if not limit:
        limit = 100
    else:
        try:
            limit = int(limit)
        except:
            abort(404, 'Invalid limit value')
    addresses = query_cluster_addresses(currency, cluster, int(limit))
    return jsonify(addresses)


@app.route('/<currency>/cluster/<cluster>/egonet')
def cluster_egonet(currency, cluster):
    direction = request.args.get('direction')
    if not direction:
        direction = ""
    limit = request.args.get('limit')
    if not limit:
        limit = 50
    else:
        try:
            limit = int(limit)
        except:
            abort(404, 'Invalid limit value')
    try:
        egoNet = ClusterEgoNet(
            query_cluster(currency, cluster),
            query_cluster_tags(currency, cluster),
            query_cluster_incoming_relations(currency, cluster, int(limit)),
            query_cluster_outgoing_relations(currency, cluster, int(limit))
        )
        ret = egoNet.construct(cluster, direction)
    except:
        ret = {}
    return jsonify(ret)

@app.errorhandler(400)
def custom400(error):
    return jsonify({'message': error.description})

if __name__ == '__main__':
    connect(app)
    app.run(port=9000, debug=True, processes=1)

# @app.teardown_appcontext
# def cluster_shutdown(error):
#     """Shutdown all connections to cassandra."""
#     app.logger.debug("Shutting down Cassandra cluster.")
#     app.cluster.shutdown()
