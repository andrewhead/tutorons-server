#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
from tutorons.common.htmltools import HtmlDocument
from tutorons.common.extractor import CommandExtractor
from tutorons.common.scanner import CommandScanner


logging.basicConfig(level=logging.INFO, format="%(message)s")


class CommandExtractorTest(unittest.TestCase):

    def test_extract_command(self):
        extractor = CommandExtractor('wget')
        node = HtmlDocument('<code>wget http://google.com</code>')
        regions = extractor.extract(node)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.node, node)
        self.assertEqual(r.start_offset, 0)
        self.assertEqual(r.end_offset, 21)
        self.assertEqual(r.string, 'wget http://google.com')

    def test_extract_command_with_variables(self):
        extractor = CommandExtractor('wget')
        node = HtmlDocument('<code>VAR=val wget http://google.com</code>')
        regions = extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 0)
        self.assertEqual(r.end_offset, 29)

    def test_line_breaks(self):
        extractor = CommandExtractor('wget')
        node = HtmlDocument(''.join([
            '<code>$  wget http://google.com<br> ',
            '$  wget http://gaggle.com</code>'
        ]))
        regions = extractor.extract(node)
        r1 = regions[0]
        self.assertEqual(r1.start_offset, 3)
        self.assertEqual(r1.end_offset, 24)
        r2 = regions[1]
        self.assertEqual(r2.start_offset, 29)
        self.assertEqual(r2.end_offset, 50)

    def test_extract_command_ignore_PS1_line(self):
        extractor = CommandExtractor('wget')
        node = HtmlDocument('\n'.join([
            '<code>',
            'my-shell$ wget http://google.com',
            'my-shell$ wget http://gaggle.com',
            '</code>',
        ]))
        regions = extractor.extract(node)
        r1 = regions[0]
        self.assertEqual(r1.start_offset, 11)
        self.assertEqual(r1.end_offset, 32)
        r2 = regions[1]
        self.assertEqual(r2.start_offset, 44)
        self.assertEqual(r2.end_offset, 65)

    def test_extract_command_by_regex(self):
        extractor = CommandExtractor('wget(\.exe)?')
        node = HtmlDocument('<code>my-shell$ wget.exe http://google.com</code>')
        regions = extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 10)
        self.assertEqual(r.end_offset, 35)

    def test_extract_multiple_commands(self):
        extractor = CommandExtractor('wget(\.exe)?')
        node = HtmlDocument('\n'.join([
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
        node = HtmlDocument('\n'.join([
            '<code>',
            '    wget http://google.com',
            '                          ',
            '                          ',
            '    wget http://gaggle.com',
            '</code>',
        ]))
        regions = extractor.extract(node)
        self.assertEqual(len(regions), 2)

    def test_handles_parsing_error(self):
        extractor = CommandExtractor('wget')
        extractor.extract(HtmlDocument('<code>os.system("wget google.com")</code>'))

    def test_extract_includes_redirect(self):
        extractor = CommandExtractor('wget')
        node = HtmlDocument("<code>wget google.com > /dev/null 2>&1</code>")
        regions = extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 0)
        self.assertEqual(r.end_offset, 31)

    def test_extract_from_crontab(self):
        extractor = CommandExtractor('wget')
        node = HtmlDocument("<code>*/5 * * * * wget mysite.com</code>")
        regions = extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 12)
        self.assertEqual(r.end_offset, 26)

    def test_ignore_command_name_without_options(self):
        extractor = CommandExtractor('wget')
        node = HtmlDocument('<code>wget</code>')
        regions = extractor.extract(node)
        self.assertEqual(len(regions), 0)


class CommandScannerTest(unittest.TestCase):

    def setUp(self):
        self.scanner = CommandScanner('wget', CommandExtractor('wget'))

    def test_identify_paragraph_with_one_line_command(self):
        document = HtmlDocument('<p>wget http://google.com</p>')
        regions = self.scanner.scan(document)
        self.assertEqual(len(regions), 1)

    def test_identify_div_with_wget(self):
        document = HtmlDocument('<div>wget http://google.com</div>')
        regions = self.scanner.scan(document)
        self.assertEqual(len(regions), 1)

    def test_identify_paragraph_with_PS1_header(self):
        document = HtmlDocument('<p>$ wget http://google.com</p>')
        regions = self.scanner.scan(document)
        self.assertEqual(len(regions), 1)

    def test_identify_paragraph_with_command_after_break(self):
        document = HtmlDocument('<p>Some descriptive text<br/>$ wget http://google.com</p>')
        regions = self.scanner.scan(document)
        self.assertEqual(len(regions), 1)

    def test_miss_wget_in_unsupported_element_type(self):
        document = HtmlDocument('<i>wget http://google.com</i>')
        regions = self.scanner.scan(document)
        self.assertEqual(len(regions), 0)

    def test_miss_paragraph_without_command(self):
        document = HtmlDocument('<p>This line does not have a command on it.</p>')
        regions = self.scanner.scan(document)
        self.assertEqual(len(regions), 0)

    def test_miss_paragraph_with_text_preceding_command(self):
        document = HtmlDocument('<p>Just run wget http://google.com</p>')
        regions = self.scanner.scan(document)
        self.assertEqual(len(regions), 0)

    def test_detect_wget_in_code_block(self):
        document = HtmlDocument('<code>wget http://google.com</code>')
        regions = self.scanner.scan(document)
        self.assertEqual(len(regions), 1)

    def test_detect_wget_in_pre_block(self):
        document = HtmlDocument('<pre>wget http://google.com</pre>')
        regions = self.scanner.scan(document)
        self.assertEqual(len(regions), 1)


if __name__ == '__main__':
    unittest.main()
