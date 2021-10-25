# coding: utf-8

import pytest
import json
from aiohttp import web
from aiohttp.test_utils import unittest_run_loop

from openapi_server.models.concept import Concept
from openapi_server.models.tags import Tags
from openapi_server.models.taxonomy import Taxonomy
from tests import BaseTestCase
import gsrest.test.tags_service as test_service


class TestTagsController(BaseTestCase):
    """TagsController integration test stubs"""

    @unittest_run_loop
    async def test_list_concepts(self):
        """Test case for list_concepts

        Returns the supported concepts of a taxonomy
        """
        await test_service.list_concepts(self)


    @unittest_run_loop
    async def test_list_tags(self):
        """Test case for list_tags

        Returns address and entity tags associated with a given label
        """
        await test_service.list_tags(self)


    @unittest_run_loop
    async def test_list_taxonomies(self):
        """Test case for list_taxonomies

        Returns the supported taxonomies
        """
        await test_service.list_taxonomies(self)

