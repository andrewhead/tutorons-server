#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from tutorons.wget.explain import WgetExtractor
import unittest
from bs4 import BeautifulSoup
import logging


logging.basicConfig(level=logging.INFO, format="%(message)s")


class DetectWgetSyntaxTest(unittest.TestCase):

    def test_detect_if_args_in_variable(self):
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('<code>wget $WGETPARAMS "${SITE}user"</code>'))
        self.assertEqual(len(regions), 1)

    def test_detect_if_input_file_but_no_url(self):
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('<code>wget -i input_file.txt</code>'))
        self.assertEqual(len(regions), 1)

    def test_detect_if_wget_command_in_all_caps(self):
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('<code>WGET http://google.com</code>'))
        self.assertEqual(len(regions), 1)

    def test_detect_if_wget_in_usr_bin_directory(self):
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('<code>/usr/bin/wget http://google.com</code>'))
        self.assertEqual(len(regions), 1)

    def test_detect_if_url_is_in_parameter(self):
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('<code>wget $url</code>'))
        self.assertEqual(len(regions), 1)

    def test_detect_in_crontab_entry(self):
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('<code>*/5 * * * * wget google.com</code>'))
        r = regions[0]
        self.assertEqual(r.start_offset, 12)
        self.assertEqual(r.end_offset, 26)

    def test_detect_in_bash_script_with_leading_comments(self):
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('\n'.join([
            "# comment",
            "wget http://gaggle.com</code>",
        ])))
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.start_offset, 10)
        self.assertEqual(r.end_offset, 31)

    def test_detect_in_bash_script_with_comments_in_middle(self):
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('\n'.join([
            "<code>wget http://google.com",
            "# comment",
            "wget http://gaggle.com</code>",
        ])))
        self.assertEqual(len(regions), 2)
        r2 = regions[1]
        self.assertEqual(r2.start_offset, 33)
        self.assertEqual(r2.end_offset, 54)

    def test_detect_line_after_line_with_trailing_spaces(self):
        '''
        There's a strange behavior with bashlex that it crashes when it parses a line that
        follows another line that has trailing spaces.  Through this test, we're making
        sure that detection works despite this behavior.
        '''
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('\n'.join([
            "<code>cat file.txt    ",
            "<code>wget http://gaggle.com",
        ])))
        r = regions[0]
        self.assertEqual(r.start_offset, 17)
        self.assertEqual(r.end_offset, 38)


class IgnoreNotWgetTest(unittest.TestCase):

    def test_ignore_wgetrc(self):
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('<code>.wgetrc</code>'))
        self.assertEqual(len(regions), 0)

    def test_ignore_if_all_words_are_arguments(self):
        extractor = WgetExtractor()
        regions = extractor.extract(BeautifulSoup('<code>wget --mirror</code>'))
        self.assertEqual(len(regions), 0)


if __name__ == '__main__':
    unittest.main()
