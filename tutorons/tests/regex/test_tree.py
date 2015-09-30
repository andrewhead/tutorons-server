#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest
import sre_constants

from tutorons.regex.parse import RepeatNode, GroupNode, LiteralNode, BranchNode, ChoiceNode
from tutorons.regex.tree import PatternTree


logging.basicConfig(level=logging.INFO, format="%(message)s")


class GetNodesTest(unittest.TestCase):

    def test_get_all_nodes_from_tree(self):

        rpt = RepeatNode(False, 1, 1)
        grp = GroupNode()
        lit1 = LiteralNode(ord('a'), "")
        lit2 = LiteralNode(ord('b'), "")
        rpt.children.append(grp)
        grp.children.extend([lit1, lit2])

        tree = PatternTree(rpt)
        nodes = tree.get_nodes()
        self.assertIn(rpt, nodes)
        self.assertIn(grp, nodes)
        self.assertIn(lit1, nodes)
        self.assertIn(lit2, nodes)


class GetStateAttributesTest(unittest.TestCase):

    def test_get_branch_choice(self):
        branch = BranchNode("")
        choice1 = ChoiceNode("")
        choice2 = ChoiceNode("")
        branch.children.extend([choice1, choice2])
        tree = PatternTree(branch)
        self.assertEqual(tree.get_state_attributes(), [
            (branch, 'choice'),
        ])

    def test_get_repetitions(self):
        repeat = RepeatNode(False, 1, 1)
        literal = LiteralNode(ord('a'), "")
        repeat.children.append(literal)
        tree = PatternTree(repeat)
        self.assertEqual(tree.get_state_attributes(), [
            (repeat, 'repetitions'),
        ])

    def test_get_attributes_from_multiple_levels_of_hierarchy(self):

        branch = BranchNode("")
        choice1 = ChoiceNode("")
        choice2 = ChoiceNode("")
        repeat = RepeatNode(False, 1, 1)
        literal1 = LiteralNode(ord('a'), "")
        literal2 = LiteralNode(ord('b'), "")

        branch.children.extend([choice1, choice2])
        choice1.children.append(repeat)
        repeat.children.append(literal1)
        choice2.children.append(literal2)

        tree = PatternTree(branch)
        self.assertEqual(set(tree.get_state_attributes()), set([
            (branch, 'choice'),
            (repeat, 'repetitions'),
        ]))


class StatePermutationsTest(unittest.TestCase):

    def test_get_branch_permutations(self):
        branch = BranchNode("")
        choice1 = ChoiceNode("")
        choice2 = ChoiceNode("")
        choice3 = ChoiceNode("")
        branch.children.extend([choice1, choice2, choice3])
        tree = PatternTree(branch)
        self.assertEqual(tree.get_state_permutations(), [
            ((branch, 'choice', 0),),
            ((branch, 'choice', 1),),
            ((branch, 'choice', 2),),
        ])

    def _make_repeat_tree(self, min_repeats=1, max_repeats=sre_constants.MAXREPEAT):
        repeat = RepeatNode(False, min_repeats, max_repeats)
        literal = LiteralNode(ord('a'), "")
        repeat.children.append(literal)
        tree = PatternTree(repeat)
        return tree

    def test_get_repetitions_permutations_for_unbound_range(self):
        tree = self._make_repeat_tree(1, sre_constants.MAXREPEAT)
        self.assertEqual(tree.get_state_permutations(), [
            ((tree.root, 'repetitions', 1),),
            ((tree.root, 'repetitions', 2),),
            ((tree.root, 'repetitions', 3),),
        ])

    def test_get_repetitions_permutations_for_rightbound_range(self):
        tree = self._make_repeat_tree(1, 2)
        self.assertEqual(tree.get_state_permutations(), [
            ((tree.root, 'repetitions', 1),),
            ((tree.root, 'repetitions', 2),),
        ])

    def test_get_repetitions_permutations_for_high_range(self):
        tree = self._make_repeat_tree(5, sre_constants.MAXREPEAT)
        self.assertEqual(tree.get_state_permutations(), [
            ((tree.root, 'repetitions', 5),),
            ((tree.root, 'repetitions', 6),),
            ((tree.root, 'repetitions', 7),),
        ])

    def test_permute_multiple_attributes(self):
        branch = BranchNode("")
        choice1 = ChoiceNode("")
        choice2 = ChoiceNode("")
        repeat = RepeatNode(False, 1, 2)
        literal1 = LiteralNode(ord('a'), "")
        literal2 = LiteralNode(ord('b'), "")

        branch.children.extend([choice1, choice2])
        choice1.children.append(repeat)
        repeat.children.append(literal1)
        choice2.children.append(literal2)

        tree = PatternTree(branch)
        self.assertEqual(tree.get_state_permutations(), [
            ((repeat, 'repetitions', 1), (branch, 'choice', 0)),
            ((repeat, 'repetitions', 1), (branch, 'choice', 1)),
            ((repeat, 'repetitions', 2), (branch, 'choice', 0)),
            ((repeat, 'repetitions', 2), (branch, 'choice', 1)),
        ])


class ApplyStateTest(unittest.TestCase):

    def test_apply_state_to_tree(self):

        branch = BranchNode("")
        choice1 = ChoiceNode("")
        choice2 = ChoiceNode("")
        repeat = RepeatNode(False, 1, 2)
        literal1 = LiteralNode(ord('a'), "")
        literal2 = LiteralNode(ord('b'), "")
        branch.children.extend([choice1, choice2])
        choice1.children.append(repeat)
        repeat.children.append(literal1)
        choice2.children.append(literal2)

        tree = PatternTree(branch)
        tree.set_state((
            (repeat, 'repetitions', 2),
            (branch, 'choice', 0),
        ))
        self.assertEqual(repeat.repetitions, 2)
        self.assertEqual(branch.choice, 0)
