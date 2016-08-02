#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest
import json
from bs4 import BeautifulSoup
from django.test import Client

logging.basicConfig(level=logging.INFO, format="%(message)s")


class PackageExplanationTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_regions(self, document):
        resp = self.client.post(
            '/package/scan',
            data={'origin': 'www.test.com', 'document': document})
        regions = json.loads(resp.content)['regions']
        return regions
