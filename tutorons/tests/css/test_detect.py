#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest

from tutorons.css.detect import JavascriptSelectorExtractor
from tutorons.common.htmltools import HtmlDocument


logging.basicConfig(level=logging.INFO, format="%(message)s")


class SelectorExtractionTest(unittest.TestCase):

    def setUp(self):
        self.extractor = JavascriptSelectorExtractor()

    def test_extract_selector(self):
        node = HtmlDocument("<code>$('p').text('hello');</code>")
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.node, node)
        self.assertEqual(r.start_offset, 3)
        self.assertEqual(r.end_offset, 3)
        self.assertEqual(r.string, 'p')

    def test_extract_multiple(self):
        regions = self.extractor.extract(HtmlDocument("\n".join([
            "<code>",
            "    $('p').text('hello');",
            "    var input = $('input.klazz');",
            "</code",
        ])))
        self.assertEqual(len(regions), 2)

    def test_skip_non_html_element(self):
        regions = self.extractor.extract(HtmlDocument("<code>$('nothtml');</code>"))
        self.assertEqual(len(regions), 0)

    def test_skip_regular_expression(self):
        regions = self.extractor.extract(HtmlDocument("<code>var b = '^ab*';</code>"))
        self.assertEqual(len(regions), 0)
