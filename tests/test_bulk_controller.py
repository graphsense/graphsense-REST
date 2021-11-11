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
    async def test_bulk_csv(self):
        """Test case for bulk_csv

        Get data as CSV in bulk
        """
        await test_service.bulk_csv(self)


    @unittest_run_loop
    async def test_bulk_json(self):
        """Test case for bulk_json

        Get data as JSON in bulk
        """
        await test_service.bulk_json(self)

