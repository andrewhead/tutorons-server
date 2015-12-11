#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest
import json
from bs4 import BeautifulSoup
from django.test import Client

logging.basicConfig(level=logging.INFO, format="%(message)s")


class FetchExplanationsForSelectorsInStylesheetTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_regions(self, document):
        resp = self.client.post(
            '/css/scan',
            data={'origin': 'www.test.com', 'document': document})
        regions = json.loads(resp.content)
        return regions

    def test_single_css_selector(self):

        string = "".join([
            "<html> <body> <code>",
            " p { background-color: lightblue; } ",
            "</code> </body> </html>"
            ])
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(
            r['node'],
            'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEqual(r['start_index'], 1)
        self.assertEqual(r['end_index'], 1)

    def test_multiple_css_selectors(self):

        string = "".join([
            "<html> <body> <code>",
            " p { background-color: lightblue; }  ",
            "h1 {color: navy; margin-left: 20px;} ",
            "</code> </body> </html>"
            ])
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 2)
        r1 = regions[0]
        self.assertEqual(
            r1['node'],
            'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEqual(r1['start_index'], 1)
        self.assertEqual(r1['end_index'], 1)

        r2 = regions[1]
        self.assertEqual(
            r2['node'],
            'HTML > BODY:nth-of-type(1) > CODE:nth-of-type(1)')
        self.assertEqual(r2['start_index'], 37)
        self.assertEqual(r2['end_index'], 38)

    def test_ignore_empty_declaration(self):

        string = "<html> <body> <code> sel { }  </code> </body> </html>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 0)

    def test_ignore_malformed_declaration(self):

        string = "<html> <body> <code> sel : }  </code> </body> </html>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 0)

        string = "<html> <body> <code> sel {  </code> </body> </html>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 0)

    def test_ignore_missing_declaration(self):

        string = "<html> <body> <code> sel </code> </body> </html>"
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 0)

    def test_ignore_java_class(self):

        string = "".join([
            "<html> <body> <code>",
            "  public class JavaClass{ protected JavaClass(int x){} ",
            "public void main(String[] args){ }} ",
            "</code> </body> </html>"
            ])
        regions = self.get_regions(string)

        self.assertEqual(len(regions), 0)

    def test_find_css_selector_filter_non_ascii(self):

        s = '\n'.join([
            "  p",
            "{",
            "text-align: center;",
            "   ",
            "color: red;",
            "}"
            ])

        string = " <html> <body> <code> " + s + " </code> </body> </html>"
        regions = self.get_regions(string)
        self.assertEqual(len(regions), 1)

    def test_find_tricky_selector(self):

        s = "table { width: 100%;} th { height: 50px; }"

        string = " <html> <body> <code> " + s + " </code> </body> </html>"
        regions = self.get_regions(string)
        self.assertEqual(len(regions), 2)


class FetchAllExplanationsTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_regions(self, document):
        resp = self.client.post(
            '/css/scan',
            data={'origin': 'www.test.com', 'document': document})
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

    def test_no_detect_file_extensions(self):
        doc = self._make_code_block('\n'.join([
            'var elem = $(".pdf");',
            'var elem = $(".PDF");',
            'var elem = $("*.pdf");'
        ]))
        regions = self.get_regions(doc)
        self.assertEqual(len(regions), 0)


class FetchExplanationForPlaintextTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def get_explanation(self, text):
        resp = self.client.post(
            '/css/explain',
            data={'origin': 'www.test.com', 'text': text})
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
        resp = self.client.post('/css/explain', data={
            'origin': 'www.test.com',
            'text': text,
            'edge_size': edge_size
        })
        soup = BeautifulSoup(resp.content)
        return soup.text

    def test_explain_css_selector_from_plaintext(self):
        resp = self.get_explanation_text('"div.klazz"', edge_size=1)
        self.assertIn("The selector 'div.klazz' chooses", resp)
