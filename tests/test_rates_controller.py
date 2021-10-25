# coding: utf-8

import pytest
import json
from aiohttp import web

from openapi_server.models.rates import Rates
from openapi_server.test import BaseTestCase
import gsrest.test.rates_service as test_service


class TestRatesController(BaseTestCase):
    """RatesController integration test stubs"""

    async def test_get_exchange_rates(self, client):
        """Test case for get_exchange_rates

        Returns exchange rate for a given height
        """
        await test_service.get_exchange_rates(self)
        if 'get_exchange_rates_sync' in dir(test_service):
            test_service.get_exchange_rates_sync(self)

        if "get_exchange_rates" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/rates/{height}'.format(currency='btc', height=1),
            headers=headers,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')

