import logging
import os
import json
from aiohttp.test_utils import AioHTTPTestCase

from openapi_server import factory


class BaseTestCase(AioHTTPTestCase):

    async def get_application(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        return factory(os.path.join(os.getcwd(), 'tests/instance/config.yaml'),
                       validate_responses=True).app

    async def requestWithCodeAndBody(self, path, code, body, **kwargs):
        headers = {
            'Accept': 'application/json',
            'Authorization': 'x'
        }
        response = await self.client.request(
            path=path.format(**kwargs),
            method='GET' if body is None else 'POST',
            json=body,
            headers=headers)
        content = (await response.read()).decode('utf-8')
        self.assertEqual(code, response.status, "response is " + content)
        if code != 200:
            return
        return json.loads(content)

    def request(self, path, **kwargs):
        return self.requestWithCodeAndBody(path, 200, None, **kwargs)


