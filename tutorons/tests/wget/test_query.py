#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import unittest
import logging
import json
from bs4 import BeautifulSoup
from django.test import Client


logging.basicConfig(level=logging.INFO, format="%(message)s")


class FetchAllExplanationsTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_resp_data(self, document):
        resp = self.client.post('/wget/scan', data={'origin': 'www.test.com', 'document': document})
        return json.loads(resp.content)['regions']

    def get_regions_from_code(self, code):
        return self.get_resp_data("<code>" + code + "</code>")

    def test_describe_one_command(self):
        regions = self.get_regions_from_code("wget http://hello.html")
        self.assertEqual(len(regions), 1)
        r = regions[0]
        doc = BeautifulSoup(r['document'])
        self.assertEquals(r['node'], 'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEquals(r['start_index'], 0)
        self.assertEquals(r['end_index'], 21)
        self.assertIn("downloads content from http://hello.html.", doc.text)

    def test_describe_multiple_commands(self):
        regions = self.get_resp_data("""
        <html>
            <body>
                <code>
                    wget http://hello.html
                </code>
                <code>
                    wget http://goodbye.html
                </code>
            </body>
        </html>
        """)
        self.assertEqual(len(regions), 2)

    def test_skip_invalid_wget(self):
        regions = self.get_regions_from_code("wget --buzzer fakearg")
        self.assertEqual(len(regions), 0)

    def test_describe_windows_executable(self):
        regions = self.get_regions_from_code("wget.exe http://hello.html")
        self.assertEqual(len(regions), 1)


class FetchExplanationForPlaintextTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_explanation(self, text):
        resp = self.client.post('/wget/explain', data={'origin': 'www.test.com', 'text': text})
        return json.loads(resp.content)['region']['document']

    def test_explain_wget_command(self):
        resp = self.get_explanation('wget http://google.com')
        self.assertIn("is a Terminal command you run to download", resp)

    def test_fail_to_explain_not_wget(self):
        resp = self.get_explanation('invalid command')
        self.assertIn("'invalid command' could not be explained as a wget command", resp)
