# coding: utf-8

import pytest
import json
from aiohttp import web
from aiohttp.test_utils import unittest_run_loop

from openapi_server.models.tag_summary import TagSummary
from tests import BaseTestCase
import gsrest.test.experimental_service as test_service


class TestExperimentalController(BaseTestCase):
    """ExperimentalController integration test stubs"""

    async def test_get_tag_summary_by_address(self):
        """Test case for get_tag_summary_by_address

        Get attribution tag summary for a given address
        """
        await test_service.get_tag_summary_by_address(self)


    async def test_get_tag_summary_by_entity(self):
        """Test case for get_tag_summary_by_entity

        Get address tag summary for a given entity
        """
        await test_service.get_tag_summary_by_entity(self)

