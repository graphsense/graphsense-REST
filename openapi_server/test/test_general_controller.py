# coding: utf-8

from __future__ import absolute_import
import unittest
import asyncio

from flask import json
from six import BytesIO

from openapi_server.models.search_result import SearchResult  # noqa: E501
from openapi_server.models.stats import Stats  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.general_service as test_service


class TestGeneralController(BaseTestCase):
    """GeneralController integration test stubs"""

    def test_get_statistics(self):
        """Test case for get_statistics

        Get statistics of supported currencies
        """
        asyncio.run(test_service.get_statistics(self))
        if 'get_statistics_sync' in dir(test_service):
            test_service.get_statistics_sync(self)

        if "get_statistics" in ["batch", "get_tx_io"]:
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/stats',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search(self):
        """Test case for search

        Returns matching addresses, transactions and labels
        """
        asyncio.run(test_service.search(self))
        if 'search_sync' in dir(test_service):
            test_service.search_sync(self)

        if "search" in ["batch", "get_tx_io"]:
            return
        query_string = [('',''),
                        ('q', 'foo'),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/search',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
