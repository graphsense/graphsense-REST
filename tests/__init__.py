import json
import logging

import pytest

# Register assert rewriting for nice diffs in tests
# https://docs.pytest.org/en/stable/how-to/writing_plugins.html#assertion-rewriting
# CAUTION THIS ONLY WORKS WHEN USING assert a == b not the unittest derived methods self.assertEqual...()
pytest.register_assert_rewrite("gsrest")

from aiohttp.test_utils import AioHTTPTestCase  # noqa: E402

from gsrest import factory_internal  # noqa: E402


class BaseTestCase(AioHTTPTestCase):
    async def get_application(
        self,
    ):
        logging.getLogger("connexion.operation").setLevel("ERROR")

        return factory_internal(self.config, validate_responses=True).app

    async def requestOnly(self, path, body, **kwargs):
        headers = {
            "Accept": "application/json",
            "Authorization": kwargs.get("auth", "x"),
        }
        response = await self.client.request(
            path=path.format(**kwargs),
            method="GET" if body is None else "POST",
            json=body,
            headers=headers,
        )
        return (response, (await response.read()).decode("utf-8"))

    async def requestWithCodeAndBody(self, path, code, body, **kwargs):
        headers = {
            "Accept": "application/json",
            "Authorization": kwargs.get("auth", "x"),
        }
        response = await self.client.request(
            path=path.format(**kwargs),
            method="GET" if body is None else "POST",
            json=body,
            headers=headers,
        )
        content = (await response.read()).decode("utf-8")
        self.assertEqual(code, response.status, "response is " + content)
        if code != 200:
            return
        return json.loads(content)

    def request(self, path, **kwargs):
        return self.requestWithCodeAndBody(path, 200, None, **kwargs)

    def assertEqualWithList(self, a, b, *keys):
        keys = iter(keys)
        key = next(keys)
        pa = a
        pb = b
        aa = a[key]
        bb = b[key]
        while not isinstance(aa, list):
            key = next(keys)
            pa = aa
            pb = bb
            aa = aa[key]
            bb = bb[key]
        listkey = next(keys)

        def fun(x):
            return x[listkey]

        pa[key] = sorted(pa[key], key=fun)
        pb[key] = sorted(pb[key], key=fun)

        assert a == b
        # return self.assertEqual(a, b)
