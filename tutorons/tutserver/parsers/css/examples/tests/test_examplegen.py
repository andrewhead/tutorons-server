#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from parsers.css.examples.examplegen import get_example
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
    

if __name__ == '__main__':
    unittest.main()
