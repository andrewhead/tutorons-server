#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest
import json
from bs4 import BeautifulSoup
from django.test import Client

logging.basicConfig(level=logging.INFO, format="%(message)s")


class FetchExplanationsForPythonBuiltInsTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_regions(self, document):
        resp = self.client.post(
            '/python/scan',
            data={'origin': 'www.test.com', 'document': document})
        regions = json.loads(resp.content)
        return regions

    def test_single_built_in(self):
        string = "<html> <body> <code>abs(2)</code> </body> </html>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(
            r['node'],
            'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEqual(r['start_index'], 0)
        self.assertEqual(r['end_index'], 2)

    def test_multiple_built_ins(self):
        string = "<html> <body> <code>abs(2)\nlen('fdsjkfds')\nbin(1)</code> </body> </html>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 3)
        r0 = regions[0]
        self.assertEqual(
            r0['node'],
            'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEqual(r0['start_index'], 0)
        self.assertEqual(r0['end_index'], 2)

        r1 = regions[1]
        self.assertEqual(
            r1['node'],
            'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEqual(r1['start_index'], 7)
        self.assertEqual(r1['end_index'], 9)

        r2 = regions[2]
        self.assertEqual(
            r2['node'],
            'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEqual(r2['start_index'], 23)
        self.assertEqual(r2['end_index'], 25)

    def test_binary_op_built_ins(self):
        string = "<html> <body> <code>abs(2) + len('fdsjkfds') </code> </body> </html>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 2)
        r0 = regions[0]
        self.assertEqual(r0['start_index'], 0)
        self.assertEqual(r0['end_index'], 2)

        r1 = regions[1]
        self.assertEqual(r1['start_index'], 9)
        self.assertEqual(r1['end_index'], 11)

    def test_ignore_malformed_calls(self):
        string = "<html> <body> <code>abs(2</code> </body> </html>"
        regions = self.get_regions(string)
        self.assertEqual(len(regions), 0)

    def test_detect_builtin_after_increment(self):
        string = "<html> <body> <code>x = 2\nx += abs(-1)</code> </body> </html>"
        regions = self.get_regions(string)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r['start_index'], 11)
        self.assertEqual(r['end_index'], 13)

    def test_detect_print(self):
        string = "<html> <body> <code>print(len([1,2,3,4]))</code> </body> </html>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r['start_index'], 6)
        self.assertEqual(r['end_index'], 8)