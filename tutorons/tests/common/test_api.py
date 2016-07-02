#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
import datetime

from tutorons.common.models import ServerQuery, ClientQuery


logging.basicConfig(level=logging.INFO, format="%(message)s")


class WriteOnlyMetaTest(ResourceTestCaseMixin, TestCase):
    '''
    We test the write-only meta (which only enables creating at list level) by testing
    one of the resources created with that meta---ClientQuery.

    A lot of this test case is based on the example code in the TastyPie documentation:
    http://django-tastypie.readthedocs.org/en/latest/testing.html
    '''

    def setUp(self):
        super(WriteOnlyMetaTest, self).setUp()

        # Initialize test data
        self.server_query = ServerQuery.objects.create(
            start_time='2016-01-01T01:00:01',
            end_time='2016-01-01T01:00:04',
            ip_addr='192.168.0.0',
            path='/python/scan',
        )
        self.client_query = ClientQuery.objects.create(
            start_time=datetime.datetime(2016, 1, 1, 1, 0, 0),
            end_time=datetime.datetime(2016, 1, 1, 1, 0, 5),
            server_query=self.server_query
        )

    def test_post_item_passes_and_succeeds(self):
        self.assertHttpCreated(self.api_client.post(
            '/api/v1/client_query/',
            format='json',
            data={
                'start_time': '2016-01-01T01:00:00',
                'end_time': '2016-01-01T01:00:05',
                'server_query': '/api/v1/server_query/{0}/'.format(self.server_query.pk),
            }
        ))
        self.assertEqual(ClientQuery.objects.count(), 2)

    def test_get_detail_not_allowed(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(
            '/api/v1/client_query/{0}/'.format(self.client_query.pk)))

    def test_get_list_not_allowed(self):
        self.assertHttpMethodNotAllowed(self.api_client.get('/api/v1/client_query/'))

    def test_update_detail_not_allowed(self):
        self.assertHttpMethodNotAllowed(self.api_client.put(
            '/api/v1/client_query/{0}/'.format(self.client_query.pk),
            format='json',
            data={'end_time': '2016-01-01T01:00:06'}
        ))

    def test_update_list_not_allowed(self):
        self.assertHttpMethodNotAllowed(self.api_client.put(
            '/api/v1/client_query/',
            format='json',
            data=[{
                'start_time': '2016-01-01T01:00:00',
                'end_time': '2016-01-01T01:00:05',
                'server_query': '/api/v1/server_query/{0}/'.format(self.server_query.pk),
            }]
        ))

    def test_delete_detail_not_allowed(self):
        self.assertHttpMethodNotAllowed(self.api_client.delete(
            '/api/v1/client_query/{0}/'.format(self.client_query.pk)))
        self.assertEqual(ClientQuery.objects.count(), 1)

    def test_delete_list_not_allowed(self):
        self.assertHttpMethodNotAllowed(self.api_client.delete('/api/v1/client_query/'))
        self.assertEqual(ClientQuery.objects.count(), 1)


class HideUnusedResourcesTest(ResourceTestCaseMixin, TestCase):

    def test_post_server_query_not_found(self):
        self.assertHttpNotFound(self.api_client.post(
            '/api/v1/server_query/',
            format='json',
            data={
                'start_time': '2016-01-01T01:00:01',
                'end_time': '2016-01-01T01:00:04',
                'ip_addr': '192.168.0.0',
                'path': '/python/scan',
            }
        ))

    def test_post_block_not_found(self):
        self.assertHttpNotFound(self.api_client.post(
            '/api/v1/block/',
            format='json',
            data={
                'time': '2016-01-01T01:00:00',
                'url': 'www.stackoverflow.com',
                'block_type': 'pre',
                'block_text': "block text",
                'block_hash': "DEADBEEF",
            }
        ))
