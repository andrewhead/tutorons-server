#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
import json
from django.test import Client
import httpretty
from bs4 import BeautifulSoup
from django.conf import settings


logging.basicConfig(level=logging.INFO, format="%(message)s")
logging.disable(logging.CRITICAL)


class FetchAllExplanationsTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    @httpretty.activate
    def get_regions(self, document):
        httpretty.register_uri(
            httpretty.GET, settings.REGEX_SVG_ENDPOINT,
            body="<div><div><svg><g class='root'></g></svg></div></div>")
        resp = self.client.post(
            '/regex/scan', data={'origin': 'www.test.com', 'document': document})
        return json.loads(resp.content)

    def get_regions_for_line(self, command):
        return self.get_regions("<code>" + command + "</code>")

    def test_get_region(self):
        regions = self.get_regions_for_line('sed "s/patt/repl/" file')
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEquals(r['node'], 'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEquals(r['start_index'], 7)
        self.assertEquals(r['end_index'], 10)
        self.assertIn("You found a regular expression", r['document'])

    def test_get_mutliple_regions(self):
        regions = self.get_regions_for_line('\n'.join([
            'sed "s/patt/repl/" file',
            'sed "s/patt2/repl/" file'
        ]))
        self.assertEqual(len(regions), 2)

    def test_description_includes_svg_and_example(self):
        regions = self.get_regions_for_line('sed "s/patt/repl/" file')
        r = regions[0]
        soup = BeautifulSoup(r['document'])
        self.assertEqual(len(soup.select('svg')), 1)
        self.assertIn("This pattern can match a string like", soup.text)


class FetchExplanationForPlaintextText(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_explanation(self, text):
        resp = self.client.post('/regex/explain', data={'origin': 'www.test.com', 'text': text})
        return resp.content

    @httpretty.activate
    def test_explain_regex_plaintext(self):
        httpretty.register_uri(
            httpretty.GET, settings.REGEX_SVG_ENDPOINT,
            body="<div><div><svg><g class='root'></g></svg></div></div>")
        resp = self.get_explanation('(a|b)*')
        self.assertIn("You found a regular expression", resp)

    @httpretty.activate
    def test_fail_to_explain_plaintext_invalid_regex(self):
        httpretty.register_uri(
            httpretty.GET, settings.REGEX_SVG_ENDPOINT,
            body="<div><div><svg></svg></div></div>")
        resp = self.get_explanation('[A-')
        self.assertIn("'[A-' could not be explained as a regular expression", resp)
