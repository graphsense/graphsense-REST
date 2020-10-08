# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.stats import Stats  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.general_service as test_service


class TestGeneralController(BaseTestCase):
    """GeneralController integration test stubs"""

    def test_get_statistics(self):
        """Test case for get_statistics

        Get statistics of supported currencies
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/stats',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        test_service.get_statistics(self)


if __name__ == '__main__':
    unittest.main()
