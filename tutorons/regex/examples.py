#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import argparse
import logging
import random
import string
from django.conf import settings
import sre_constants

import tutorons.regex.parse as regex_parse
from tutorons.regex.nodes import InNode, RepeatNode, LiteralNode, BranchNode,\
    RangeNode, CategoryNode, AnyNode


logging.basicConfig(level=logging.INFO, format="%(message)s")
RANDOM_WORD_LEN = 5
SYMBOLS_ADDED = 2


def get_examples(regex, count=1, dictionary=None):
    '''
    Generate representative, readable examples of string that matches a regular expression.
    If dictionary is set to None, use the default dictionary.
    '''
    tree = regex_parse.parse_regex(regex)
    dictionary = get_default_dict() if dictionary is None else dictionary
    example_visitor = ExampleVisitor(dictionary)

    examples = []
    state_permutations = tree.get_state_permutations()
    random.shuffle(state_permutations)
    for perm in state_permutations[:count]:
        tree.set_state(perm)
        example = example_visitor.visit(tree)
        examples.append(example)

    return examples


class ExampleVisitor(object):
    '''
    Visitor for parsed regular expression that generates a representative, readable example of a
    string that matches the regular expression.
    '''
    def __init__(self, dictionary, messy_words=True):
        self.word_builder = WordBuilder(dictionary)
        self.messy_words = messy_words

    def visit(self, tree):
        return self.visit_node(tree.root)

    def visit_node(self, node):
        if isinstance(node, RepeatNode):
            return self.visit_repeat(node)
        elif isinstance(node, InNode):
            return self.visit_in(node)
        elif isinstance(node, LiteralNode):
            return self.visit_literal(node)
        elif isinstance(node, BranchNode):
            return self.visit_branch(node)
        elif isinstance(node, AnyNode):
            return self.visit_any(node)
        else:
            return ''.join([self.visit_node(ch) for ch in node.children])

    def visit_repeat(self, node):
        # As far as I can tell, a repeat node only ever has exactly 1 child
        child = node.children[0]
        reps = node.repetitions
        if (isinstance(child, InNode) or
                isinstance(child, AnyNode) or
                isinstance(child, CategoryNode) and child.classname == 'word'):
            messy = self.messy_words if isinstance(child, InNode) else False
            chars = get_valid_characters(child)
            if reps is None and node.max_repeat != sre_constants.MAXREPEAT:
                reps = node.min_repeat
            return self.word_builder.build_word(chars, messy=messy, length=reps)
        else:
            reps = max(1, node.min_repeat) if reps is None else reps
            return ''.join([self.visit_node(child) for _ in range(reps)])

    def visit_branch(self, node):
        if node.choice is None:
            chosen_child = random.choice(node.children)
        else:
            chosen_child = node.children[node.choice]
        return self.visit_node(chosen_child)

    def visit_in(self, node):
        chars = get_valid_characters(node)
        return self.word_builder.build_word(chars, length=1)

    def visit_literal(self, node):
        return unichr(node.value)

    def visit_any(self, node):
        return random.choice(get_valid_characters(node))


class WordBuilder(object):

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def build_word(self, chars, length=None, messy=True):
        if length:
            return ''.join([random.choice(chars) for _ in range(length)])
        else:
            word = self._get_dict_term(chars)
            if messy:
                word = self.add_nonalpha(word, chars)
            return word

    def add_nonalpha(self, word, chars, count=2):
        non_alpha = list(set(chars) - set(string.ascii_letters))
        new_word = list(word)
        if len(non_alpha) > 0:
            for _ in range(count):
                rand_symbol = random.choice(non_alpha)
                rand_index = random.randint(0, len(word))
                new_word.insert(rand_index, rand_symbol)
        return ''.join(new_word)

    def _get_dict_term(self, chars):

        # If we can, we get a dictionary word that satisfies the pattern.
        # Otherwise, return a random word
        dict_shuf = sorted(self.dictionary, key=lambda k: random.random())
        chars_lower = [c.lower() for c in chars]

        # We match with lower-case versions of dictionary words.  If it
        # matches, then we shift the output to be mixed upper and lower
        # as specified by the pattern
        for term in dict_shuf:
            term = term.lower()
            match = all([c in chars_lower for c in term])
            if match:
                clist = list(term)
                for i in range(len(clist)):
                    c = clist[i]
                    if c.upper() in chars and c.lower() in chars:
                        clist[i] = random.choice([c.upper(), c.lower()])
                    elif c.upper() in chars:
                        clist[i] = c.upper()
                    elif c.lower() in chars:
                        clist[i] = c.lower()
                return ''.join(clist)
        return self._make_random_word(chars)

    def _make_random_word(self, chars):
        # Try to make readable word by only using alphanumeric chars.
        choices = list(set(chars).intersection(set(string.ascii_letters)))
        if len(choices) == 0:
            return ''
        else:
            return ''.join([random.choice(choices) for _ in range(RANDOM_WORD_LEN)])


def get_valid_characters(node):
    ''' Get the list of characters that can be used to match a character node. '''

    if isinstance(node, InNode):
        if node.negated:
            op = lambda clist, c: clist.remove(c)
            chars = list(string.printable)
        else:
            op = lambda clist, c: clist.append(c)
            chars = []
        for child in node.children:
            child_chars = get_valid_characters(child)
            for cc in child_chars:
                op(chars, cc)

    elif isinstance(node, LiteralNode):
        return [unichr(node.value)]

    elif isinstance(node, RangeNode):
        return [unichr(val) for val in range(node.lo, node.hi+1)]

    elif isinstance(node, CategoryNode):
        if node.classname == 'word':
            return string.ascii_letters
        elif node.classname == 'space':
            return string.whitespace
        elif node.classname == 'digit':
            return string.digits
        else:
            return []

    elif isinstance(node, AnyNode):
        # According to Python documentation:
        # '.', in the default mode, matches any character except a newline.
        # - (https://docs.python.org/2/library/re.html)
        # We approximate this by replace a 'dot' with a character from the 'printable'
        #  attribute of the 'string' module, ignoring characters that will insert
        #  new lines to make sure that examples can be read on one line.
        NEWLINE_CHARS = ['\n', '\r', '\x0b', '\x0c']
        printable_chars = string.printable
        for char in NEWLINE_CHARS:
            printable_chars.replace(char, '')
        return printable_chars

    else:
        return []

    return chars


def get_default_dict():
    ''' Get a default dictionary of readable words. '''
    terms = []
    with open(settings.DEFAULT_DICTIONARY) as dict_file:
        for t in dict_file.readlines():
            t_stripped = t.strip()
            if len(t_stripped) in range(4, 7):
                terms.append(t_stripped)
    return terms


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description="Generate readable string that satisfies a regular expression.")
    argparser.add_argument('regex', help="regular expression")
    args = argparser.parse_args()
    print get_examples(args.regex)
