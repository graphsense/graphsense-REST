# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.block import Block  # noqa: E501
from openapi_server.models.block_eth import BlockEth  # noqa: E501
from openapi_server.models.block_txs import BlockTxs  # noqa: E501
from openapi_server.models.blocks import Blocks  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.blocks_service as test_service


class TestBlocksController(BaseTestCase):
    """BlocksController integration test stubs"""

    def test_get_block(self):
        """Test case for get_block

        Get a block by its height
        """
        test_service.get_block(self)

        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/blocks/{height}'.format(currency="btc", height="1"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_get_block_eth(self):
        """Test case for get_block_eth

        Get a ethereum block by its height
        """
        test_service.get_block_eth(self)

        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/eth/blocks/{height}'.format(height="1"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_block_txs(self):
        """Test case for list_block_txs

        Get all blocks (100 per page)
        """
        test_service.list_block_txs(self)

        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/blocks/{height}/txs'.format(currency="btc", height="1"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_block_txs_csv(self):
        """Test case for list_block_txs_csv

        Get all blocks as CSV
        """
        test_service.list_block_txs_csv(self)

        headers = { 
            'Accept': 'text/csv',
        }
        response = self.client.open(
            '/{currency}/blocks/{height}/txs.csv'.format(currency="btc", height="1"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_blocks(self):
        """Test case for list_blocks

        Get all blocks
        """
        test_service.list_blocks(self)

        query_string = [('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/blocks'.format(currency="btc"),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))



if __name__ == '__main__':
    unittest.main()
