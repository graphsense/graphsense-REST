# coding: utf-8

from __future__ import absolute_import
import unittest
import asyncio

from flask import json
from six import BytesIO

from openapi_server.test import BaseTestCase
import gsrest.test.bulk_service as test_service


class TestBulkController(BaseTestCase):
    """BulkController integration test stubs"""

    def test_bulk(self):
        """Test case for bulk

        Get data as CSV or JSON in bulk
        """
        asyncio.run(test_service.bulk(self))
        if 'bulk_sync' in dir(test_service):
            test_service.bulk_sync(self)

        if "bulk" == "bulk":
            return
        body = None
        query_string = [('','')]
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{currency}/bulk/{api}/{operation}'.format(currency='btc', api='blocks', operation='get_block'),
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
