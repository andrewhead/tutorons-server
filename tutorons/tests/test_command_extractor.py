#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
from bs4 import BeautifulSoup
from tutorons.common.extractor import CommandExtractor


logging.basicConfig(level=logging.INFO, format="%(message)s")


class CommandExtractorTest(unittest.TestCase):

    def test_extract_command(self):
        extractor = CommandExtractor('wget')
        node = BeautifulSoup('<code>wget http://google.com</code>')
        regions = extractor.extract(node)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.node, node)
        self.assertEqual(r.start_offset, 0)
        self.assertEqual(r.end_offset, 21)
        self.assertEqual(r.string, 'wget http://google.com')

    def test_extract_command_with_variables(self):
        extractor = CommandExtractor('wget')
        node = BeautifulSoup('<code>VAR=val wget http://google.com</code>')
        regions = extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 0)
        self.assertEqual(r.end_offset, 29)

    def test_extract_command_ignore_PS1_line(self):
        extractor = CommandExtractor('wget')
        node = BeautifulSoup('<code>my-shell$ wget http://google.com</code>')
        regions = extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 10)
        self.assertEqual(r.end_offset, 31)

    def test_extract_command_by_regex(self):
        extractor = CommandExtractor('wget(\.exe)?')
        node = BeautifulSoup('<code>my-shell$ wget.exe http://google.com</code>')
        regions = extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 10)
        self.assertEqual(r.end_offset, 35)

    def test_extract_multiple_commands(self):
        extractor = CommandExtractor('wget(\.exe)?')
        node = BeautifulSoup('\n'.join([
            '<code>',
            '    wget http://google.com',
            '    wget http://gaggle.com',
            '</code>',
        ]))
        regions = extractor.extract(node)
        self.assertEqual(len(regions), 2)

    def test_allow_many_newlines_between_commands(self):
        '''
        We include this test as bashlex doesn't like more than one newline
        charater between mulitple lines of a script.
        '''
        extractor = CommandExtractor('wget')
        node = BeautifulSoup('\n'.join([
            '<code>',
            '    wget http://google.com',
            '                          ',
            '                          ',
            '    wget http://gaggle.com',
            '</code>',
        ]))
        regions = extractor.extract(node)
        self.assertEqual(len(regions), 2)


if __name__ == '__main__':
    unittest.main()
