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
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.get_statistics(self))
        loop.close()

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
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.search(self))
        loop.close()

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
