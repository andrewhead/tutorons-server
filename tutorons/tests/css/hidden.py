#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from tutorons.css.example import get_example
import unittest
import logging


logging.basicConfig(level=logging.INFO, format="%(message)s")


class TestGenerateExamples(unittest.TestCase):

    def test_mark_single_element(self):
        html = get_example('p', indent=1)
        self.assertEqual(html, '\n'.join([
            "<span class='tutoron_selection'>",
            "&lt;p&gt;<br>",
            "&lt;/p&gt;<br>",
            "</span>",
        ]))

    def test_mark_nested_element(self):
        html = get_example('div p', indent=1)
        self.assertEqual(html, '\n'.join([
            "&lt;div&gt;<br>",
            "<span class='tutoron_selection'>",
            "&nbsp;&lt;p&gt;<br>",
            "&nbsp;&lt;/p&gt;<br>",
            "</span>",
            "&lt;/div&gt;<br>",
        ]))

    def test_render_div_if_no_explicit_element(self):
        html = get_example('.klazz', indent=1)
        self.assertIn('div', html)

    def test_add_class_to_element(self):
        html = get_example('p.klazz', indent=1)
        self.assertIn('p class="klazz"', html)

    def test_add_id_to_element(self):
        html = get_example('p#ident', indent=1)
        self.assertIn('p id="ident"', html)

    def test_add_pseudoclass_to_element(self):
        html = get_example(':checked', indent=1)
        self.assertIn('&lt;!-- pseudoclass "checked" --&gt;', html)

    def test_add_attribute_to_element(self):
        html = get_example('input[id^=Product]', indent=1)
        self.assertIn('input id="Product"', html)

if __name__ == '__main__':
    unittest.main()
