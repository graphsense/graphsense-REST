# coding: utf-8

import pytest
import json
from aiohttp import web

from openapi_server.models.block import Block
from openapi_server.models.tx import Tx
from openapi_server.test import BaseTestCase
import gsrest.test.blocks_service as test_service


class TestBlocksController(BaseTestCase):
    """BlocksController integration test stubs"""

    async def test_get_block(self, client):
        """Test case for get_block

        Get a block by its height
        """
        await test_service.get_block(self)
        if 'get_block_sync' in dir(test_service):
            test_service.get_block_sync(self)

        if "get_block" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/blocks/{height}'.format(currency='btc', height=1),
            headers=headers,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_list_block_txs(self, client):
        """Test case for list_block_txs

        Get block transactions
        """
        await test_service.list_block_txs(self)
        if 'list_block_txs_sync' in dir(test_service):
            test_service.list_block_txs_sync(self)

        if "list_block_txs" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/blocks/{height}/txs'.format(currency='btc', height=1),
            headers=headers,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')

