# coding: utf-8

import pytest
import json
from aiohttp import web
from aiohttp.test_utils import unittest_run_loop

from openapi_server.models.tx import Tx
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.tx_value import TxValue
from tests import BaseTestCase
import gsrest.test.txs_service as test_service


class TestTxsController(BaseTestCase):
    """TxsController integration test stubs"""

    async def test_get_tx(self):
        """Test case for get_tx

        Returns details of a specific transaction identified by its hash.
        """
        await test_service.get_tx(self)


    async def test_get_tx_io(self):
        """Test case for get_tx_io

        Returns input/output values of a specific transaction identified by its hash.
        """
        await test_service.get_tx_io(self)


    async def test_list_token_txs(self):
        """Test case for list_token_txs

        Returns all token transactions in a given transaction
        """
        await test_service.list_token_txs(self)

