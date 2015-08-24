#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
import json
from django.test import Client


logging.basicConfig(level=logging.INFO, format="%(message)s")


class TestRenderRegexDescription(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_resp_data(self, document):
        resp = self.client.post('/regex', data={'origin': 'www.test.com', 'document': document})
        return json.loads(resp.content)

    def request_short(self, command):
        return self.get_resp_data("\n".join(["<code>", command, "</code>"]))

    def test_describe_regex_in_command(self):
        result = self.request_short('sed "s/patt/repl/" file')
        self.assertIn("You found a regular expression: patt", result['patt'])


if __name__ == '__main__':
    unittest.main()
