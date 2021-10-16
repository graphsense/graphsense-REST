# coding: utf-8

from __future__ import absolute_import
import unittest
import asyncio

from flask import json
from six import BytesIO

from openapi_server.models.block import Block  # noqa: E501
from openapi_server.models.blocks import Blocks  # noqa: E501
from openapi_server.models.tx import Tx  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.blocks_service as test_service


class TestBlocksController(BaseTestCase):
    """BlocksController integration test stubs"""

    def test_get_block(self):
        """Test case for get_block

        Get a block by its height
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.get_block(self))
        loop.close()

        if "get_block" in ["batch", "get_tx_io"]:
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/blocks/{height}'.format(currency='btc', height=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_block_txs(self):
        """Test case for list_block_txs

        Get block transactions
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.list_block_txs(self))
        loop.close()

        if "list_block_txs" in ["batch", "get_tx_io"]:
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/blocks/{height}/txs'.format(currency='btc', height=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_blocks(self):
        """Test case for list_blocks

        Get all blocks
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.list_blocks(self))
        loop.close()

        if "list_blocks" in ["batch", "get_tx_io"]:
            return
        query_string = [('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/blocks'.format(currency='btc'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
