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
        resp = self.client.post('/css', data={'origin': 'www.test.com', 'document': document})
        regions = json.loads(resp.content)
        return regions

    def _make_code_block(self, text):
        return "<code>" + text + "</code>"

    def test_get_region(self):
        doc = self._make_code_block('var elem = $(".klazz");')
        regions = self.get_regions(doc)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r['node'], 'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEqual(r['start_index'], 14)
        self.assertEqual(r['end_index'], 19)
        self.assertIn(
            "chooses elements of class 'klazz'",
            BeautifulSoup(r['document']).text
        )

    def test_get_multiple_regions(self):
        doc = self._make_code_block('\n'.join([
            'var elem1 = $(".klazz");',
            'var elem2 = $(".klazz");',
        ]))
        regions = self.get_regions(doc)
        self.assertEqual(len(regions), 2)


class FetchExplanationForPlaintextTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_explanation(self, text):
        resp = self.client.post('/explain/css', data={'origin': 'www.test.com', 'text': text})
        return resp.content

    def test_explain_css_selector_from_plaintext(self):
        resp = self.get_explanation('div.klazz')
        self.assertIn("chooses containers of class", resp)

    def test_fail_to_explain_invalid_selector_from_plaintext(self):
        resp = self.get_explanation('invalid....selector')
        self.assertIn("'invalid....selector' could not be explained as a CSS selector", resp)


class FetchExplanationForFuzzyMatchTestMatch(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_explanation_text(self, text, edge_size):
        resp = self.client.post('/explain/css', data={
            'origin': 'www.test.com',
            'text': text,
            'edge_size': edge_size
        })
        soup = BeautifulSoup(resp.content)
        return soup.text

    def test_explain_css_selector_from_plaintext(self):
        resp = self.get_explanation_text('"div.klazz"', edge_size=1)
        self.assertIn("The selector 'div.klazz' chooses", resp)
