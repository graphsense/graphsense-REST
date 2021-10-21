# coding: utf-8

from __future__ import absolute_import
import unittest
import asyncio

from flask import json
from six import BytesIO

from openapi_server.models.address import Address  # noqa: E501
from openapi_server.models.address_tag import AddressTag  # noqa: E501
from openapi_server.models.address_txs import AddressTxs  # noqa: E501
from openapi_server.models.entity import Entity  # noqa: E501
from openapi_server.models.links import Links  # noqa: E501
from openapi_server.models.neighbors import Neighbors  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.addresses_service as test_service


class TestAddressesController(BaseTestCase):
    """AddressesController integration test stubs"""

    def test_get_address(self):
        """Test case for get_address

        Get an address, optionally with tags
        """
        asyncio.run(test_service.get_address(self))
        if 'get_address_sync' in dir(test_service):
            test_service.get_address_sync(self)

        if "get_address" == "bulk":
            return
        query_string = [('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}'.format(currency='btc', address='addressA'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_address_entity(self):
        """Test case for get_address_entity

        Get the entity of an address
        """
        asyncio.run(test_service.get_address_entity(self))
        if 'get_address_entity_sync' in dir(test_service):
            test_service.get_address_entity_sync(self)

        if "get_address_entity" == "bulk":
            return
        query_string = [('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/entity'.format(currency='btc', address='addressA'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_address_links(self):
        """Test case for list_address_links

        Get outgoing transactions between two addresses
        """
        asyncio.run(test_service.list_address_links(self))
        if 'list_address_links_sync' in dir(test_service):
            test_service.list_address_links_sync(self)

        if "list_address_links" == "bulk":
            return
        query_string = [('neighbor', 'addressE')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/links'.format(currency='btc', address='addressA'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_address_neighbors(self):
        """Test case for list_address_neighbors

        Get an addresses' neighbors in the address graph
        """
        asyncio.run(test_service.list_address_neighbors(self))
        if 'list_address_neighbors_sync' in dir(test_service):
            test_service.list_address_neighbors_sync(self)

        if "list_address_neighbors" == "bulk":
            return
        query_string = [('direction', 'out'),
                        ('',''),
                        ('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/neighbors'.format(currency='btc', address='addressA'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_address_txs(self):
        """Test case for list_address_txs

        Get all transactions an address has been involved in
        """
        asyncio.run(test_service.list_address_txs(self))
        if 'list_address_txs_sync' in dir(test_service):
            test_service.list_address_txs_sync(self)

        if "list_address_txs" == "bulk":
            return
        query_string = [('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/txs'.format(currency='btc', address='addressA'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_tags_by_address(self):
        """Test case for list_tags_by_address

        Get attribution tags for a given address
        """
        asyncio.run(test_service.list_tags_by_address(self))
        if 'list_tags_by_address_sync' in dir(test_service):
            test_service.list_tags_by_address_sync(self)

        if "list_tags_by_address" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/addresses/{address}/tags'.format(currency='btc', address='addressA'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
