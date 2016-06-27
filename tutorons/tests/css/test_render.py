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
        self.test_explanations = {
            '.klazz': "The selector '.klazz' chooses all elements of class 'klazz'"
        }
        self.test_examples = {
            '.klazz': '\n'.join([
                '&lt;div class=klazz&gt;',
                '&lt;/div&gt;',
            ])
        }

    def test_render_preamble(self):
        html = render(self.test_explanations, self.test_examples)
        doc = BeautifulSoup(html)
        self.assertIn("You found a CSS selector", doc.text)
        self.assertIn("selectors choose sections of HTML pages", doc.text)

    def test_render_description(self):
        html = render(self.test_explanations, self.test_examples)
        doc = BeautifulSoup(html)
        self.assertIn("chooses all elements of class 'klazz'", doc.text)

    def test_render_example_html(self):
        html = render(self.test_explanations, self.test_examples)
        doc = BeautifulSoup(html)
        self.assertIn('\n'.join([
            '<div class=klazz>',
            '</div>',
        ]), doc.text)
