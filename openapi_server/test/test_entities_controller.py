# coding: utf-8

from __future__ import absolute_import
import unittest
import asyncio

from flask import json
from six import BytesIO

from openapi_server.models.entities import Entities  # noqa: E501
from openapi_server.models.entity import Entity  # noqa: E501
from openapi_server.models.entity_addresses import EntityAddresses  # noqa: E501
from openapi_server.models.links import Links  # noqa: E501
from openapi_server.models.neighbors import Neighbors  # noqa: E501
from openapi_server.models.search_result_level1 import SearchResultLevel1  # noqa: E501
from openapi_server.models.tags import Tags  # noqa: E501
from openapi_server.models.txs_account import TxsAccount  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.entities_service as test_service


class TestEntitiesController(BaseTestCase):
    """EntitiesController integration test stubs"""

    def test_get_entity(self):
        """Test case for get_entity

        Get an entity, optionally with tags
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.get_entity(self))
        loop.close()

        query_string = [('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}'.format(currency='btc', entity=67065),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_entities(self):
        """Test case for list_entities

        Get entities
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.list_entities(self))
        loop.close()

        query_string = [('',''),
                        ('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities'.format(currency='btc'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_entity_addresses(self):
        """Test case for list_entity_addresses

        Get an entity's addresses
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.list_entity_addresses(self))
        loop.close()

        query_string = [('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}/addresses'.format(currency='btc', entity=67065),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_entity_links(self):
        """Test case for list_entity_links

        Get transactions between two entities
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.list_entity_links(self))
        loop.close()

        query_string = [('neighbor', 123456)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}/links'.format(currency='btc', entity=67065),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_entity_neighbors(self):
        """Test case for list_entity_neighbors

        Get an entity's neighbors in the entity graph
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.list_entity_neighbors(self))
        loop.close()

        query_string = [('direction', 'out'),
                        ('',''),
                        ('',''),
                        ('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}/neighbors'.format(currency='btc', entity=67065),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_entity_txs(self):
        """Test case for list_entity_txs

        Get all transactions an entity has been involved in
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.list_entity_txs(self))
        loop.close()

        query_string = [('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}/txs'.format(currency='btc', entity=67065),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_tags_by_entity(self):
        """Test case for list_tags_by_entity

        Get tags for a given entity
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.list_tags_by_entity(self))
        loop.close()

        query_string = [('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}/tags'.format(currency='btc', entity=67065),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_entity_neighbors(self):
        """Test case for search_entity_neighbors

        Search deeply for matching neighbors
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(test_service.search_entity_neighbors(self))
        loop.close()

        query_string = [('direction', 'out'),
                        ('key', 'category'),
                        ('value', ['Miner']),
                        ('depth', 2),
                        ('',''),
                        ('','')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}/search'.format(currency='btc', entity=67065),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
