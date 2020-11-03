# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.entity_addresses import EntityAddresses  # noqa: E501
from openapi_server.models.entity_with_tags import EntityWithTags  # noqa: E501
from openapi_server.models.neighbors import Neighbors  # noqa: E501
from openapi_server.models.tag import Tag  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.entities_service as test_service


class TestEntitiesController(BaseTestCase):
    """EntitiesController integration test stubs"""

    def test_get_entity_with_tags(self):
        """Test case for get_entity_with_tags

        Get an entity with tags
        """
        test_service.get_entity_with_tags(self)

        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}'.format(currency="btc", entity="67065"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_entity_addresses(self):
        """Test case for list_entity_addresses

        Get an entity's addresses
        """
        test_service.list_entity_addresses(self)

        query_string = [
                        ]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}/addresses'.format(currency="btc", entity="67065"),
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

        query_string = [('direction', 'out'),('direction', 'out')
                        
                        
                        ]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}/neighbors'.format(currency="btc", entity="67065"),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_entity_neighbors_csv(self):
        """Test case for list_entity_neighbors_csv

        Get an entity's neighbors in the entity graph as CSV
        """
        test_service.list_entity_neighbors_csv(self)

        query_string = [('direction', 'out')]
        headers = { 
            'Accept': 'text/csv',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}/neighbors.csv'.format(currency="btc", entity="67065"),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_entity_tags(self):
        """Test case for list_entity_tags

        Get attribution tags for a given entity
        """
        test_service.list_entity_tags(self)

        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}/tags'.format(currency="btc", entity="67065"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_entity_tags_csv(self):
        """Test case for list_entity_tags_csv

        Get attribution tags for a given entity as CSV
        """
        test_service.list_entity_tags_csv(self)

        headers = { 
            'Accept': 'application/csv',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}/tags.csv'.format(currency="btc", entity="67065"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))



if __name__ == '__main__':
    unittest.main()
