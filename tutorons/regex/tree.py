#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import itertools

from tutorons.regex.nodes import BranchNode, RepeatNode


logging.basicConfig(level=logging.INFO, format="%(message)s")


class PatternTree(object):

    def __init__(self, root):
        self.root = root

    def get_nodes(self):
        ''' Collect all nodes of a Regex parse tree. '''
        return self._get_node_descendants(self.root)

    def _get_node_descendants(self, node):
        desc = []
        for c in node.children:
            desc.extend(self._get_node_descendants(c))
        desc.append(node)
        return desc

    def get_state_attributes(self):
        '''
        Get all attributes of the nodes of the patterns that, when changed
        will alter the types of examples that can be generated for this tree.
        Examples are which branch is selected and the number or repetitions
        of a subpattern.
        Returns a list of (node, attribute-name) tuples.
        '''
        nodes = self.get_nodes()
        attributes = []
        for n in nodes:
            if isinstance(n, BranchNode):
                attributes.append((n, 'choice'))
            elif isinstance(n, RepeatNode):
                attributes.append((n, 'repetitions'))
        return attributes

    def get_state_permutations(self):
        '''
        Get all combinations of tree states that will alter the types of examples
        that can be generated for a tree.
        Returns a list of lists of assignments, where each item is:
        (node, attribute-name, value)
        And each list is a 'state', or a set of assignments that can be applied to a tree
        to prepare it for example generation.
        For now, different assignments are limited in the following ways:
        * repetitions can only be any value between [lower_bound:min(lower_bound+2, upper_bound)]
        '''
        states = []
        attributes = self.get_state_attributes()

        val_generator = AttributeValueGenerator()
        for attr in attributes:
            values = val_generator.get_values(attr)
            states.append([attr + (val,) for val in values])

        permutations = [_ for _ in itertools.product(*states)]
        return permutations

    def set_state(self, state):
        '''
        Apply a list of state attributes and values to the nodes in a tree.
        The list should be one that was returned by the
        get_state_permutations() method.
        '''
        for node, attr, value in state:
            setattr(node, attr, value)


class AttributeValueGenerator(object):
    '''
    Visitor that visits node attributes to generate the possible values it can take
    on when generating examples that satisfy the pattern.
    '''

    def get_values(self, attribute):
        node, attrname = attribute
        if isinstance(node, BranchNode) and attrname == 'choice':
            return self.get_branch_choices(node)
        elif isinstance(node, RepeatNode) and attrname == 'repetitions':
            return self.get_repetition_counts(node)

    def get_branch_choices(self, branch_node):
        return range(0, len(branch_node.children))

    def get_repetition_counts(self, rep_node):
        MAX_NUM_COUNTS = 3
        range_size = rep_node.max_repeat - rep_node.min_repeat + 1
        num_counts = min(range_size, MAX_NUM_COUNTS)
        return range(rep_node.min_repeat, rep_node.min_repeat + num_counts)
