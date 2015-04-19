#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest
from regex_examples import parse_regex
from regex_examples import InNode, RepeatNode, BranchNode


logging.basicConfig(level=logging.INFO, format="%(message)s")


class ParseRegexTest(unittest.TestCase):

    def _get_first_child(self, root):
        return root.children[0]

    def test_character_node(self):
        root = parse_regex('[a-z]')
        child = self._get_first_child(root)
        self.assertEqual(type(child), InNode)

    def test_repeat_node(self):
        root = parse_regex('a+')
        child = self._get_first_child(root)
        self.assertEqual(type(child), RepeatNode)
        self.assertEqual(child.min_repeat, 1)

    def test_asterisk_node(self):
        root = parse_regex('a*')
        child = self._get_first_child(root)
        self.assertEqual(type(child), RepeatNode)
        self.assertEqual(child.min_repeat, 0)

    def test_branch_node(self):
        ''' This one is tricky -- we have to get all 'or's on the same level '''
        root = parse_regex('abra|kadabra')
        child = self._get_first_child(root)
        self.assertEqual(type(child), BranchNode)
        self.assertEqual(len(child.children), 2)

    def test_literal_node(self):
        pass


if __name__ == '__main__':
    unittest.main()

