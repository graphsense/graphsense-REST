# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.address import Address  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.addresses_service as test_service


class TestAddressesController(BaseTestCase):
    """AddressesController integration test stubs"""

    def test_get_address_with_tags(self):
        """Test case for get_address_with_tags

        Get an address with tags
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}'.format(currency="btc", address="3Hrnn1UN78uXgLNvtqVXMjHwB41PmX66X4"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        test_service.get_address_with_tags(self)


if __name__ == '__main__':
    unittest.main()
