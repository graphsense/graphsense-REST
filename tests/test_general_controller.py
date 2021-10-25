# coding: utf-8

import pytest
import json
from aiohttp import web

from openapi_server.models.search_result import SearchResult
from openapi_server.models.stats import Stats
from openapi_server.test import BaseTestCase
import gsrest.test.general_service as test_service


class TestGeneralController(BaseTestCase):
    """GeneralController integration test stubs"""

    async def test_get_statistics(self, client):
        """Test case for get_statistics

        Get statistics of supported currencies
        """
        await test_service.get_statistics(self)
        if 'get_statistics_sync' in dir(test_service):
            test_service.get_statistics_sync(self)

        if "get_statistics" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/stats',
            headers=headers,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_search(self, client):
        """Test case for search

        Returns matching addresses, transactions and labels
        """
        await test_service.search(self)
        if 'search_sync' in dir(test_service):
            test_service.search_sync(self)

        if "search" == "bulk":
            return
        params = [('currency', 'btc'),
                        ('q', 'foo'),
                        ('limit', 10)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/search',
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')

