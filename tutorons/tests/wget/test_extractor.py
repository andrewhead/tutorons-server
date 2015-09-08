#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import unittest
import logging

from tutorons.common.htmltools import HtmlDocument
from tutorons.common.scanner import InvalidCommandException
from tutorons.wget.explain import WgetExtractor
import tutorons.wget.explain as wget_explain_module


logging.basicConfig(level=logging.INFO, format="%(message)s")


class DetectWgetSyntaxTest(unittest.TestCase):

    def test_detect_if_args_in_variable(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('<code>wget $WGETPARAMS "${SITE}user"</code>'))
        self.assertEqual(len(regions), 1)

    def test_detect_if_input_file_but_no_url(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('<code>wget -i input_file.txt</code>'))
        self.assertEqual(len(regions), 1)

    def test_detect_if_wget_command_in_all_caps(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('<code>WGET http://google.com</code>'))
        self.assertEqual(len(regions), 1)

    def test_detect_if_wget_in_usr_bin_directory(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('<code>/usr/bin/wget http://google.com</code>'))
        self.assertEqual(len(regions), 1)

    def test_detect_if_url_is_in_parameter(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('<code>wget $url</code>'))
        self.assertEqual(len(regions), 1)

    def test_detect_in_crontab_entry(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('<code>*/5 * * * * wget google.com</code>'))
        r = regions[0]
        self.assertEqual(r.start_offset, 12)
        self.assertEqual(r.end_offset, 26)

    def test_detect_in_bash_script_with_leading_comments(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('\n'.join([
            "# comment",
            "wget http://gaggle.com</code>",
        ])))
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.start_offset, 10)
        self.assertEqual(r.end_offset, 31)

    def test_detect_in_bash_script_with_comments_in_middle(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('\n'.join([
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
        regions = extractor.extract(HtmlDocument('\n'.join([
            "<code>cat file.txt    ",
            "<code>wget http://gaggle.com",
        ])))
        r = regions[0]
        self.assertEqual(r.start_offset, 17)
        self.assertEqual(r.end_offset, 38)

    def test_handle_args_inside_carats(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('<code>wget -A&lt;ext&gt; &lt;URL&gt;</code>'))
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.start_offset, 0)
        self.assertEqual(r.end_offset, 17)

    def test_skip_blank_regions_but_keep_offset(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('\n'.join([
            '<code>#!/bin/sh<br>',
            'wget http://google.com',
        ])))
        r = regions[0]
        self.assertEqual(r.start_offset, 10)
        self.assertEqual(r.end_offset, 31)

    def test_skip_if_more_than_one_url_and_no_args(self):
        '''
        We suspect that if there are multiple "URLs" but no args, then this command
        is likely part of a prose sentence and not a command invokation.
        '''
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('<code>wget url1 url2</code>'))
        self.assertEqual(len(regions), 0)

    def test_detect_if_more_than_one_url_and_args_present(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('<code>wget -q url1 url2</code>'))
        self.assertEqual(len(regions), 1)

    def test_count_empty_line(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('\n'.join([
            '<span>text</span>',
            '',
            '<h1>wget url</h1>',
        ])))
        r = regions[0]
        self.assertEqual(r.start_offset, 6)
        self.assertEqual(r.end_offset, 13)

    def test_skip_all_in_bad_node(self):
        '''
        If we find a bad node (e.g., one with Unicode), we skip the full node, as
        in my experience this causes offset errors in the other regions.
        '''
        extractor = WgetExtractor()

        def _mock_run(command):
            if 'second' in command:
                raise InvalidCommandException(command, Exception)
            else:
                return "URL: http://url.com"

        orig_run_wget = wget_explain_module.run_wget
        wget_explain_module.run_wget = _mock_run
        regions = extractor.extract(HtmlDocument('\n'.join([
            '<code>',
            '  wget http://first.com',  # this m-dash should cause an exception
            '  wget http://second.com',
            '</code>',
        ])))
        wget_explain_module.run_wget = orig_run_wget
        self.assertEqual(len(regions), 0)


class IgnoreNotWgetTest(unittest.TestCase):

    def test_ignore_wgetrc(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('<code>.wgetrc</code>'))
        self.assertEqual(len(regions), 0)

    def test_ignore_if_all_words_are_arguments(self):
        extractor = WgetExtractor()
        regions = extractor.extract(HtmlDocument('<code>wget --mirror</code>'))
        self.assertEqual(len(regions), 0)


if __name__ == '__main__':
    unittest.main()
