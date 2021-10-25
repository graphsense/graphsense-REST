# coding: utf-8

import pytest
import json
from aiohttp import web
from aiohttp.test_utils import unittest_run_loop

from tests import BaseTestCase
import gsrest.test.bulk_service as test_service


class TestBulkController(BaseTestCase):
    """BulkController integration test stubs"""

    @unittest_run_loop
    async def test_bulk(self):
        """Test case for bulk

        Get data as CSV or JSON in bulk
        """
        await test_service.bulk(self)

