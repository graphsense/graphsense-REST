import logging
import os
import json
from aiohttp.test_utils import AioHTTPTestCase

from openapi_server import main


class BaseTestCase(AioHTTPTestCase):

    async def get_application(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        return main(os.path.join(os.getcwd(), 'tests/instance/config.yaml'))

    async def requestWithCode(self, path, code, **kwargs):
        headers = {
            'Accept': 'application/json',
        }
        response = await self.client.request(
            path=path.format(**kwargs),
            method='GET',
            headers=headers)
        content = (await response.read()).decode('utf-8')
        self.assertEqual(code, response.status, "response is " + content)
        if code != 200:
            return
        return json.loads(content)

    def request(self, path, **kwargs):
        return self.requestWithCode(path, 200, **kwargs)


