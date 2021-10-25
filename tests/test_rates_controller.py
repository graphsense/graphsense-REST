# coding: utf-8

import pytest
import json
from aiohttp import web
from aiohttp.test_utils import unittest_run_loop

from openapi_server.models.rates import Rates
from tests import BaseTestCase
import gsrest.test.rates_service as test_service


class TestRatesController(BaseTestCase):
    """RatesController integration test stubs"""

    @unittest_run_loop
    async def test_get_exchange_rates(self):
        """Test case for get_exchange_rates

        Returns exchange rate for a given height
        """
        await test_service.get_exchange_rates(self)

