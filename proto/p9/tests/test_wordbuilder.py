#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import unittest
import logging
import re

from regex_examples import WordBuilder

logging.basicConfig(level=logging.INFO, format="%(message)s")


class WordBuilderTest(unittest.TestCase):

    def setUp(self):
        self.word_builder = WordBuilder(['abba'])

    def test_add_nonalpha(self):
        word = 'abba'
        chars = [
            'a', 'b',  # alphabetic
            '!'        # non-alphabetic 
        ]
        new_word = self.word_builder.add_nonalpha(word, chars, count=2)
        symbols = [c for c in new_word if c in '!']
        alphas = [c for c in new_word if c in 'ab']
        self.assertEqual(len(symbols), 2)
        self.assertEqual(len(alphas), 4)
        self.assertEqual(''.join(alphas), 'abba')


if __name__ == '__main__':
    unittest.main()
