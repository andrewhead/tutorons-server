#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import unittest
import logging

from regex_parse import InNode, LiteralNode, RepeatNode, BranchNode, ChoiceNode, RangeNode
import regex_examples
from regex_examples import UrtextVisitor


logging.basicConfig(level=logging.INFO, format="%(message)s")


class UrtestVisitorTest(unittest.TestCase):
 
    def setUp(self):
        dictionary = ["aaaa", "bbbb", "gfed"]
        self.visitor = UrtextVisitor(dictionary)

    def test_visit_literal(self):
        lit_node = LiteralNode(ord('a'), "")
        msg = self.visitor.visit(lit_node)
        self.assertEqual(msg, 'a')

    def test_visit_repeat_get_dict_word(self):
        rpt_node = RepeatNode(1, "")
        in_node = InNode("")
        in_node.children.extend([
            LiteralNode(ord('a'), ""),
        ])
        rpt_node.children.append(in_node)
        msg = self.visitor.visit(rpt_node)
        self.assertEqual(msg, "aaaa")

    def test_visit_repeat_get_random_word(self):
        rpt_node = RepeatNode(1, "")
        in_node = InNode("")
        in_node.children.extend([
            LiteralNode(ord('c'), ""),
        ])
        rpt_node.children.append(in_node)
        msg = self.visitor.visit(rpt_node)
        self.assertEqual(msg, 'c' * regex_examples.RANDOM_WORD_LEN)

    def test_visit_repeat_charclass_with_literal_and_range(self):
        rpt_node = RepeatNode(1, "")
        in_node = InNode("")
        in_node.children.extend([
            LiteralNode(ord('d'), ""),
            RangeNode(ord('e'), ord('g'), ""),
        ])
        rpt_node.children.append(in_node)
        msg = self.visitor.visit(rpt_node)
        self.assertEqual(msg, 'gfed')

    def test_visit_repeat_literal_specified_times(self):
        rpt_node = RepeatNode(1, "")
        rpt_node.repetitions = 2
        rpt_node.children.extend([
            LiteralNode(ord('c'), ""),
        ])
        msg = self.visitor.visit(rpt_node)
        self.assertEqual(msg, 'c' * 2)

    def test_visit_branch_first_child(self):
        br_node = BranchNode("")
        choice1 = ChoiceNode("")
        choice1.children.extend([LiteralNode(ord('a'), "")])
        choice2 = ChoiceNode("")
        choice2.children.extend([LiteralNode(ord('b'), "")])
        br_node.children.extend([choice1, choice2])
        br_node.choice = 0
        msg = self.visitor.visit(br_node)
        self.assertEqual(msg, 'a')

    def test_visit_branch_last_child(self):
        br_node = BranchNode("")
        choice1 = ChoiceNode("")
        choice1.children.extend([LiteralNode(ord('a'), "")])
        choice2 = ChoiceNode("")
        choice2.children.extend([LiteralNode(ord('b'), "")])
        br_node.children.extend([choice1, choice2])
        br_node.choice = 1
        msg = self.visitor.visit(br_node)
        self.assertEqual(msg, 'b')


if __name__ == '__main__':
    unittest.main()
