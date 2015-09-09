#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import unittest
import logging
from bs4 import BeautifulSoup

from tutorons.wget.explain import Option
from tutorons.wget.render import render


logging.basicConfig(level=logging.INFO, format="%(message)s")


class TestRenderDescription(unittest.TestCase):

    def test_describe_one_command(self):
        html = render('http://hello.html')
        doc = BeautifulSoup(html)
        self.assertIn(
            "Here, it downloads content from http://hello.html.", doc.text)

    def test_describe_options(self):
        html = render('http://hello.html', options=[
            Option('-A', '--accept', '*.jpg',
                   "*.jpg is a comma-separated list of accepted extensions."),
            Option('-l', '--level', '3',
                   "3 is a maximum recursion depth (inf or 0 for infinite)"),
        ])
        doc = BeautifulSoup(html)
        self.assertIn("<p>It uses these options:</p>", str(doc))
        self.assertIn("--accept", doc.text)
        self.assertIn("-A", doc.text)
        self.assertIn(": *.jpg is a comma-separated list of accepted extensions.", doc.text)
        self.assertIn("3 is a maximum recursion depth (inf or 0 for infinite)", doc.text)

    def test_describe_option_combination(self):
        html = render('http://hello.html', optcombos=[
            "Recursively scrape web pages linked from http://google.com of type '*.jpg', " +
            "following links 3 times.",
        ])
        doc = BeautifulSoup(html)
        self.assertIn(
            "Recursively scrape web pages linked from http://google.com of type '*.jpg', " +
            "following links 3 times.",
            doc.text)

    def test_no_show_shortname_if_opt_has_no_shortname(self):
        html = render('http://hello.html', options=[
            Option(None, '--accept', '*.jpg',
                   "*.jpg is a comma-separated list of accepted extensions."),
        ])
        doc = BeautifulSoup(html)
        self.assertIn('--accept:', doc.text)
