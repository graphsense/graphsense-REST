# coding: utf-8

import pytest
import json
from aiohttp import web

from openapi_server.models.address import Address
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.entity import Entity
from openapi_server.models.links import Links
from openapi_server.models.neighbors import Neighbors
from openapi_server.test import BaseTestCase
import gsrest.test.addresses_service as test_service


class TestAddressesController(BaseTestCase):
    """AddressesController integration test stubs"""

    async def test_get_address(self, client):
        """Test case for get_address

        Get an address, optionally with tags
        """
        await test_service.get_address(self)
        if 'get_address_sync' in dir(test_service):
            test_service.get_address_sync(self)

        if "get_address" == "bulk":
            return
        params = [('include_tags', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/addresses/{address}'.format(currency='btc', address='addressA'),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_get_address_entity(self, client):
        """Test case for get_address_entity

        Get the entity of an address
        """
        await test_service.get_address_entity(self)
        if 'get_address_entity_sync' in dir(test_service):
            test_service.get_address_entity_sync(self)

        if "get_address_entity" == "bulk":
            return
        params = [('include_tags', False),
                        ('tag_coherence', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/addresses/{address}/entity'.format(currency='btc', address='addressA'),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_list_address_links(self, client):
        """Test case for list_address_links

        Get outgoing transactions between two addresses
        """
        await test_service.list_address_links(self)
        if 'list_address_links_sync' in dir(test_service):
            test_service.list_address_links_sync(self)

        if "list_address_links" == "bulk":
            return
        params = [('neighbor', 'addressE')]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/addresses/{address}/links'.format(currency='btc', address='addressA'),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_list_address_neighbors(self, client):
        """Test case for list_address_neighbors

        Get an addresses' neighbors in the address graph
        """
        await test_service.list_address_neighbors(self)
        if 'list_address_neighbors_sync' in dir(test_service):
            test_service.list_address_neighbors_sync(self)

        if "list_address_neighbors" == "bulk":
            return
        params = [('direction', 'out'),
                        ('include_labels', False),
                        ('page', 'page_example'),
                        ('pagesize', 10)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/addresses/{address}/neighbors'.format(currency='btc', address='addressA'),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_list_address_txs(self, client):
        """Test case for list_address_txs

        Get all transactions an address has been involved in
        """
        await test_service.list_address_txs(self)
        if 'list_address_txs_sync' in dir(test_service):
            test_service.list_address_txs_sync(self)

        if "list_address_txs" == "bulk":
            return
        params = [('page', 'page_example'),
                        ('pagesize', 10)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/addresses/{address}/txs'.format(currency='btc', address='addressA'),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_list_tags_by_address(self, client):
        """Test case for list_tags_by_address

        Get attribution tags for a given address
        """
        await test_service.list_tags_by_address(self)
        if 'list_tags_by_address_sync' in dir(test_service):
            test_service.list_tags_by_address_sync(self)

        if "list_tags_by_address" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/addresses/{address}/tags'.format(currency='btc', address='addressA'),
            headers=headers,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')

