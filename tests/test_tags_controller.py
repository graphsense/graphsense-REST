# coding: utf-8

import pytest
import json
from aiohttp import web

from openapi_server.models.concept import Concept
from openapi_server.models.tags import Tags
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.test import BaseTestCase
import gsrest.test.tags_service as test_service


class TestTagsController(BaseTestCase):
    """TagsController integration test stubs"""

    async def test_list_concepts(self, client):
        """Test case for list_concepts

        Returns the supported concepts of a taxonomy
        """
        await test_service.list_concepts(self)
        if 'list_concepts_sync' in dir(test_service):
            test_service.list_concepts_sync(self)

        if "list_concepts" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/tags/taxonomies/{taxonomy}/concepts'.format(taxonomy='foo'),
            headers=headers,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_list_tags(self, client):
        """Test case for list_tags

        Returns address and entity tags associated with a given label
        """
        await test_service.list_tags(self)
        if 'list_tags_sync' in dir(test_service):
            test_service.list_tags_sync(self)

        if "list_tags" == "bulk":
            return
        params = [('currency', 'btc'),
                        ('label', 'cimedy')]
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/tags',
            headers=headers,
            params=params,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


    async def test_list_taxonomies(self, client):
        """Test case for list_taxonomies

        Returns the supported taxonomies
        """
        await test_service.list_taxonomies(self)
        if 'list_taxonomies_sync' in dir(test_service):
            test_service.list_taxonomies_sync(self)

        if "list_taxonomies" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = await client.request(
            method='GET',
            path='/tags/taxonomies',
            headers=headers,
            )
        assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')

