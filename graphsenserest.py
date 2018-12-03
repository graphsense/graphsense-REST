from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import graphsensedao as gd
import graphsensemodel as gm
import json

with open("./config.json", "r") as fp:
    config = json.load(fp)

app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)
app.config.update(config)
app.config.from_envvar("GRAPHSENSE_REST_SETTINGS", silent=True)
currency_mapping = app.config["MAPPING"]


@app.route("/")
def index():
    statistics = dict()
    for currency in currency_mapping.keys():
        if len(currency.split("_")) == 1:
            statistics[currency] = gd.query_statistics(currency)
    return jsonify(statistics)


@app.route("/<currency>/exchangerates")
def exchange_rates(currency):
    manual_limit = 100000
    limit = request.args.get("limit")
    offset = request.args.get("offset")
    if offset and not isinstance(offset, int):
        abort(404, "Invalid offset")
    if limit and (not isinstance(offset, int) or limit > manual_limit):
        abort(404, "Invalid limit")

    exchange_rates = gd.query_exchange_rates(currency, offset, limit)
    return jsonify({
        "exchangeRates": exchange_rates
    })


@app.route("/<currency>/block/<int:height>")
def block(currency, height):
    block = gd.query_block(currency, height)
    if not block:
        abort(404, "Block height %d not found" % height)
    return jsonify(block)


@app.route("/<currency>/block/<int:height>/transactions")
def block_transactions(currency, height):
    block_transactions = gd.query_block_transactions(currency, height)
    if not block_transactions:
        abort(404, "Block height %d not found" % height)
    return jsonify(block_transactions)


@app.route("/<currency>/blocks")
def blocks(currency):
    page_state = request.args.get("page")
    (page_state, blocks) = gd.query_blocks(currency, page_state)
    return jsonify({
        "nextPage": page_state.hex() if page_state is not None else None,
        "blocks": blocks
    })


@app.route("/<currency>/tx/<txHash>")
def transaction(currency, txHash):
    transaction = gd.query_transaction(currency, txHash)
    if not transaction:
        abort(404, "Transaction id %s not found" % txHash)
    return jsonify(transaction)


@app.route("/<currency>/transactions")
def transactions(currency):
    page_state = request.args.get("page")
    (page_state, transactions) = gd.query_transactions(currency, page_state)
    return jsonify({
        "nextPage": page_state.hex() if page_state is not None else None,
        "transactions": transactions
    })


@app.route("/<currency>/search")
def search(currency):
    expression = request.args.get("q")
    if not expression:
        abort(404, "Expression parameter not provided")
    leading_zeros = 0
    pos = 0
    # leading zeros will be lost when casting to int
    while expression[pos] == "0":
        pos += 1
        leading_zeros += 1
    limit = request.args.get("limit")
    if not limit:
        limit = 50
    else:
        try:
            limit = int(limit)
        except Exception:
            abort(404, "Invalid limit value")
    if len(expression) >= 5:
        prefix = expression[:5]
    else:
        # returns an empty list because the user did not input enough chars
        prefix = expression
    # no limit here, else we miss the specified transaction
    transactions = gd.query_transaction_search(currency, prefix)
    # no limit here, else we miss the specified address
    addresses = gd.query_address_search(currency, prefix)

    return jsonify({
        "addresses": [row.address for row in addresses.current_rows
                      if row.address.startswith(expression)][:limit],
        "transactions": [tx for tx in ["0"*leading_zeros + str(hex(int.from_bytes(row.tx_hash, byteorder="big")))[2:]
                                       for row in transactions.current_rows] if tx.startswith(expression)][:limit]
    })


@app.route("/<currency>/address/<address>")
def address(currency, address):
    if not address:
        abort(404, "Address not provided")

    result = gd.query_address(currency, address)
    return jsonify(result.__dict__) if result else jsonify({})


@app.route("/<currency>/address/<address>/transactions")
def address_transactions(currency, address):
    if not address:
        abort(404, "Address not provided")
    limit = request.args.get("limit")
    if not limit:
        limit = 100
    else:
        try:
            limit = int(limit)
        except Exception:
            abort(404, "Invalid limit value")
    rows = gd.query_address_transactions(currency, address, limit)
    txs = [gm.AddressTransactions(row, gd.query_exchange_rate_for_height(currency, row.height)).__dict__ for row in rows]
    return jsonify(txs)


@app.route("/<currency>/address/<address>/tags")
def address_tags(currency, address):
    if not address:
        abort(404, "Address not provided")

    tags = gd.query_address_tags(currency, address)
    return jsonify(tags)


@app.route("/<currency>/address/<address>/implicitTags")
def address_implicit_tags(currency, address):
    if not address:
        abort(404, "Address not provided")

    implicit_tags = gd.query_implicit_tags(currency, address)
    return jsonify(implicit_tags)


@app.route("/<currency>/address/<address>/cluster")
def address_cluster(currency, address):
    if not address:
        abort(404, "Address not provided")

    address_cluster = gd.query_address_cluster(currency, address)
    return jsonify(address_cluster)


@app.route("/<currency>/address/<address>/egonet")
def address_egonet(currency, address):
    direction = request.args.get("direction")
    if not direction:
        direction = ""

    limit = request.args.get("limit")
    if not limit:
        limit = 50
    else:
        limit = int(limit)
    try:
        egoNet = gm.AddressEgoNet(
            gd.query_address(currency, address),
            gd.query_address_tags(currency, address),
            gd.query_implicit_tags(currency, address),
            gd.query_address_incoming_relations(currency, address, int(limit)),
            gd.query_address_outgoing_relations(currency, address, int(limit))
        )
        ret = egoNet.construct(address, direction)
    except Exception:
        ret = {}
    return jsonify(ret)


@app.route("/<currency>/cluster/<cluster>")
def cluster(currency, cluster):
    if not cluster:
        abort(404, "Cluster not provided")
    try:
        cluster = int(cluster)
    except Exception:
        abort(404, "Invalid cluster ID")
    cluster_obj = gd.query_cluster(currency, cluster)
    return jsonify(cluster_obj.__dict__) if cluster_obj else jsonify({})


@app.route("/<currency>/cluster/<cluster>/tags")
def cluster_tags(currency, cluster):
    if not cluster:
        abort(404, "Cluster not provided")
    try:
        cluster = int(cluster)
    except Exception:
        abort(404, "Invalid cluster ID")
    tags = gd.query_cluster_tags(currency, cluster)
    return jsonify(tags)


@app.route("/<currency>/cluster/<cluster>/addresses")
def cluster_addresses(currency, cluster):
    if not cluster:
        abort(404, "Cluster not provided")
    try:
        cluster = int(cluster)
    except Exception:
        abort(404, "Invalid cluster ID")
    limit = request.args.get("limit")
    if not limit:
        limit = 100
    else:
        try:
            limit = int(limit)
        except Exception:
            abort(404, "Invalid limit value")
    addresses = gd.query_cluster_addresses(currency, cluster, int(limit))
    return jsonify(addresses)


@app.route("/<currency>/cluster/<cluster>/egonet")
def cluster_egonet(currency, cluster):
    direction = request.args.get("direction")
    if not cluster:
        abort(404, "Cluster not provided")
    try:
        cluster = int(cluster)
        cluster = str(cluster)
    except Exception:
        abort(404, "Invalid cluster ID")
    if not direction:
        direction = ""
    limit = request.args.get("limit")
    if not limit:
        limit = 50
    else:
        try:
            limit = int(limit)
        except Exception:
            abort(404, "Invalid limit value")
    try:
        egoNet = gm.ClusterEgoNet(
            gd.query_cluster(currency, cluster),
            gd.query_cluster_tags(currency, cluster),
            gd.query_cluster_incoming_relations(currency, cluster, int(limit)),
            gd.query_cluster_outgoing_relations(currency, cluster, int(limit))
        )
        ret = egoNet.construct(cluster, direction)
    except Exception:
        ret = {}
    return jsonify(ret)


@app.errorhandler(400)
def custom400(error):
    return jsonify({"message": error.description})


if __name__ == "__main__":
    gd.connect(app)
    app.run(port=9000, debug=True, processes=1)
