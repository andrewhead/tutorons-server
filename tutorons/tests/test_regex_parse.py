#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest

from tutorons.regex.parse import parse_regex, InNode, RepeatNode, BranchNode,\
    LiteralNode, RangeNode, CategoryNode


logging.basicConfig(level=logging.INFO, format="%(message)s")


class ParseRegexTest(unittest.TestCase):

    def _get_first_child(self, root):
        return root.children[0]

    def test_character_node(self):
        root = parse_regex('[a-z]')
        child = self._get_first_child(root)
        self.assertEqual(type(child), InNode)

    def test_category_word_node(self):
        root = parse_regex('\w')
        cat_node = root.children[0].children[0]
        self.assertEqual(type(cat_node), CategoryNode)
        self.assertEqual(cat_node.classname, "word")

    def test_category_space_node(self):
        root = parse_regex('\s')
        cat_node = root.children[0].children[0]
        self.assertEqual(type(cat_node), CategoryNode)
        self.assertEqual(cat_node.classname, "space")

    def test_repeat_plus_node(self):
        root = parse_regex('a+')
        child = self._get_first_child(root)
        self.assertEqual(type(child), RepeatNode)
        self.assertEqual(child.min_repeat, 1)

    def test_repeat_asterisk_node(self):
        root = parse_regex('a*')
        child = self._get_first_child(root)
        self.assertEqual(type(child), RepeatNode)
        self.assertEqual(child.min_repeat, 0)

    def test_repeat_count(self):
        root = parse_regex('a{3}')
        child = self._get_first_child(root)
        self.assertEqual(type(child), RepeatNode)
        self.assertEqual(child.repetitions, 3)

    def test_branch_node(self):
        ''' This one is tricky -- we have to get all 'or's on the same level '''
        root = parse_regex('abra|kadabra')
        child = self._get_first_child(root)
        self.assertEqual(type(child), BranchNode)
        self.assertEqual(len(child.children), 2)

    def test_literal_node(self):
        root = parse_regex('abc')
        child = self._get_first_child(root)
        self.assertEqual(len(root.children), 3)
        self.assertEqual(type(child), LiteralNode)

    def test_range_node(self):
        root = parse_regex('[a-z]')
        rng_node = root.children[0].children[0]
        self.assertEqual(type(rng_node), RangeNode)
        self.assertEqual(rng_node.lo, ord('a'))
        self.assertEqual(rng_node.hi, ord('z'))

    def test_in_node_negated(self):
        root = parse_regex('[^a-z]')
        in_node = root.children[0]
        self.assertTrue(in_node.negated)


class SpecialParseTest(unittest.TestCase):
    ''' Additional cases that broke our parser that we fixed. '''
    def test_parse_repeating_literal(self):
        root = parse_regex('a+')
        rpt_node = root.children[0]
        self.assertEqual(type(rpt_node), RepeatNode)
        lit_node = rpt_node.children[0]
        self.assertEqual(type(lit_node), LiteralNode)


if __name__ == '__main__':
    unittest.main()
