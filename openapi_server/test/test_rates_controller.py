# coding: utf-8

from __future__ import absolute_import
import unittest
import asyncio

from flask import json
from six import BytesIO

from openapi_server.models.rates import Rates  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.rates_service as test_service


class TestRatesController(BaseTestCase):
    """RatesController integration test stubs"""

    def test_get_exchange_rates(self):
        """Test case for get_exchange_rates

        Returns exchange rate for a given height
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.get_exchange_rates(self))
        loop.close()

        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/rates/{height}'.format(currency='btc', height=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
