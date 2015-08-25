#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
import re

from tutorons.common.scanner import NodeScanner
from tutorons.common.extractor import Region
from tutorons.common.htmltools import HtmlDocument


logging.basicConfig(level=logging.INFO, format="%(message)s")


class ScanNodesTest(unittest.TestCase):

    def test_only_scan_embedded_pattern_once_in_multilevel_tree(self):
        node = HtmlDocument('<div><p>hello</p></div>')
        extractor = HelloTextExtractor()
        scanner = NodeScanner(extractor, ['p', 'div'])
        regions = scanner.scan(node)
        self.assertEqual(len(regions), 1)

    def test_node_of_region_is_the_lowest_enclosing_element(self):
        node = HtmlDocument('\n'.join([
            '<div>',
            '  <p>hello</p>',
            '</div>',
        ]))
        extractor = HelloTextExtractor()
        scanner = NodeScanner(extractor, ['p', 'div'])
        regions = scanner.scan(node)
        r = regions[0]
        self.assertEqual(r.node, node.p)
        self.assertEqual(r.start_offset, 0)
        self.assertEqual(r.end_offset, 4)

    def test_find_multiple_patterns_in_distinct_elements(self):
        node = HtmlDocument('\n'.join([
            '<div>',
            '  <p>hello</p>',
            '  <p>hello</p>',
            '</div>',
            ]))
        extractor = HelloTextExtractor()
        scanner = NodeScanner(extractor, ['p'])
        regions = scanner.scan(node)
        self.assertEqual(len(regions), 2)

    def test_document_is_the_same_as_passed_in(self):
        node = HtmlDocument('<div><p>hello</p></div>')
        extractor = HelloTextExtractor()
        scanner = NodeScanner(extractor, ['p'])
        regions = scanner.scan(node)
        r = regions[0]
        self.assertEqual(
            str(r.node.parent.parent.parent),
            '<html><head></head><body><div><p>hello</p></div></body></html>'
        )

    def test_scan_same_pattern_after_inside_tag(self):
        node = HtmlDocument('\n'.join([
            '<div>',
            '  <p>hello</p>',
            '  hello',
            '</div>',
            ]))
        extractor = HelloTextExtractor()
        scanner = NodeScanner(extractor, ['p', 'div'])
        regions = scanner.scan(node)
        self.assertEqual(len(regions), 2)
        self.assertTrue(any([r.start_offset == 11 and r.end_offset == 15 for r in regions]))


class HelloTextExtractor(object):
    ''' Extractor for testing that pulls out substrings that say 'hello'. '''
    def extract(self, node):
        regions = []
        matches = re.finditer('hello', node.text)
        for m in matches:
            region = Region(node, m.start(), m.end() - 1, node.text)
            regions.append(region)
        return regions


if __name__ == '__main__':
    unittest.main()
