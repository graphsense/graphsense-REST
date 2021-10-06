# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.batch_operation import BatchOperation  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.batch_service as test_service


class TestBatchController(BaseTestCase):
    """BatchController integration test stubs"""

    def test_batch(self):
        """Test case for batch

        Get data as CSV in batch
        """
        test_service.batch(self)

        batch_operation = openapi_server.BatchOperation()
        headers = { 
            'Accept': 'text/csv',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/{currency}/batch'.format(currency='btc'),
            method='POST',
            headers=headers,
            data=json.dumps(batch_operation),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
