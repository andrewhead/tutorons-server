#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import unittest
import logging
from tutorons.wget.explain import build_help, Option, optcombo_explain, explain
from tutorons.common.scanner import InvalidCommandException


logging.basicConfig(level=logging.INFO, format="%(message)s")


class DefaultHelpMessageTest(unittest.TestCase):

    def test_describe_fetch_two_urls(self):
        command = 'wget http://google.com http://gaggle.com'
        msg = explain(command)['url']
        self.assertEqual(msg, "http://google.com and http://gaggle.com")

    def test_describe_fetch_three_urls(self):
        command = 'wget http://google.com http://gaggle.com http://giggle.com'
        msg = explain(command)['url']
        self.assertEqual(msg, "http://google.com, http://gaggle.com, and http://giggle.com")

    def test_describe_input_file_if_i_option_given(self):
        command = 'wget -i input.txt'
        msg = explain(command)['url']
        self.assertEqual(msg, "URLs from the file 'input.txt'")

    def test_describe_both_input_file_and_urls(self):
        command = 'wget -i input.txt http://google.com http://gaggle.com'
        msg = explain(command)['url']
        self.assertEqual(msg, "http://google.com, http://gaggle.com, and " +
                              "URLs from the file 'input.txt'")

    def test_throw_exception_on_non_ascii_wget_command(self):
        # The first dash below is an m-dash, not an n-dash.  This causes string
        # processing errors, which should be caught.
        with self.assertRaises(InvalidCommandException):
            command = 'wget —passive-ftp http://google.com'
            explain(command)


class BuildArgumentHelpTest(unittest.TestCase):

    def testDescribeRecursiveOption(self):
        msg = build_help(longname='--recursive')
        self.assertEqual(msg, "specify recursive download.")

    def testDescribeOutputOption(self):
        msg = build_help(longname="--output-document", value="outfile")
        self.assertEqual(msg, "write documents to outfile.")

    def testDescribeValuedOptionWithNounPrepended(self):
        msg = build_help(longname="--include-directories", value="mydir")
        self.assertEqual(msg, "mydir is a list of allowed directories.")

    def testDescribeValuedOptionWithNounAppended(self):
        msg = build_help(longname="--config", value="myfile")
        self.assertEqual(msg, "specify config file to use (FILE=myfile).")

    def testDescribeOptionByShortname(self):
        msg = build_help(shortname="-nc")
        self.assertEqual(
            msg, "skip downloads that would download to existing files (overwriting them).")


class BuildCompoundHelpTest(unittest.TestCase):

    def testNoExplanationIfNoCombos(self):
        url = "http://google.com"
        # Random grouping of non-existent arguments
        options = [
            Option('', '--tweedledee', None),
            Option('', '--tweedledum', None),
        ]
        exps = optcombo_explain(url, options)
        self.assertEqual(exps, [])

    def testDescribeUserPwCombination(self):
        url = "http://google.com"
        options = [
            Option('', '--user', 'me'),
            Option('', '--password', 'pw'),
        ]
        exps = optcombo_explain(url, options)
        self.assertEqual(exps, [
            "Authenticate at http://google.com with username 'me' and password 'pw'."
        ])

    def testDescribeRACombination(self):
        url = "http://google.com"
        options = [
            Option('-A', '--accept', '*.jpg'),
            Option('-r', '--recursive', None),
        ]
        exps = optcombo_explain(url, options)
        self.assertEqual(exps, [
            "Recursively scrape web pages linked from http://google.com of type '*.jpg'."
        ])

    def testDescribeRLCombination(self):
        url = "http://google.com"
        options = [
            Option('-l', '--level', '4'),
            Option('-r', '--recursive', None),
        ]
        exps = optcombo_explain(url, options)
        self.assertEqual(exps, [
            "Recursively scrape web pages linked from http://google.com, recursing 4 times."
        ])

    def testDescribeRALCombination(self):
        # Note that this should *not* also generate a description for RA or RL, to avoid redundancy
        url = "http://google.com"
        options = [
            Option('-l', '--level', '4'),
            Option('-A', '--accept', '*.jpg'),
            Option('-r', '--recursive', None),
        ]
        exps = optcombo_explain(url, options)
        self.assertEqual(exps, [
            "Recursively scrape web pages linked from http://google.com " +
            "of type '*.jpg', following links 4 times."
        ])


if __name__ == '__main__':
    unittest.main()
