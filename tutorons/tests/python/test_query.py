#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest
import json
from bs4 import BeautifulSoup
from django.test import Client

logging.basicConfig(level=logging.INFO, format="%(message)s")


class FetchAllExplanationsTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_regions(self, document):
        resp = self.client.post(
            '/python/scan',
            data={'origin': 'www.test.com', 'document': document})
        regions = json.loads(resp.content)
        return regions

    def test_get_region(self):
        string = "<html> <body> <code>abs(2)</code> </body> </html>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(
            r['node'],
            'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEqual(r['start_index'], 0)
        self.assertEqual(r['end_index'], 2)
        self.assertIn(
            "Return the absolute value of a number.",
            BeautifulSoup(r['document']).text
        )

    def test_get_multiple_regions(self):
        string = "<html> <body> <code>abs(2)\nlen('fdsjkfds')\nbin(1)</code> </body> </html>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 3)
        r0 = regions[0]
        self.assertEqual(
            r0['node'],
            'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEqual(r0['start_index'], 0)
        self.assertEqual(r0['end_index'], 2)
        self.assertIn(
            "Return the absolute value of a number.",
            BeautifulSoup(r0['document']).text
        )

        r1 = regions[1]
        self.assertEqual(
            r1['node'],
            'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEqual(r1['start_index'], 7)
        self.assertEqual(r1['end_index'], 9)
        self.assertIn(
            "Return the length (the number of items) of an object.",
            BeautifulSoup(r1['document']).text
        )


class FetchExplanationForPlaintextTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_explanation(self, text):
        resp = self.client.post(
            '/python/explain',
            data={'origin': 'www.test.com', 'text': text})
        return resp.content

    def test_explain_python_builtin_from_plaintext(self):
        resp = self.get_explanation('zip')
        self.assertIn("This function returns a list of tuples,", resp)

    def test_fail_to_explain_invalid_python_builtin_from_plaintext(self):
        resp = self.get_explanation('zip()')
        self.assertIn("'zip()' could not be explained as a python built-in.", resp)
