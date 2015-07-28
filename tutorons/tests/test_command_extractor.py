#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
from bs4 import BeautifulSoup
from tutorons.common.extractor import CommandExtractor
from tutorons.common.node_detector import CommandNodeDetector


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

    def test_line_breaks(self):
        extractor = CommandExtractor('wget')
        node = BeautifulSoup(''.join([
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
        node = BeautifulSoup('\n'.join([
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

    def test_handles_parsing_error(self):
        extractor = CommandExtractor('wget')
        extractor.extract(BeautifulSoup('<code>os.system("wget google.com")</code>'))

    def test_extract_includes_redirect(self):
        extractor = CommandExtractor('wget')
        node = BeautifulSoup("<code>wget google.com > /dev/null 2>&1</code>")
        regions = extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 0)
        self.assertEqual(r.end_offset, 31)

    def test_extract_from_crontab(self):
        extractor = CommandExtractor('wget')
        node = BeautifulSoup("<code>*/5 * * * * wget mysite.com</code>")
        regions = extractor.extract(node)
        r = regions[0]
        self.assertEqual(r.start_offset, 12)
        self.assertEqual(r.end_offset, 26)

    def test_ignore_command_name_without_options(self):
        extractor = CommandExtractor('wget')
        node = BeautifulSoup('<code>wget</code>')
        regions = extractor.extract(node)
        self.assertEqual(len(regions), 0)


class CommandElementDetectionTest(unittest.TestCase):

    def test_identify_paragraph_with_one_line_command(self):
        det = CommandNodeDetector('wget')
        document = BeautifulSoup('<p>wget http://google.com</p>')
        nodes = det.detect(document)
        self.assertEqual(len(nodes), 1)

    def test_identify_div_with_wget(self):
        det = CommandNodeDetector('wget')
        document = BeautifulSoup('<div>wget http://google.com</div>')
        nodes = det.detect(document)
        self.assertEqual(len(nodes), 1)

    def test_identify_paragraph_with_PS1_header(self):
        det = CommandNodeDetector('wget')
        document = BeautifulSoup('<p>$ wget http://google.com</p>')
        nodes = det.detect(document)
        self.assertEqual(len(nodes), 1)

    def test_identify_paragraph_with_command_after_break(self):
        det = CommandNodeDetector('wget')
        document = BeautifulSoup('<p>Some descriptive text<br/>$ wget http://google.com</p>')
        nodes = det.detect(document)
        self.assertEqual(len(nodes), 1)

    def test_miss_wget_in_unsupported_element_type(self):
        det = CommandNodeDetector('wget')
        document = BeautifulSoup('<i>wget http://google.com</i>')
        nodes = det.detect(document)
        self.assertEqual(len(nodes), 0)

    def test_miss_paragraph_without_command(self):
        det = CommandNodeDetector('wget')
        document = BeautifulSoup('<p>This line does not have a command on it.</p>')
        nodes = det.detect(document)
        self.assertEqual(len(nodes), 0)

    def test_miss_paragraph_with_text_preceding_command(self):
        det = CommandNodeDetector('wget')
        document = BeautifulSoup('<p>Just run wget http://google.com</p>')
        nodes = det.detect(document)
        self.assertEqual(len(nodes), 0)

    def test_detect_any_code_block(self):
        det = CommandNodeDetector('wget')
        document = BeautifulSoup('<code></code>')
        nodes = det.detect(document)
        self.assertEqual(len(nodes), 1)

    def test_detect_any_pre_block(self):
        det = CommandNodeDetector('wget')
        document = BeautifulSoup('<pre></pre>')
        nodes = det.detect(document)
        self.assertEqual(len(nodes), 1)


if __name__ == '__main__':
    unittest.main()
