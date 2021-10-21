# coding: utf-8

from __future__ import absolute_import
import unittest
import asyncio

from flask import json
from six import BytesIO

from openapi_server.models.concept import Concept  # noqa: E501
from openapi_server.models.tags import Tags  # noqa: E501
from openapi_server.models.taxonomy import Taxonomy  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.tags_service as test_service


class TestTagsController(BaseTestCase):
    """TagsController integration test stubs"""

    def test_list_concepts(self):
        """Test case for list_concepts

        Returns the supported concepts of a taxonomy
        """
        asyncio.run(test_service.list_concepts(self))
        if 'list_concepts_sync' in dir(test_service):
            test_service.list_concepts_sync(self)

        if "list_concepts" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/tags/taxonomies/{taxonomy}/concepts'.format(taxonomy='foo'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_tags(self):
        """Test case for list_tags

        Returns address and entity tags associated with a given label
        """
        asyncio.run(test_service.list_tags(self))
        if 'list_tags_sync' in dir(test_service):
            test_service.list_tags_sync(self)

        if "list_tags" == "bulk":
            return
        query_string = [('',''),
                        ('label', 'cimedy')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/tags',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_taxonomies(self):
        """Test case for list_taxonomies

        Returns the supported taxonomies
        """
        asyncio.run(test_service.list_taxonomies(self))
        if 'list_taxonomies_sync' in dir(test_service):
            test_service.list_taxonomies_sync(self)

        if "list_taxonomies" == "bulk":
            return
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/tags/taxonomies',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
