# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.entity_with_tags import EntityWithTags  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.entities_service as test_service


class TestEntitiesController(BaseTestCase):
    """EntitiesController integration test stubs"""

    def test_get_entity_with_tags(self):
        """Test case for get_entity_with_tags

        Get an entity with tags
        """
        test_service.get_entity_with_tags(self)

        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/{currency}/entities/{entity}'.format(currency="btc", entity="67065"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))



if __name__ == '__main__':
    unittest.main()
