#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest

from tutorons.regex.extract import ModRewriteRegexExtractor, JavascriptRegexExtractor
from tutorons.common.htmltools import HtmlDocument


logging.basicConfig(level=logging.INFO, format="%(message)s")


'''
TODO consider implementing regular expression checking for these languages:
1. tcl shell
2. Python regular expression methods
3. Java methods
'''


class ExtractRegexFromModRewriteTest(unittest.TestCase):

    def setUp(self):
        self.extractor = ModRewriteRegexExtractor()

    def test_extract_regex_for_rewrite_rule(self):
        node = HtmlDocument('\n'.join([
            "<code>",
            "RewriteRule ^.*$ index.php",
            "</code>",
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.node, node)
        self.assertEqual(r.start_offset, 13)
        self.assertEqual(r.end_offset, 16)

    def test_extract_regex_for_rewrite_condition(self):
        node = HtmlDocument('\n'.join([
            "<code>",
            "RewriteCond  %{HTTP_USER_AGENT}  ^Mozilla",
            "</code>",
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.start_offset, 34)
        self.assertEqual(r.end_offset, 41)

    def test_allow_whitespace_before_directive(self):
        node = HtmlDocument('\n'.join([
            "<code>",
            "    RewriteCond  %{HTTP_USER_AGENT}  ^Mozilla",
            "</code>",
        ]))
        regions = self.extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 38)
        self.assertEqual(r.end_offset, 45)

    def test_case_insensitive_directive_detected(self):
        node = HtmlDocument('\n'.join([
            "<code>",
            "REWRITEcOnD  %{HTTP_USER_AGENT}  ^Mozilla",
            "</code>",
        ]))
        regions = self.extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 34)
        self.assertEqual(r.end_offset, 41)


class ExtractRegexFromJavascriptTest(unittest.TestCase):

    def setUp(self):
        self.extractor = JavascriptRegexExtractor()

    def test_extract_regex_from_variable_declaration(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            "var pattern = /regular-expression/g;",
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.node, node)
        self.assertEqual(r.start_offset, 16)
        self.assertEqual(r.end_offset, 33)


if __name__ == '__main__':
    unittest.main()
