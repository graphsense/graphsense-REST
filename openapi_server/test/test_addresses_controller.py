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
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.get_address(self))
        loop.close()

        if "get_address" in ["batch", "get_tx_io"]:
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
        test_service.get_address_entity(self)

        if "get_address_entity" in ["batch", "get_tx_io"]:
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

        Get transactions between two addresses
        """
        test_service.list_address_links(self)

        if "list_address_links" in ["batch", "get_tx_io"]:
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
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.list_address_neighbors(self))
        loop.close()

        if "list_address_neighbors" in ["batch", "get_tx_io"]:
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
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.list_address_txs(self))
        loop.close()

        if "list_address_txs" in ["batch", "get_tx_io"]:
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
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.list_tags_by_address(self))
        loop.close()

        if "list_tags_by_address" in ["batch", "get_tx_io"]:
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
