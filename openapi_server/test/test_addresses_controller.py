# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.address_txs import AddressTxs  # noqa: E501
from openapi_server.models.address_with_tags import AddressWithTags  # noqa: E501
from openapi_server.models.tag import Tag  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.addresses_service as test_service


class TestAddressesController(BaseTestCase):
    """AddressesController integration test stubs"""

    def test_get_address_with_tags(self):
        """Test case for get_address_with_tags

        Get an address with tags
        """
        test_service.get_address_with_tags(self)

        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}'.format(currency="btc", address="3Hrnn1UN78uXgLNvtqVXMjHwB41PmX66X4"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_address_tags(self):
        """Test case for list_address_tags

        Get attribution tags for a given address
        """
        test_service.list_address_tags(self)

        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/tags'.format(currency="btc", address="3Hrnn1UN78uXgLNvtqVXMjHwB41PmX66X4"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_address_tags_csv(self):
        """Test case for list_address_tags_csv

        Get attribution tags for a given address
        """
        test_service.list_address_tags_csv(self)

        headers = { 
            'Accept': 'application/csv',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/tags.csv'.format(currency="btc", address="3Hrnn1UN78uXgLNvtqVXMjHwB41PmX66X4"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_address_txs(self):
        """Test case for list_address_txs

        Get all transactions an address has been involved in
        """
        test_service.list_address_txs(self)

        query_string = [('page', ''),
                        ('pagesize', '10')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/txs'.format(currency="btc", address="3Hrnn1UN78uXgLNvtqVXMjHwB41PmX66X4"),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))



if __name__ == '__main__':
    unittest.main()
