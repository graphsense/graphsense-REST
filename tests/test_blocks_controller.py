# coding: utf-8

import pytest
import json
from aiohttp import web
from aiohttp.test_utils import unittest_run_loop

from openapi_server.models.block import Block
from openapi_server.models.tx import Tx
from tests import BaseTestCase
import gsrest.test.blocks_service as test_service


class TestBlocksController(BaseTestCase):
    """BlocksController integration test stubs"""

    @unittest_run_loop
    async def test_get_block(self):
        """Test case for get_block

        Get a block by its height
        """
        await test_service.get_block(self)

        if "get_block" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = await self.client.request(
            method='GET',
            path='/{currency}/blocks/{height}'.format(currency='btc', height=1),
            headers=headers,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    @unittest_run_loop
    async def test_list_block_txs(self):
        """Test case for list_block_txs

        Get block transactions
        """
        await test_service.list_block_txs(self)

        if "list_block_txs" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = await self.client.request(
            method='GET',
            path='/{currency}/blocks/{height}/txs'.format(currency='btc', height=1),
            headers=headers,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')

