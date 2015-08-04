#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest
from tutorons.common.htmltools import HtmlDocument
from tutorons.css.explain import CssSelectorExtractor, explain


logging.basicConfig(level=logging.INFO, format="%(message)s")


class SelectorExtractionTest(unittest.TestCase):

    def setUp(self):
        self.extractor = CssSelectorExtractor()

    def test_extract_selector(self):
        node = HtmlDocument("<code>$('p').text('hello');</code>")
        regions = self.extractor.extract(node)
        self.assertEqual(len(regions), 1)
        r = regions[0]
        self.assertEqual(r.node, node)
        self.assertEqual(r.start_offset, 3)
        self.assertEqual(r.end_offset, 3)
        self.assertEqual(r.string, 'p')

    def test_extract_multiple(self):
        regions = self.extractor.extract(HtmlDocument("\n".join([
            "<code>",
            "    $('p').text('hello');",
            "    var input = $('input.klazz');",
            "</code",
        ])))
        self.assertEqual(len(regions), 2)

    def test_skip_non_html_element(self):
        regions = self.extractor.extract(HtmlDocument("<code>$('nothtml');</code>"))
        self.assertEqual(len(regions), 0)

    def test_skip_regular_expression(self):
        regions = self.extractor.extract(HtmlDocument("<code>var b = '^ab*';</code>"))
        self.assertEqual(len(regions), 0)


class SelectorExplanationTest(unittest.TestCase):

    def test_explain_nested_elements(self):
        exp = explain('div a')
        self.assertIn("chooses links from containers", exp)

    def test_explain_classes(self):
        exp = explain('div.klazz')
        self.assertIn("chooses containers of class 'klazz'", exp)

    def test_explain_ids(self):
        exp = explain('div#ident')
        self.assertIn("chooses a container with the ID 'ident'", exp)

    def test_explain_pseudoclass_as_state(self):
        exp = explain('input:checked')
        self.assertIn("chooses checked inputs", exp)
        exp = explain('input:hidden')
        self.assertIn("chooses hidden inputs", exp)
        exp = explain('input:visible')
        self.assertIn("chooses visible inputs", exp)
        exp = explain('input:enabled')
        self.assertIn("chooses enabled inputs", exp)
        exp = explain('a:active')
        self.assertIn("chooses active links", exp)
        exp = explain('a:visited')
        self.assertIn("chooses visited links", exp)
        exp = explain('div:empty')
        self.assertIn("chooses empty containers", exp)
        # Tricky ones requiring manual manipulation
        exp = explain('a:focus')
        self.assertIn("chooses in-focus links", exp)
        exp = explain('a:hover')
        self.assertIn("chooses hovered-over links", exp)

    def test_explain_pseudoclass_as_pseudoclass(self):
        exp = explain('input:checked')
        self.assertIn("chooses checked inputs", exp)

    def test_explain_class(self):
        exp = explain('.watch-view-count')
        self.assertEqual(
            exp, "The selector '.watch-view-count' chooses elements of class " +
            "'watch-view-count'.")

    def test_explain_pre(self):
        exp = explain('pre')
        self.assertIn("preformatted text", exp)

    def test_explain_img(self):
        exp = explain('img')
        self.assertIn("images", exp)

    def test_explain_camelcase(self):
        exp = explain('.watchView')
        self.assertIn('.watchView', exp)
