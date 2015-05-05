#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from wget_explain import PREAMBLE, build_help, explain, Option, optcombo_explain
import unittest
import logging


logging.basicConfig(level=logging.INFO, format="%(message)s")


class BuildArgumentHelpTest(unittest.TestCase):

    def testDescribeRecursiveOption(self):
        msg = build_help('--recursive')
        self.assertEqual(msg, "specify recursive download.")

    def testDescribeOutputOption(self):
        msg = build_help("--output-document", "outfile")
        self.assertEqual(msg, "write documents to outfile.")

    def testDescribeValuedOptionWithNounPrepended(self):
        msg = build_help("--include-directories", "mydir")
        self.assertEqual(msg, "mydir is a list of allowed directories.")

    def testDescribeValuedOptionWithNounAppended(self):
        msg = build_help("--config", "myfile")
        self.assertEqual(msg, "specify config file to use (FILE=myfile).")


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
            "Recursively scrape web pages linked from http://google.com of type '*.jpg', following links 4 times."
        ])


class DescribeCommandTest(unittest.TestCase):

    def testDescribeUnixExecutable(self):
        msg = explain("wget --recursive")
        self.assertEqual(msg, '\n'.join([
            PREAMBLE,
            "--recursive (-r): specify recursive download.",
            ""
        ]))

    def testAcceptPathToExecutable(self):
        msg = explain("dir1/dir2/wget --recursive")
        self.assertEqual(msg, '\n'.join([
            PREAMBLE,
            "--recursive (-r): specify recursive download.",
            ""
        ]))

    def testAcceptLongPS1Header(self):
        msg = explain("johnny-o-user:2014 05 06:>>> wget --recursive")
        self.assertEqual(msg, '\n'.join([
            PREAMBLE,
            "--recursive (-r): specify recursive download.",
            ""
        ]))

    def testDescribeWindowsExecutable(self):
        msg = explain("wget.exe --recursive")
        self.assertEqual(msg, '\n'.join([
            PREAMBLE,
            "--recursive (-r): specify recursive download.",
            ""
        ]))

    def testDescribeOptionCombination(self):
        msg = explain("wget --recursive -A *.jpg -l3 http://google.com")
        self.assertEqual(msg, '\n'.join([
            PREAMBLE + " This command downloads the page at http://google.com.",
            "Recursively scrape web pages linked from http://google.com of type '*.jpg', following links 3 times.",
            "--recursive (-r): specify recursive download.",
            "--accept (-A): *.jpg is a comma-separated list of accepted extensions.",
            "--level (-l): 3 is a maximum recursion depth (inf or 0 for infinite).",
            ""
        ]))

    def testDescribeUrl(self):
        msg = explain("wget http://google.com")
        self.assertEqual(msg, '\n'.join([
            PREAMBLE + " This command downloads the page at http://google.com.",
            ""
        ]))

    def testNoShowShortnameIfOptHasNoShortname(self):
        msg = explain("wget --retry-connrefused")
        self.assertEqual(msg, '\n'.join([
            PREAMBLE,
            "--retry-connrefused: retry even if connection is refused.",
            ""
        ]))

if __name__ == '__main__':
    unittest.main()
