#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest

from tutorons.css.detect import find_jquery_selector


logging.basicConfig(level=logging.INFO, format="%(message)s")


class JquerySelectorFinderTest(unittest.TestCase):

    def test_find_internal_string(self):
        s = find_jquery_selector("     'word'     ", 5)
        self.assertEqual(s, 'word')

    def test_find_external_string(self):
        s = find_jquery_selector("     'word'     ", 7)
        self.assertEqual(s, 'word')

    def test_find_jquery_selector_offset_to_left(self):
        s = find_jquery_selector("   'word'       ", 5)
        self.assertEqual(s, 'word')

    def test_find_jquery_selector_offset_to_right(self):
        s = find_jquery_selector("       'word' ", 5)
        self.assertEqual(s, 'word')

    def test_string_in_double_quotes(self):
        s = find_jquery_selector('     "word"     ', 7)
        self.assertEqual(s, 'word')

    def test_choose_closest_quotes_from_outside(self):
        s = find_jquery_selector('     "\'word\'"     ', 3)
        self.assertEqual(s, "'word'")

    def test_choose_closest_quotes_from_inside(self):
        s = find_jquery_selector('     "\'word\'"     ', 8)
        self.assertEqual(s, 'word')

    def test_if_no_quotes_return_string(self):
        s = find_jquery_selector('   word   ', 3)
        self.assertEqual(s, 'word')
