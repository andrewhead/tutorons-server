#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest
from tutorons.css.explain import detect, explain


logging.basicConfig(level=logging.INFO, format="%(message)s")


class SelectorExtractionTest(unittest.TestCase):

    def test_extract_selector(self):
        selectors = detect("$('p').text('hello');")
        self.assertEqual(len(selectors), 1)
        self.assertEqual(selectors[0], 'p')

    def test_extract_multiple(self):
        selectors = detect("""
            $('p').text('hello');
            var input = $('input.klazz');
        """)
        self.assertEqual(len(selectors), 2)
        self.assertIn('input.klazz', selectors)

    def test_skip_non_html_element(self):
        selectors = detect("$('nothtml');")
        self.assertEqual(len(selectors), 0)

    def test_skip_regular_expression(self):
        selectors = detect("var b = '^ab*';")
        self.assertEqual(len(selectors), 0)


class SelectorExplanationTest(unittest.TestCase):

    def test_explain_class(self):
        exp = explain('.watch-view-count')
        self.assertEqual(exp, "The selector '.watch-view-count' chooses elements of class " +
            "'watch-view-count'.")
