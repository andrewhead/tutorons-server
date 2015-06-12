#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
from bs4 import BeautifulSoup
from tutorons.common.extractor import LineExtractor


logging.basicConfig(level=logging.INFO, format="%(message)s")


class ExtractLineTest(unittest.TestCase):

    def setUp(self):
        self.extractor = LineExtractor()

    def test_extract_first_line(self):
        node = BeautifulSoup('\n'.join([
            '<code>    First line</code>',
        ])).code
        regions = self.extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.node, node)
        self.assertEqual(r.start_offset, 0)
        self.assertEqual(r.end_offset, 13)
        self.assertEqual(r.string, "    First line")

    def test_extract_empty_lines(self):
        node = BeautifulSoup('\n'.join([
            '<code>',
            '   First line',
            '</code>',
        ])).code
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 3)

    def test_count_newlines_as_chars(self):
        node = BeautifulSoup('\n'.join([
            '<code>',
            '    First line',
            '</code>',
        ])).code
        regions = self.extractor.extract(node)
        r = regions[1]
        self.assertEqual(r.start_offset, 1)
        self.assertEqual(r.end_offset, 14)

    def test_extract_second_line(self):
        node = BeautifulSoup('\n'.join([
            '<code>    First line',
            '    Second line</code>',
        ])).code
        regions = self.extractor.extract(node)
        r2 = regions[1]
        self.assertEqual(r2.node, node)
        self.assertEqual(r2.start_offset, 15)
        self.assertEqual(r2.end_offset, 29)
        self.assertEqual(r2.string, "    Second line")


if __name__ == '__main__':
    unittest.main()
