# coding: utf-8

import pytest
import json
from aiohttp import web
from aiohttp.test_utils import unittest_run_loop

from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.entity import Entity
from openapi_server.models.entity_addresses import EntityAddresses
from openapi_server.models.links import Links
from openapi_server.models.neighbors import Neighbors
from openapi_server.models.search_result_level1 import SearchResultLevel1
from openapi_server.models.tags import Tags
from tests import BaseTestCase
import gsrest.test.entities_service as test_service


class TestEntitiesController(BaseTestCase):
    """EntitiesController integration test stubs"""

    @unittest_run_loop
    async def test_get_entity(self):
        """Test case for get_entity

        Get an entity, optionally with tags
        """
        await test_service.get_entity(self)


    @unittest_run_loop
    async def test_list_entity_addresses(self):
        """Test case for list_entity_addresses

        Get an entity's addresses
        """
        await test_service.list_entity_addresses(self)


    @unittest_run_loop
    async def test_list_entity_links(self):
        """Test case for list_entity_links

        Get transactions between two entities
        """
        await test_service.list_entity_links(self)


    @unittest_run_loop
    async def test_list_entity_neighbors(self):
        """Test case for list_entity_neighbors

        Get an entity's neighbors in the entity graph
        """
        await test_service.list_entity_neighbors(self)


    @unittest_run_loop
    async def test_list_entity_txs(self):
        """Test case for list_entity_txs

        Get all transactions an entity has been involved in
        """
        await test_service.list_entity_txs(self)


    @unittest_run_loop
    async def test_list_tags_by_entity(self):
        """Test case for list_tags_by_entity

        Get tags for a given entity for the given level
        """
        await test_service.list_tags_by_entity(self)


    @unittest_run_loop
    async def test_search_entity_neighbors(self):
        """Test case for search_entity_neighbors

        Search deeply for matching neighbors
        """
        await test_service.search_entity_neighbors(self)

