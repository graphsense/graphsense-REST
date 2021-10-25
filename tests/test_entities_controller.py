# coding: utf-8

import pytest
import json
from aiohttp import web

from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.entity import Entity
from openapi_server.models.entity_addresses import EntityAddresses
from openapi_server.models.links import Links
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.search_result_level1 import SearchResultLevel1
from openapi_server.models.tags import Tags
from openapi_server.test import BaseTestCase
import gsrest.test.entities_service as test_service


class TestEntitiesController(BaseTestCase):
    """EntitiesController integration test stubs"""

    async def test_get_entity(self, client):
        """Test case for get_entity

        Get an entity, optionally with tags
        """
        await test_service.get_entity(self)
        if 'get_entity_sync' in dir(test_service):
            test_service.get_entity_sync(self)

        if "get_entity" == "bulk":
            return
        params = [('include_tags', False),
                        ('tag_coherence', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/entities/{entity}'.format(currency='btc', entity=67065),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_list_entity_addresses(self, client):
        """Test case for list_entity_addresses

        Get an entity's addresses
        """
        await test_service.list_entity_addresses(self)
        if 'list_entity_addresses_sync' in dir(test_service):
            test_service.list_entity_addresses_sync(self)

        if "list_entity_addresses" == "bulk":
            return
        params = [('page', 'page_example'),
                        ('pagesize', 10)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/entities/{entity}/addresses'.format(currency='btc', entity=67065),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_list_entity_links(self, client):
        """Test case for list_entity_links

        Get transactions between two entities
        """
        await test_service.list_entity_links(self)
        if 'list_entity_links_sync' in dir(test_service):
            test_service.list_entity_links_sync(self)

        if "list_entity_links" == "bulk":
            return
        params = [('neighbor', 123456)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/entities/{entity}/links'.format(currency='btc', entity=67065),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_list_entity_neighbors(self, client):
        """Test case for list_entity_neighbors

        Get an entity's neighbors in the entity graph
        """
        await test_service.list_entity_neighbors(self)
        if 'list_entity_neighbors_sync' in dir(test_service):
            test_service.list_entity_neighbors_sync(self)

        if "list_entity_neighbors" == "bulk":
            return
        params = [('direction', 'out'),
                        ('only_ids', [56]),
                        ('include_labels', False),
                        ('page', 'page_example'),
                        ('pagesize', 10)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/entities/{entity}/neighbors'.format(currency='btc', entity=67065),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_list_entity_txs(self, client):
        """Test case for list_entity_txs

        Get all transactions an entity has been involved in
        """
        await test_service.list_entity_txs(self)
        if 'list_entity_txs_sync' in dir(test_service):
            test_service.list_entity_txs_sync(self)

        if "list_entity_txs" == "bulk":
            return
        params = [('page', 'page_example'),
                        ('pagesize', 10)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/entities/{entity}/txs'.format(currency='btc', entity=67065),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_list_tags_by_entity(self, client):
        """Test case for list_tags_by_entity

        Get tags for a given entity
        """
        await test_service.list_tags_by_entity(self)
        if 'list_tags_by_entity_sync' in dir(test_service):
            test_service.list_tags_by_entity_sync(self)

        if "list_tags_by_entity" == "bulk":
            return
        params = [('tag_coherence', False)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/entities/{entity}/tags'.format(currency='btc', entity=67065),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_search_entity_neighbors(self, client):
        """Test case for search_entity_neighbors

        Search deeply for matching neighbors
        """
        await test_service.search_entity_neighbors(self)
        if 'search_entity_neighbors_sync' in dir(test_service):
            test_service.search_entity_neighbors_sync(self)

        if "search_entity_neighbors" == "bulk":
            return
        params = [('direction', 'out'),
                        ('key', 'category'),
                        ('value', ['Miner']),
                        ('depth', 2),
                        ('breadth', 16),
                        ('skip_num_addresses', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/{currency}/entities/{entity}/search'.format(currency='btc', entity=67065),
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')

