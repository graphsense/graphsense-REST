# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.address import Address  # noqa: E501
from openapi_server.models.address_tag import AddressTag  # noqa: E501
from openapi_server.models.address_txs import AddressTxs  # noqa: E501
from openapi_server.models.addresses import Addresses  # noqa: E501
from openapi_server.models.entity import Entity  # noqa: E501
from openapi_server.models.link import Link  # noqa: E501
from openapi_server.models.neighbors import Neighbors  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.addresses_service as test_service


class TestAddressesController(BaseTestCase):
    """AddressesController integration test stubs"""

    def test_get_address(self):
        """Test case for get_address

        Get an address, optionally with tags
        """
        test_service.get_address(self)

        query_string = [('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}'.format(currency='btc', address='1Archive1n2C579dMsAu3iC6tWzuQJz8dN'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_address_entity(self):
        """Test case for get_address_entity

        Get the entity of an address
        """
        test_service.get_address_entity(self)

        query_string = [('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/entity'.format(currency='btc', address='1Archive1n2C579dMsAu3iC6tWzuQJz8dN'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_address_links(self):
        """Test case for list_address_links

        Get transactions between two addresses
        """
        test_service.list_address_links(self)

        query_string = [('neighbor', '17DfZja1713S3JRWA9jaebCKFM5anUh7GG')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/links'.format(currency='btc', address='1Archive1n2C579dMsAu3iC6tWzuQJz8dN'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_address_links_csv(self):
        """Test case for list_address_links_csv

        Get transactions between two addresses as CSV
        """
        test_service.list_address_links_csv(self)

        query_string = [('neighbor', '17DfZja1713S3JRWA9jaebCKFM5anUh7GG')]
        headers = { 
            'Accept': 'text/csv',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/links.csv'.format(currency='btc', address='1Archive1n2C579dMsAu3iC6tWzuQJz8dN'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_address_neighbors(self):
        """Test case for list_address_neighbors

        Get an addresses' neighbors in the address graph
        """
        test_service.list_address_neighbors(self)

        query_string = [('direction', 'out'),
                        ('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/neighbors'.format(currency='btc', address='1Archive1n2C579dMsAu3iC6tWzuQJz8dN'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_address_neighbors_csv(self):
        """Test case for list_address_neighbors_csv

        Get an addresses' neighbors in the address graph as CSV
        """
        test_service.list_address_neighbors_csv(self)

        query_string = [('direction', 'out')]
        headers = { 
            'Accept': 'text/csv',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/neighbors.csv'.format(currency='btc', address='1Archive1n2C579dMsAu3iC6tWzuQJz8dN'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_address_txs(self):
        """Test case for list_address_txs

        Get all transactions an address has been involved in
        """
        test_service.list_address_txs(self)

        query_string = [('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/txs'.format(currency='btc', address='1Archive1n2C579dMsAu3iC6tWzuQJz8dN'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_address_txs_csv(self):
        """Test case for list_address_txs_csv

        Get all transactions an address has been involved in as CSV
        """
        test_service.list_address_txs_csv(self)

        headers = { 
            'Accept': 'text/csv',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/txs.csv'.format(currency='btc', address='1Archive1n2C579dMsAu3iC6tWzuQJz8dN'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_addresses(self):
        """Test case for list_addresses

        Get addresses
        """
        test_service.list_addresses(self)

        query_string = [('',''),
                        ('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses'.format(currency='btc'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_addresses_csv(self):
        """Test case for list_addresses_csv

        Get addresses as CSV
        """
        test_service.list_addresses_csv(self)

        query_string = [('ids', "1,2")]
        headers = { 
            'Accept': 'application/csv',
        }
        response = self.client.open(
            '/{currency}/addresses.csv'.format(currency='btc'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_tags_by_address(self):
        """Test case for list_tags_by_address

        Get attribution tags for a given address
        """
        test_service.list_tags_by_address(self)

        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/tags'.format(currency='btc', address='1Archive1n2C579dMsAu3iC6tWzuQJz8dN'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_tags_by_address_csv(self):
        """Test case for list_tags_by_address_csv

        Get attribution tags for a given address
        """
        test_service.list_tags_by_address_csv(self)

        headers = { 
            'Accept': 'application/csv',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/tags.csv'.format(currency='btc', address='1Archive1n2C579dMsAu3iC6tWzuQJz8dN'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
