#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest

from tutorons.regex.extract import ModRewriteRegexExtractor, JavascriptRegexExtractor,\
    GrepRegexExtractor, SedRegexExtractor
from tutorons.common.htmltools import HtmlDocument


logging.basicConfig(level=logging.INFO, format="%(message)s")


'''
TODO consider implementing regular expression checking for these languages:
1. tcl shell
2. Python regular expression methods
3. Java methods
4. sed
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


class ExtractRegexFromGrepTest(unittest.TestCase):

    def setUp(self):
        self.extractor = GrepRegexExtractor()

    def test_extract_regex_from_variable_declaration(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            "grep pattern *",
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.node, node)
        self.assertEqual(r.start_offset, 6)
        self.assertEqual(r.end_offset, 12)

    def test_extract_same_pattern_from_multiple_greps_in_one_element(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            "grep pattern *",
            "grep pattern *",
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 2)
        r1 = regions[0]
        self.assertEqual(r1.start_offset, 6)
        self.assertEqual(r1.end_offset, 12)
        r2 = regions[1]
        self.assertEqual(r2.start_offset, 21)
        self.assertEqual(r2.end_offset, 27)

    def test_extract_pattern_containing_spaces(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            "grep 'Pattern with spaces' *",
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 7)
        self.assertEqual(r.end_offset, 25)

    def test_extract_pattern_from_option(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            "grep -e pattern *",
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 9)
        self.assertEqual(r.end_offset, 15)

    def test_extract_patterns_from_multiple_options(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            "grep -e pattern1 -e pattern2 *",
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 2)
        self.assertTrue(any([r.start_offset == 9 and r.end_offset == 16 for r in regions]))
        self.assertTrue(any([r.start_offset == 21 and r.end_offset == 28 for r in regions]))


class ExtractRegexFromSedTest(unittest.TestCase):

    def setUp(self):
        self.extractor = SedRegexExtractor()

    def test_extract_regexes_from_address_range(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            'sed "/addr1/,/addr2/p" file',
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 2)
        r1 = regions[0]
        self.assertEqual(r1.node, node)
        self.assertEqual(r1.start_offset, 7)
        self.assertEqual(r1.end_offset, 11)
        r2 = regions[1]
        self.assertEqual(r2.start_offset, 15)
        self.assertEqual(r2.end_offset, 19)

    def test_ignore_addresses_that_arent_regex(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            'sed "0,1p" file',
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 0)

    def test_extract_regex_from_substitute_pattern(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            'sed "s/patt/replace/" file',
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.start_offset, 8)
        self.assertEqual(r.end_offset, 11)

    def test_extract_regex_from_multiple_substitute_patterns(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            'sed -e "s/patt1/replace/" -e "s/patt2/replace/" file',
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 2)
        self.assertTrue(any([r.start_offset == 11 and r.end_offset == 15 for r in regions]))
        self.assertTrue(any([r.start_offset == 33 and r.end_offset == 37 for r in regions]))

    def test_handle_escaped_characters(self):
        return
        node = HtmlDocument('\n'.join([
            '<code>',
            'sed "s/pa\\\\/tt/replace/" file',
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.start_offset, 8)
        self.assertEqual(r.end_offset, 13)


if __name__ == '__main__':
    unittest.main()
