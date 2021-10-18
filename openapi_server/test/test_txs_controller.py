# coding: utf-8

from __future__ import absolute_import
import unittest
import asyncio

from flask import json
from six import BytesIO

from openapi_server.models.io import Io  # noqa: E501
from openapi_server.models.tx import Tx  # noqa: E501
from openapi_server.models.tx_value import TxValue  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.txs_service as test_service


class TestTxsController(BaseTestCase):
    """TxsController integration test stubs"""

    def test_get_tx(self):
        """Test case for get_tx

        Returns details of a specific transaction identified by its hash.
        """
        asyncio.run(test_service.get_tx(self))
        if 'get_tx_sync' in dir(test_service):
            test_service.get_tx_sync(self)

        if "get_tx" in ["batch", "get_tx_io"]:
            return
        query_string = [('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/txs/{tx_hash}'.format(currency='btc', tx_hash='ab188013'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_tx_io(self):
        """Test case for get_tx_io

        Returns input/output values of a specific transaction identified by its hash.
        """
        asyncio.run(test_service.get_tx_io(self))
        if 'get_tx_io_sync' in dir(test_service):
            test_service.get_tx_io_sync(self)

        if "get_tx_io" in ["batch", "get_tx_io"]:
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/txs/{tx_hash}/{io}'.format(currency='btc', tx_hash='ab188013', io=openapi_server.Io()),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
