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


class TestRenderRegexDescription(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    @httpretty.activate
    def get_resp_data(self, document):
        httpretty.register_uri(
            httpretty.GET, settings.REGEX_SVG_ENDPOINT,
            body="<div><div><svg></svg></div></div>")
        resp = self.client.post('/regex', data={'origin': 'www.test.com', 'document': document})
        return json.loads(resp.content)

    def request_short(self, command):
        return self.get_resp_data("\n".join(["<code>", command, "</code>"]))

    def test_introduction_appears(self):
        result = self.request_short('sed "s/patt/repl/" file')
        self.assertIn("You found a regular expression", result['patt'])

    def test_svg_included_in_description(self):
        result = self.request_short('sed "s/patt/repl/" file')
        soup = BeautifulSoup(result['patt'])
        self.assertEqual(len(soup.select('svg')), 1)


if __name__ == '__main__':
    unittest.main()
