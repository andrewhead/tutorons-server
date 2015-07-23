#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from tutorons.wget.explain import WgetExtractor
import unittest
from bs4 import BeautifulSoup
import logging


logging.basicConfig(level=logging.INFO, format="%(message)s")


class DetectWgetTest(unittest.TestCase):

    def test_detect_wget_from_wgetrc(self):
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('<code>.wgetrc</code>'))
        self.assertEqual(len(regions), 0)

    def test_ignore_if_all_words_are_arguments(self):
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('<code>wget --mirror</code>'))
        self.assertEqual(len(regions), 0)


if __name__ == '__main__':
    unittest.main()
