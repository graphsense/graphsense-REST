# coding: utf-8

import pytest
import json
from aiohttp import web

from openapi_server.models.tx import Tx
from openapi_server.models.tx_value import TxValue
from openapi_server.test import BaseTestCase
import gsrest.test.txs_service as test_service


class TestTxsController(BaseTestCase):
    """TxsController integration test stubs"""

    async def test_get_tx(self, client):
        """Test case for get_tx

        Returns details of a specific transaction identified by its hash.
        """
        await test_service.get_tx(self)
        if 'get_tx_sync' in dir(test_service):
            test_service.get_tx_sync(self)

        if "get_tx" == "bulk":
            return
        params = [('include_io', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/txs/{tx_hash}'.format(currency='btc', tx_hash='ab188013'),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_get_tx_io(self, client):
        """Test case for get_tx_io

        Returns input/output values of a specific transaction identified by its hash.
        """
        await test_service.get_tx_io(self)
        if 'get_tx_io_sync' in dir(test_service):
            test_service.get_tx_io_sync(self)

        if "get_tx_io" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/txs/{tx_hash}/{io}'.format(currency='btc', tx_hash='ab188013', io='outputs'),
            headers=headers,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')

