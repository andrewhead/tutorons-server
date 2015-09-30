#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import unittest

from tutorons.regex.parse import parse_regex
from tutorons.regex.nodes import InNode, RepeatNode, BranchNode,\
    LiteralNode, RangeNode, CategoryNode, AnyNode


logging.basicConfig(level=logging.INFO, format="%(message)s")


class ParseRegexTest(unittest.TestCase):

    def _get_first_child(self, tree):
        return tree.root.children[0]

    def test_character_node(self):
        tree = parse_regex('[a-z]')
        child = self._get_first_child(tree)
        self.assertEqual(type(child), InNode)

    def test_any_node(self):
        tree = parse_regex('.')
        child = self._get_first_child(tree)
        self.assertEqual(type(child), AnyNode)

    def test_category_word_node(self):
        tree = parse_regex('\w')
        cat_node = tree.root.children[0].children[0]
        self.assertEqual(type(cat_node), CategoryNode)
        self.assertEqual(cat_node.classname, "word")

    def test_category_space_node(self):
        tree = parse_regex('\s')
        cat_node = tree.root.children[0].children[0]
        self.assertEqual(type(cat_node), CategoryNode)
        self.assertEqual(cat_node.classname, "space")

    def test_repeat_question_node(self):
        tree = parse_regex('a?')
        child = self._get_first_child(tree)
        self.assertEqual(type(child), RepeatNode)
        self.assertEqual(child.min_repeat, 0)

    def test_repeat_plus_node(self):
        tree = parse_regex('a+')
        child = self._get_first_child(tree)
        self.assertEqual(type(child), RepeatNode)
        self.assertEqual(child.min_repeat, 1)

    def test_repeat_asterisk_node(self):
        tree = parse_regex('a*')
        child = self._get_first_child(tree)
        self.assertEqual(type(child), RepeatNode)
        self.assertEqual(child.min_repeat, 0)

    def test_repeat_range(self):
        tree = parse_regex('a{3,5}')
        child = self._get_first_child(tree)
        self.assertEqual(type(child), RepeatNode)
        self.assertEqual(child.min_repeat, 3)
        self.assertEqual(child.max_repeat, 5)

    def test_repeat_count_is_none_by_default(self):
        tree = parse_regex('a{3}')
        child = self._get_first_child(tree)
        self.assertEqual(type(child), RepeatNode)
        self.assertIsNone(child.repetitions)

    def test_branch_node(self):
        ''' This one is tricky -- we have to get all 'or's on the same level '''
        tree = parse_regex('abra|kadabra')
        child = self._get_first_child(tree)
        self.assertEqual(type(child), BranchNode)
        self.assertEqual(len(child.children), 2)

    def test_literal_node(self):
        tree = parse_regex('abc')
        child = self._get_first_child(tree)
        self.assertEqual(len(tree.root.children), 3)
        self.assertEqual(type(child), LiteralNode)

    def test_range_node(self):
        tree = parse_regex('[a-z]')
        rng_node = tree.root.children[0].children[0]
        self.assertEqual(type(rng_node), RangeNode)
        self.assertEqual(rng_node.lo, ord('a'))
        self.assertEqual(rng_node.hi, ord('z'))

    def test_in_node_negated(self):
        tree = parse_regex('[^a-z]')
        in_node = self._get_first_child(tree)
        self.assertTrue(in_node.negated)


class SpecialParseTest(unittest.TestCase):
    ''' Additional cases that broke our parser that we fixed. '''
    def test_parse_repeating_literal(self):
        tree = parse_regex('a+')
        rpt_node = tree.root.children[0]
        self.assertEqual(type(rpt_node), RepeatNode)
        lit_node = rpt_node.children[0]
        self.assertEqual(type(lit_node), LiteralNode)


if __name__ == '__main__':
    unittest.main()
