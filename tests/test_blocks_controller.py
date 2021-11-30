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


    @unittest_run_loop
    async def test_list_block_txs(self):
        """Test case for list_block_txs

        Get block transactions
        """
        await test_service.list_block_txs(self)

