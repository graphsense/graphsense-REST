# coding: utf-8

import pytest
import json
from aiohttp import web
from aiohttp.test_utils import unittest_run_loop

from openapi_server.models.address_tags import AddressTags
from openapi_server.models.concept import Concept
from openapi_server.models.taxonomy import Taxonomy
from tests import BaseTestCase
import gsrest.test.tags_service as test_service


class TestTagsController(BaseTestCase):
    """TagsController integration test stubs"""

    async def test_list_address_tags(self):
        """Test case for list_address_tags

        Returns address tags associated with a given label
        """
        await test_service.list_address_tags(self)


    async def test_list_concepts(self):
        """Test case for list_concepts

        Returns the supported concepts of a taxonomy
        """
        await test_service.list_concepts(self)


    async def test_list_taxonomies(self):
        """Test case for list_taxonomies

        Returns the supported taxonomies
        """
        await test_service.list_taxonomies(self)

