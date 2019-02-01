from graphsenserest import app
import graphsensedao as gd
import unittest
import json
from flask_cors import CORS

class FlaskBookshelfTests(unittest.TestCase):
    clusterId = 59468308
    address = '1Arch17xM2rBqDSLhPKc9WF9hnsuHbUiwB'
    txhash = 'd3ad39fa52a89997ac7381c95eeffeaf40b66af7a57e9eba144be0a175a12b11'
    @classmethod
    def setUpClass(cls):
        with open("./config.json", "r") as fp:
            config = json.load(fp)
        CORS(app)
        app.config.from_object(__name__)
        app.config.update(config)
        app.config.from_envvar("GRAPHSENSE_REST_SETTINGS", silent=True)
        currency_mapping = app.config["MAPPING"]
        gd.connect(app)
        #app.run(port=9000, debug=True, processes=1)
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    #def test_home_status_code(self):
    #    # sends HTTP GET request to the application
    #    # on the specified path
    #    result = self.app.get('/')

    #    # assert the status code of the response
    #    self.assertEqual(result.status_code, 200)

    def test_block(self):
        # sends HTTP GET request to the application
        #"/<currency>/block/<int:height>"
        result = self.app.get('/btc/block/10')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        # assert the response data
        response = result.json
        self.assertEqual(response['blockHash'], "000000002c05cc2e78923c34df87fd108b22221ac6076c18f3ade378a4d915e9")
        self.assertEqual(response['height'], 10)
        self.assertEqual(response['noTransactions'], 1)
        self.assertEqual(response['timestamp'], 1231473952)

    def test_block_transactions(self):
        # sends HTTP GET request to the application
        # "/<currency>/block/<int:height>/transactions"
        result = self.app.get('/btc/block/10/transactions')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        # assert the response data
        response = result.json
        self.assertEqual(response['height'], 10)
        self.assertEqual(len(response['txs']), 1)

        expected = [{'noInputs': 0, 'noOutputs': 1, 'totalInput': {'eur': 0.0, 'satoshi': 0, 'usd': 0.0},
                         'totalOutput': {'eur': 0.0, 'satoshi': 5000000000, 'usd': 0.0},
                         'txHash': '%s' % self.txhash}]
        self.assertEqual(response['txs'], expected)
        #self.assertEqual(response['height'], 10)

    def test_exchange_rates(self):
        #"/<currency>/exchangerates"
        result = self.app.get('/btc/exchangerates')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_blocks(self):
        #"/<currency>/blocks"
        result = self.app.get('/btc/blocks')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_tx_hash(self):
        # "/<currency>/tx/<txHash>"
        result = self.app.get('/btc/tx/%s' % self.txhash)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_search(self):
        #"/<currency>/search"
        result = self.app.get('/btc/search?q=1Arch')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_address(self):
        #"/<currency>/address/<address>"
        result = self.app.get('/btc/address/%s' % self.address)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_address_with_tags(self):
        #"/<currency>/address_with_tags/<address>"
        result = self.app.get('/btc/address_with_tags/%s' % self.address)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_address_transactions(self):
        #"/<currency>/address/<address>/transactions"
        result = self.app.get('/btc/address/%s/transactions' % self.address)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_address_tags(self):
        #"/<currency>/address/<address>/tags"
        result = self.app.get('/btc/address/%s/tags' % self.address)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_address_implicit_tags(self):
        # "/<currency>/address/<address>/implicitTags"
        result = self.app.get('/btc/address/%s/implicitTags' % self.address)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_address_cluster(self):
        # "/<currency>/address/<address>/cluster"
        result = self.app.get('/btc/address/%s/cluster' % self.address)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_address_cluster_with_tags(self):
        #"/<currency>/address/<address>/cluster_with_tags"
        result = self.app.get('/btc/address/%s/cluster_with_tags' % self.address)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_address_egonet(self):
        # "/<currency>/address/<address>/egonet"
        result = self.app.get('/btc/address/%s/egonet' % self.address)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_address_neighbours(self):
        #"/<currency>/address/<address>/neighbors"
        result = self.app.get('/btc/address/%s/neighbors?direction=in&pagesize=10&limit=10' % self.address)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_cluster(self):
        #"/<currency>/cluster/<cluster>"
        result = self.app.get('/btc/cluster/%s' % self.clusterId)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_cluster_with_tags(self):
        # "/<currency>/cluster_with_tags/<cluster>"
        result = self.app.get('/btc/cluster_with_tags/%s' % self.clusterId)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_cluster_tags(self):
        # "/<currency>/cluster/<cluster>/tags"
        result = self.app.get('/btc/cluster/%s/tags' % self.clusterId)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_cluster_addresses(self):
        # "/<currency>/cluster/<cluster>/addresses"
        result = self.app.get('/btc/cluster/%s/addresses' % self.clusterId)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_cluster_egonet(self):
        # "/<currency>/cluster/<cluster>/egonet"
        result = self.app.get('/btc/cluster/%s/egonet' % self.clusterId)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_cluster_neighbours(self):
        # "/<currency>/cluster/<cluster>/neighbors"
        result = self.app.get('/btc/cluster/%s/neighbors?direction=in&pagesize=10&limit=10' % self.clusterId)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

