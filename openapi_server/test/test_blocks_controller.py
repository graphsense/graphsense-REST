# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.block import Block  # noqa: E501
from openapi_server.models.block_tx_summary import BlockTxSummary  # noqa: E501
from openapi_server.models.block_txs import BlockTxs  # noqa: E501
from openapi_server.models.blocks import Blocks  # noqa: E501
from openapi_server.test import BaseTestCase


class TestBlocksController(BaseTestCase):
    """BlocksController integration test stubs"""

    def test_get_block(self):
        """Test case for get_block

        Get a block by its height
        """
        headers = { 
            'Accept': 'application/json',
            'api_key': 'special-key',
        }
        response = self.client.open(
            '/{currency}/blocks/{height}'.format(currency=btc, height=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_block_txs(self):
        """Test case for list_block_txs

        Get all blocks (100 per page)
        """
        headers = { 
            'Accept': 'application/json',
            'api_key': 'special-key',
        }
        response = self.client.open(
            '/{currency}/blocks/{height}/txs'.format(currency=btc, height=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_block_txs_csv(self):
        """Test case for list_block_txs_csv

        Get all blocks as CSV
        """
        headers = { 
            'Accept': 'text/csv',
            'api_key': 'special-key',
        }
        response = self.client.open(
            '/{currency}/blocks/{height}/txs.csv'.format(currency=btc, height=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_blocks(self):
        """Test case for list_blocks

        Get all blocks
        """
        query_string = [('page', 'page_example')]
        headers = { 
            'Accept': 'application/json',
            'api_key': 'special-key',
        }
        response = self.client.open(
            '/{currency}/blocks'.format(currency=btc),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
