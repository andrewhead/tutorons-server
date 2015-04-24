#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import argparse
import regex_parse
from regex_parse import InNode, RepeatNode, LiteralNode, BranchNode, RangeNode
import logging
import random


logging.basicConfig(level=logging.INFO, format="%(message)s")
RANDOM_WORD_LEN = 5


def urtext(regex, dictionary=None):
    '''
    Generate representative, readable example of string that matches a regular expression.
    If dictionary is set to None, use the default dictionary.
    '''
    tree = regex_parse.parse_regex(regex)
    dictionary = get_default_dict() if dictionary is None else dictionary
    urtext_visitor = UrtextVisitor(dictionary)
    message = urtext_visitor.visit(tree)
    return message


class UrtextVisitor(object):
    ''' 
    Visitor for parsed regular expression that generates a representative, readable example of a 
    string that matches the regular expression.
    '''
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def visit(self, node):
        if isinstance(node, RepeatNode):
            return self.visit_repeat(node)
        elif isinstance(node, InNode):
            return self.visit_in(node)
        elif isinstance(node, LiteralNode):
            return self.visit_literal(node)
        elif isinstance(node, BranchNode):
            return self.visit_branch(node)
        else:
            return ''.join([self.visit(ch) for ch in node.children])

    def visit_repeat(self, node):
        # As far as I can tell, repeat only ever has exactly 1 child
        if isinstance(node.children[0], InNode):
            # We assume that InNodes only have literals as children
            # If we can, we get a dictionary word that satisfies the pattern.
            # Otherwise, return a random word
            in_node = node.children[0]
            chars = []
            for child in in_node.children:
                if isinstance(child, LiteralNode):
                    chars.append(unichr(child.value))
                elif isinstance(child, RangeNode):
                    chars.extend([unichr(val) for val in range(child.lo, child.hi+1)])
            dict_shuffled = sorted(self.dictionary, key=lambda k: random.random())
            for term in dict_shuffled:
                match = all([c in chars for c in term])
                if match:
                    return term
            return ''.join([random.choice(chars) for _ in range(RANDOM_WORD_LEN)])
        else:
            return self.visit(node.children[0]) * node.repetitions
           
    def visit_branch(self, node):
        return self.visit(node.children[node.choice])

    def visit_in(self, node):
        pass

    def visit_literal(self, node):
        return unichr(node.value)


def get_default_dict():
    ''' Get a default dictionary of readable words. '''
    terms = []
    with open('dict.txt') as dict_file:
        for t in dict_file.readlines():
            t_stripped = t.strip()
            if len(t_stripped) in range(4, 7):
                terms.append(t_stripped)
    return terms


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description=
        "Generate readable string that satisfies a regular expression.")
    argparser.add_argument('regex', help="regular expression")
    args = argparser.parse_args()
    print urtext(args.regex)
