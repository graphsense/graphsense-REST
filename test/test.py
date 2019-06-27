from graphsenserest import app
import graphsensedao as gd
import unittest
import json
from flask_cors import CORS
from requests.auth import _basic_auth_str

class FlaskBookshelfTests(unittest.TestCase):
    clusterId = 59468308
    address = '1Arch17xM2rBqDSLhPKc9WF9hnsuHbUiwB'
    txhash = 'd3ad39fa52a89997ac7381c95eeffeaf40b66af7a57e9eba144be0a175a12b11'
    label = 'coinapultcom'
    headers = {'X-API-KEY': 'mytoken',
               # 'content-type': 'application/json'
               }

    @classmethod
    def setUpClass(cls):
        with open("./config.json", "r") as fp:
            config = json.load(fp)
        CORS(app)
        app.config.from_object(__name__)
        app.config.update(config)

        app.config.from_envvar("GRAPHSENSE_REST_SETTINGS", silent=True)
        keyspace_mapping = app.config["MAPPING"]
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

    def test_00_login(self):
        result = self.app.get('/login',
                              headers={"Authorization": _basic_auth_str('admin', 'test123')})
        # assert the status code of the response
        self.assertEqual(200, result.status_code)
        # assert the response data
        response = result.json
        self.assertTrue('access_token' in response)
        self.headers['access_token'] = response['access_token']
        self.headers['refresh_token'] = response['refresh_token']
        self.headers['Authorization'] = 'Bearer ' + self.headers['access_token']
        # self.headers['X-API-KEY'] = response['token']


    def test_01_refresh_token(self):
        # sends HTTP GET request to the application
        self.headers['Authorization'] = 'Bearer ' + self.headers['refresh_token']
        result = self.app.get('/token_refresh', headers=self.headers)
        # assert the status code of the response
        self.assertEqual(200, result.status_code)
        # assert the response data
        print(result.json)
        response = result.json
        self.assertTrue('access_token' in response)
        self.headers['access_token'] = response['access_token']
        self.headers['Authorization'] = 'Bearer ' + self.headers['access_token']
        # now test secret again


    def test_02_logout(self):
        # sends HTTP GET request to the application
        result = self.app.get('/logout_access', headers=self.headers)
        # assert the status code of the response
        self.assertEqual(200, result.status_code)
        # assert the response data


    def test_03_relogin(self):
        # sends HTTP GET request to the application
        result = self.app.get('/login',
                              headers={"Authorization": _basic_auth_str('admin', 'test123')})
        # assert the status code of the response
        self.assertEqual(200, result.status_code)
        # assert the response data
        response = result.json
        self.assertTrue('access_token' in response)
        self.headers['access_token'] = response['access_token']
        self.headers['refresh_token'] = response['refresh_token']
        self.headers['Authorization'] = 'Bearer ' + self.headers['access_token']


    def test_05_block(self):
        # sends HTTP GET request to the application
        #"/<currency>/block/<int:height>"
        result = self.app.get('/btc/block/10', headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        # assert the response data
        response = result.json
        self.assertEqual(response['blockHash'], "000000002c05cc2e78923c34df87fd108b22221ac6076c18f3ade378a4d915e9")
        self.assertEqual(response['height'], 10)
        self.assertEqual(response['noTransactions'], 1)
        self.assertEqual(response['timestamp'], 1231473952)


    def test_06_block_transactions(self):
        # sends HTTP GET request to the application
        # "/<currency>/block/<int:height>/transactions"
        result = self.app.get('/btc/block/10/transactions', headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        # assert the response data
        response = result.json
        print(response)
        self.assertEqual(response['height'], 10)
        self.assertEqual(len(response['txs']), 1)

        expected = [{'noInputs': 0, 'noOutputs': 1, 'totalInput': {'eur': 0.0, 'satoshi': 0, 'usd': 0.0},
                         'totalOutput': {'eur': 0.0, 'satoshi': 5000000000, 'usd': 0.0},
                         'txHash': '%s' % self.txhash}]
        self.assertEqual(response['txs'], expected)
        #self.assertEqual(response['height'], 10)


    def test_07_exchange_rates(self):
        #"/<currency>/exchangerates"
        result = self.app.get('/btc/exchangerates', headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_08_blocks(self):
        #"/<currency>/blocks"
        result = self.app.get('/btc/blocks', headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_09_tx_hash(self):
        # "/<currency>/tx/<txHash>"
        result = self.app.get('/btc/tx/%s' % self.txhash, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_10_search(self):
        #"/<currency>/search"
        response = self.app.get('/btc/search?q=%s' % self.address, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(response.status_code, 200)

        result = response.json
        self.assertTrue("addresses" in result.keys())
        self.assertTrue(type(result["addresses"]) is list)
        self.assertTrue("transactions" in result.keys())
        self.assertTrue(type(result["transactions"]) is list)
        print(result)


    def test_11_address(self):
        #"/<currency>/address/<address>"
        result = self.app.get('/btc/address/%s' % self.address, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_12_address_with_tags(self):
        #"/<currency>/address_with_tags/<address>"
        result = self.app.get('/btc/address_with_tags/%s' % self.address, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_13_address_transactions(self):
        #"/<currency>/address/<address>/transactions"
        result = self.app.get('/btc/address/%s/transactions' % self.address, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_14_address_tags(self):
        #"/<currency>/address/<address>/tags"
        result = self.app.get('/btc/address/%s/tags' % self.address, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_15_address_implicit_tags(self):
        # "/<currency>/address/<address>/implicitTags"
        result = self.app.get('/btc/address/%s/implicitTags' % self.address, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_16_address_cluster(self):
        # "/<currency>/address/<address>/cluster"
        result = self.app.get('/btc/address/%s/cluster' % self.address, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_17_address_cluster_with_tags(self):
        #"/<currency>/address/<address>/cluster_with_tags"
        result = self.app.get('/btc/address/%s/cluster_with_tags' % self.address, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_19_address_neighbours(self):
        #"/<currency>/address/<address>/neighbors"
        result = self.app.get('/btc/address/%s/neighbors?direction=in&pagesize=2&limit=10' % self.address, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


        result = self.app.get('/btc/address/%s/neighbors?direction=out&pagesize=2&limit=10' % self.address,headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_20_cluster(self):
        #"/<currency>/cluster/<cluster>"
        result = self.app.get('/btc/cluster/%s' % self.clusterId, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_21_cluster_with_tags(self):
        # "/<currency>/cluster_with_tags/<cluster>"
        result = self.app.get('/btc/cluster_with_tags/%s' % self.clusterId, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_22_cluster_tags(self):
        # "/<currency>/cluster/<cluster>/tags"
        result = self.app.get('/btc/cluster/%s/tags' % self.clusterId, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_23_cluster_addresses(self):
        # "/<currency>/cluster/<cluster>/addresses"
        result = self.app.get('/btc/cluster/%s/addresses' % self.clusterId, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_24_cluster_neighbours(self):
        # "/<currency>/cluster/<cluster>/neighbors"
        result = self.app.get('/btc/cluster/%s/neighbors?direction=in&pagesize=2&limit=10' % self.clusterId, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print(result.json)
        result = self.app.get('/btc/cluster/%s/neighbors?direction=out&pagesize=2&limit=10' % self.clusterId, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print(result.json)

    def test_25_block_transactions_csv(self):
        # sends HTTP GET request to the application
        # "/<currency>/block/<int:height>/transactions"
        result = self.app.get('/btc/block/10/transactions.csv', headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print(str(result.data, result.charset))


    def test_26_address_tags_csv(self):
        #"/<currency>/address/<address>/tags.csv"
        result = self.app.get('/btc/address/%s/tags.csv' % '1PUoHc5ncRsRpFavzQwPnDhqAkQ1SYFicR', headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print(str(result.data, result.charset))


    def test_27_cluster_tags_csv(self):
        #"/<currency>/cluster/<address>/tags.csv"
        result = self.app.get('/btc/cluster/%s/tags.csv' % '111857125', headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print(str(result.data, result.charset))


    def test_28_address_neighbours(self):
        #"/<currency>/address/<address>/neighbors"
        result = self.app.get('/btc/address/%s/neighbors.csv?direction=in&pagesize=2&limit=100' % self.address, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print(str(result.data, result.charset))
        result = self.app.get('/btc/address/%s/neighbors.csv?direction=out&pagesize=2&limit=100' % self.address, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print(str(result.data, result.charset))


    def test_29_cluster_neighbours(self):
        # "/<currency>/cluster/<cluster>/neighbors"
        result = self.app.get('/btc/cluster/%s/neighbors.csv?direction=in&pagesize=2&limit=100' % self.clusterId, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print(str(result.data, result.charset))
        result = self.app.get('/btc/cluster/%s/neighbors.csv?direction=out&pagesize=2&limit=100' % self.clusterId, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print(str(result.data, result.charset))


    def test_30_labelsearch(self):
        #"/labelsearch"
        result = self.app.get('/labelsearch?q=coi', headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print(result.json)


    # def test_31_label_addresses(self):
    #     #"/label/<label>/addresses"
    #     result = self.app.get('/label/%s/addresses' % self.label, headers=self.headers)
    #     # assert the status code of the response
    #     self.assertEqual(result.status_code, 200)
    #     print(result.json)


    def test_32_label(self):
        #"/label/<label>"
        result = self.app.get('/label/%s' % self.label, headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print(result.json)

    def test_33_swagger(self):
        #"/label/<label>"
        result = self.app.get('/swagger.json', headers=self.headers)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        print(result.json)







