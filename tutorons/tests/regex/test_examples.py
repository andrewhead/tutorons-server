#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import unittest
import logging
import string
import re
import mock
import sre_constants

from tutorons.regex.nodes import InNode, LiteralNode, RepeatNode, BranchNode,\
    ChoiceNode, RangeNode, NegateNode, CategoryNode, GroupNode, AnyNode
import tutorons.regex.examples as regex_examples
from tutorons.regex.examples import ExampleVisitor, get_examples


logging.basicConfig(level=logging.INFO, format="%(message)s")


class UrtestVisitorTest(unittest.TestCase):

    def setUp(self):
        dictionary = ["aaaa", "bbbb", "gfed", "yxxy"]
        self.visitor = ExampleVisitor(dictionary, messy_words=False)

    def test_visit_literal(self):
        lit_node = LiteralNode(ord('a'), "")
        msg = self.visitor.visit_node(lit_node)
        self.assertEqual(msg, 'a')

    def test_visit_in(self):
        in_node = InNode("")
        in_node.children.extend([
            LiteralNode(ord('a'), "")
        ])
        msg = self.visitor.visit_node(in_node)
        self.assertEqual(msg, "a")

    def test_visit_in_word_category(self):
        in_node = InNode("")
        in_node.children.extend([
            CategoryNode("word", ""),
        ])
        msg = self.visitor.visit_node(in_node)
        self.assertIn(msg, "".join([string.digits, string.ascii_letters]))

    def test_visit_in_space_category(self):
        in_node = InNode("")
        in_node.children.extend([
            CategoryNode("space", ""),
        ])
        msg = self.visitor.visit_node(in_node)
        self.assertIn(msg, string.whitespace)

    def test_visit_in_digit_category(self):
        in_node = InNode("")
        in_node.children.extend([
            CategoryNode("digit", ""),
        ])
        msg = self.visitor.visit_node(in_node)
        self.assertIn(msg, string.digits)

    def test_visit_branch_random_child(self):
        br_node = BranchNode("")
        choice1 = ChoiceNode("")
        choice1.children.extend([LiteralNode(ord('a'), "")])
        choice2 = ChoiceNode("")
        choice2.children.extend([LiteralNode(ord('b'), "")])
        br_node.children.extend([choice1, choice2])
        # br_node.choice = 0
        with mock.patch('random.choice', return_value=choice1):
            msg = self.visitor.visit_node(br_node)
            self.assertEqual(msg, 'a')
        with mock.patch('random.choice', return_value=choice2):
            msg = self.visitor.visit_node(br_node)
            self.assertEqual(msg, 'b')

    def test_visit_group(self):
        lit1 = LiteralNode(ord('a'), "")
        lit2 = LiteralNode(ord('b'), "")
        grp = GroupNode()
        grp.children.extend([lit1, lit2])
        msg = self.visitor.visit_node(grp)
        self.assertEqual(msg, 'ab')

    def test_visit_any_node(self):
        any_node = AnyNode()
        msg = self.visitor.visit_node(any_node)
        self.assertEqual(len(msg), 1)


class ExampleRepeatsText(unittest.TestCase):

    def setUp(self):
        self.dictionary = ["aaaa", "bbbb", "gfed", "yxxy"]
        self.visitor = ExampleVisitor(self.dictionary, messy_words=False)

    def test_visit_repeat_once_if_child_not_in_and_repetitions_not_specified(self):
        rpt_node = RepeatNode(False, 0, sre_constants.MAXREPEAT)
        grp_node = GroupNode()
        grp_node.children.extend([
            LiteralNode(ord('a'), ""),
            LiteralNode(ord('b'), ""),
        ])
        rpt_node.children.append(grp_node)
        msg = self.visitor.visit_node(rpt_node)
        self.assertEqual(msg, 'ab')

    def test_visit_repeat_literal_specified_times(self):
        rpt_node = RepeatNode(False, 2, 2)
        rpt_node.children.extend([
            LiteralNode(ord('c'), ""),
        ])
        msg = self.visitor.visit_node(rpt_node)
        self.assertEqual(msg, 'c' * 2)

    def test_visit_repeat_skip_negated_characters(self):
        rpt_node = RepeatNode(True, 2, sre_constants.MAXREPEAT)
        in_node = InNode("")
        in_node.children.extend([
            NegateNode(""),
            RangeNode(ord('a'), ord('g'), ""),
            RangeNode(ord('A'), ord('G'), ""),
        ])
        rpt_node.children.append(in_node)
        msg = self.visitor.visit_node(rpt_node)
        self.assertEqual(msg.lower(), 'yxxy')

    def test_visit_repeat_get_dict_word(self):
        rpt_node = RepeatNode(True, 1, sre_constants.MAXREPEAT)
        in_node = InNode("")
        in_node.children.extend([
            LiteralNode(ord('a'), ""),
        ])
        rpt_node.children.append(in_node)
        msg = self.visitor.visit_node(rpt_node)
        self.assertEqual(msg, "aaaa")

    def test_visit_repeat_get_random_word(self):
        rpt_node = RepeatNode(True, 1, sre_constants.MAXREPEAT)
        in_node = InNode("")
        in_node.children.extend([
            LiteralNode(ord('c'), ""),
        ])
        rpt_node.children.append(in_node)
        msg = self.visitor.visit_node(rpt_node)
        self.assertEqual(msg, 'c' * regex_examples.RANDOM_WORD_LEN)

    def test_visit_repeated_any_get_dictionary_word(self):
        rpt_node = RepeatNode(True, 1, sre_constants.MAXREPEAT)
        rpt_node.children.extend([
            AnyNode(),
        ])
        msg = self.visitor.visit_node(rpt_node)
        self.assertIn(msg.lower(), self.dictionary)

    def test_visit_repeated_word_category_get_dictionary_word(self):
        rpt_node = RepeatNode(True, 1, sre_constants.MAXREPEAT)
        rpt_node.children.extend([
            CategoryNode("word", ""),
        ])
        msg = self.visitor.visit_node(rpt_node)
        self.assertIn(msg.lower(), self.dictionary)

    def test_visit_repeat_get_dict_word_case_changed(self):
        rpt_node = RepeatNode(True, 1, sre_constants.MAXREPEAT)
        in_node = InNode("")
        in_node.children.extend([
            LiteralNode(ord('X'), ""),
            LiteralNode(ord('y'), ""),
        ])
        rpt_node.children.append(in_node)
        msg = self.visitor.visit_node(rpt_node)
        self.assertEqual(msg, "yXXy")

    def test_visit_repeat_charclass_with_literal_and_range(self):
        rpt_node = RepeatNode(True, 1, sre_constants.MAXREPEAT)
        in_node = InNode("")
        in_node.children.extend([
            LiteralNode(ord('d'), ""),
            RangeNode(ord('e'), ord('g'), ""),
        ])
        rpt_node.children.append(in_node)
        msg = self.visitor.visit_node(rpt_node)
        self.assertEqual(msg, 'gfed')


class GenerateMultipleExamplesTest(unittest.TestCase):

    def test_generate_both_branches(self):
        patt = r'aaa|bbb'
        texts = get_examples(patt, 2)
        self.assertIn('aaa', texts)
        self.assertIn('bbb', texts)

    def test_generate_multiple_repetition_counts(self):
        patt = r'a{3,4}'
        texts = get_examples(patt, 2)
        self.assertIn('aaa', texts)
        self.assertIn('aaaa', texts)


class PatternTest(unittest.TestCase):
    ''' Test common patterns as a sanity check. '''

    def test_phone_number(self):
        patt = r'\d{3}-\d{3}-\d{4}'
        text = get_examples(patt, 1)[0]
        self.assertTrue(bool(re.match(patt, text)))

    def test_mac_address(self):
        patt = r'([0-9A-F]{2}[:]){5}([0-9A-F]{2})'
        text = get_examples(patt, 1)[0]
        self.assertTrue(bool(re.match(patt, text)))

    def test_domain_with_repeated_group_and_dots(self):
        patt = "^(www.)?domain.com$"
        text = get_examples(patt, 1)[0]
        self.assertTrue(bool(re.match(patt, text)))


if __name__ == '__main__':
    unittest.main()
