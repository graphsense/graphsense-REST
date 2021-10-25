# coding: utf-8

import pytest
import json
from aiohttp import web

from openapi_server.test import BaseTestCase
import gsrest.test.bulk_service as test_service


class TestBulkController(BaseTestCase):
    """BulkController integration test stubs"""

    async def test_bulk(self, client):
        """Test case for bulk

        Get data as CSV or JSON in bulk
        """
        await test_service.bulk(self)
        if 'bulk_sync' in dir(test_service):
            test_service.bulk_sync(self)

        if "bulk" == "bulk":
            return
        body = None
        params = [('form', 'csv')]
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = await client.request(
            method='POST',
            path='/{currency}/bulk/{api}/{operation}'.format(currency='btc', api='blocks', operation='get_block'),
            headers=headers,
            json=body,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')

