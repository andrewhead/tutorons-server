#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
from tutorons.common.htmltools import HtmlDocument
from tutorons.common.extractor import JavascriptStringExtractor


logging.basicConfig(level=logging.INFO, format="%(message)s")


class JavascriptStringExtractText(unittest.TestCase):

    def setUp(self):
        self.extractor = JavascriptStringExtractor()

    def test_get_string_from_first_line(self):
        node = HtmlDocument('\n'.join([
            '<code>    $("string");</code>',
        ])).code
        regions = self.extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.node, node)
        self.assertEqual(r.start_offset, 7)
        self.assertEqual(r.end_offset, 12)
        self.assertEqual(r.string, "string")

    def test_get_string_from_second_line(self):
        node = HtmlDocument('\n'.join([
            '<code>var i;',
            'i = \'string\'</code>',
        ])).code
        regions = self.extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.node, node)
        self.assertEqual(r.start_offset, 12)
        self.assertEqual(r.end_offset, 17)
        self.assertEqual(r.string, "string")

    def test_get_multiple_strings(self):
        node = HtmlDocument('\n'.join([
            '<code>var newStr = "string1" + "string2";</code>',
        ])).code
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 2)

    def test_count_newlines_as_characters(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            '    $("string");',
            '</code>',
        ])).code
        regions = self.extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 8)
        self.assertEqual(r.end_offset, 13)


if __name__ == '__main__':
    unittest.main()
