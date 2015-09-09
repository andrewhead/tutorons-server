#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest
from bs4 import BeautifulSoup

from tutorons.css.render import render


logging.basicConfig(level=logging.INFO, format="%(message)s")


class TestRenderDescription(unittest.TestCase):

    def setUp(self):
        self.test_explanation = "The selector '.klazz' chooses elements of class 'watch-view-count'"
        self.test_document = '\n'.join([
            '&lt;div class=klazz&gt;',
            '&lt;/div&gt;',
        ])

    def test_render_preamble(self):
        html = render(self.test_explanation, self.test_document)
        doc = BeautifulSoup(html)
        self.assertIn("You found a CSS selector", doc.text)
        self.assertIn("selectors pick sections of HTML pages", doc.text)

    def test_render_description(self):
        html = render(self.test_explanation, self.test_document)
        doc = BeautifulSoup(html)
        self.assertIn("chooses elements of class 'watch-view-count'", doc.text)

    def test_render_example_html(self):
        html = render(self.test_explanation, self.test_document)
        doc = BeautifulSoup(html)
        self.assertIn('\n'.join([
            '<div class=klazz>',
            '</div>',
        ]), doc.text)
