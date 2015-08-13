#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest

from tutorons.regex.extract import ModRewriteRegexExtractor
from tutorons.common.htmltools import HtmlDocument


logging.basicConfig(level=logging.INFO, format="%(message)s")

'''
For regex, we pull test cases from the following two groups:
1. Syntax of the surrounding code is correct, the code is well-formatted, and
    the full contents of the block is just code.
2. Syntax or formatting of the code is incorrect, or the code is surrounded by
    'junk' text that's not code
'''


class RegexFromModRewriteTest(unittest.TestCase):

    def setUp(self):
        self.extractor = ModRewriteRegexExtractor()

    def test_extract_regex_for_rewrite_rule(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            'RewriteRule ^.*$ index.php',
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.start_offset, 13)
        self.assertEqual(r.end_offset, 16)

    def test_extract_regex_for_rewrite_condition(self):
        node = HtmlDocument('\n'.join([
            '<code>',
            'RewriteCond  %{HTTP_USER_AGENT}  ^Mozilla',
            '</code>',
        ]))
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.start_offset, 34)
        self.assertEqual(r.end_offset, 41)


'''
TODO additional test cases for:
1. Javascript search and replace
2. tcl shell
3. Python regular expression methods
4. Java methods
'''

if __name__ == '__main__':
    unittest.main()
