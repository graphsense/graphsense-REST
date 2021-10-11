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
        test_service.get_entity(self)

        if "get_entity" in ["batch", "get_tx_io"]:
            return
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
        test_service.list_entities(self)

        if "list_entities" in ["batch", "get_tx_io"]:
            return
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

        if "list_entity_addresses" in ["batch", "get_tx_io"]:
            return
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
        test_service.list_entity_links(self)

        if "list_entity_links" in ["batch", "get_tx_io"]:
            return
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
        test_service.list_entity_neighbors(self)

        if "list_entity_neighbors" in ["batch", "get_tx_io"]:
            return
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
        test_service.list_entity_txs(self)

        if "list_entity_txs" in ["batch", "get_tx_io"]:
            return
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
        test_service.list_tags_by_entity(self)

        if "list_tags_by_entity" in ["batch", "get_tx_io"]:
            return
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
        test_service.search_entity_neighbors(self)

        if "search_entity_neighbors" in ["batch", "get_tx_io"]:
            return
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
