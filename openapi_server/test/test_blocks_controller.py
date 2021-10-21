# coding: utf-8

from __future__ import absolute_import
import unittest
import asyncio

from flask import json
from six import BytesIO

from openapi_server.models.block import Block  # noqa: E501
from openapi_server.models.tx import Tx  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.blocks_service as test_service


class TestBlocksController(BaseTestCase):
    """BlocksController integration test stubs"""

    def test_get_block(self):
        """Test case for get_block

        Get a block by its height
        """
        asyncio.run(test_service.get_block(self))
        if 'get_block_sync' in dir(test_service):
            test_service.get_block_sync(self)

        if "get_block" == "bulk":
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
        asyncio.run(test_service.list_block_txs(self))
        if 'list_block_txs_sync' in dir(test_service):
            test_service.list_block_txs_sync(self)

        if "list_block_txs" == "bulk":
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


if __name__ == '__main__':
    unittest.main()
