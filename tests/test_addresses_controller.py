# coding: utf-8

import pytest
import json
from aiohttp import web
from aiohttp.test_utils import unittest_run_loop

from openapi_server.models.address import Address
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.entity import Entity
from openapi_server.models.links import Links
from openapi_server.models.neighbors import Neighbors
from tests import BaseTestCase
import gsrest.test.addresses_service as test_service


class TestAddressesController(BaseTestCase):
    """AddressesController integration test stubs"""

    @unittest_run_loop
    async def test_get_address(self):
        """Test case for get_address

        Get an address, optionally with tags
        """
        await test_service.get_address(self)


    @unittest_run_loop
    async def test_get_address_entity(self):
        """Test case for get_address_entity

        Get the entity of an address
        """
        await test_service.get_address_entity(self)


    @unittest_run_loop
    async def test_list_address_links(self):
        """Test case for list_address_links

        Get outgoing transactions between two addresses
        """
        await test_service.list_address_links(self)


    @unittest_run_loop
    async def test_list_address_neighbors(self):
        """Test case for list_address_neighbors

        Get an addresses' neighbors in the address graph
        """
        await test_service.list_address_neighbors(self)


    @unittest_run_loop
    async def test_list_address_txs(self):
        """Test case for list_address_txs

        Get all transactions an address has been involved in
        """
        await test_service.list_address_txs(self)


    @unittest_run_loop
    async def test_list_tags_by_address(self):
        """Test case for list_tags_by_address

        Get attribution tags for a given address
        """
        await test_service.list_tags_by_address(self)
