# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.tx import Tx  # noqa: E501
from openapi_server.models.txs import Txs  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.txs_service as test_service


class TestTxsController(BaseTestCase):
    """TxsController integration test stubs"""

    def test_get_tx(self):
        """Test case for get_tx

        Returns details of a specific transaction identified by its hash.
        """
        test_service.get_tx(self)

        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/txs/{tx_hash}'.format(currency="btc", tx_hash="ab188013"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_txs(self):
        """Test case for list_txs

        Returns transactions
        """
        test_service.list_txs(self)

        query_string = [('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/txs'.format(currency="btc"),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))



if __name__ == '__main__':
    unittest.main()
