# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.concept import Concept  # noqa: E501
from openapi_server.models.tag import Tag  # noqa: E501
from openapi_server.models.taxonomy import Taxonomy  # noqa: E501
from openapi_server.test import BaseTestCase
import gsrest.test.tags_service as test_service


class TestTagsController(BaseTestCase):
    """TagsController integration test stubs"""

    def test_list_concepts(self):
        """Test case for list_concepts

        Returns the supported concepts of a taxonomy
        """
        test_service.list_concepts(self)

        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/tags/taxonomies/{taxonomy}/concepts'.format(taxonomy="foo"),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_list_tags(self):
        """Test case for list_tags

        Returns the tags associated with a given label
        """
        test_service.list_tags(self)

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
        test_service.list_taxonomies(self)

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
