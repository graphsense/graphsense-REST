# coding: utf-8

import pytest
import json
from aiohttp import web
from aiohttp.test_utils import unittest_run_loop

from openapi_server.models.token_configs import TokenConfigs
from tests import BaseTestCase
import gsrest.test.tokens_service as test_service


class TestTokensController(BaseTestCase):
    """TokensController integration test stubs"""

    async def test_list_supported_tokens(self):
        """Test case for list_supported_tokens

        Returns a list of supported token (sub)currencies.
        """
        await test_service.list_supported_tokens(self)

