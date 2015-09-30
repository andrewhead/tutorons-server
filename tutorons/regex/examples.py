#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import argparse
import logging
import random
import string
from django.conf import settings

import tutorons.regex.parse as regex_parse
from tutorons.regex.parse import InNode, RepeatNode, LiteralNode, BranchNode,\
    RangeNode, CategoryNode, AnyNode


logging.basicConfig(level=logging.INFO, format="%(message)s")
RANDOM_WORD_LEN = 5
SYMBOLS_ADDED = 2


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
    def __init__(self, dictionary, messy_words=True):
        self.word_builder = WordBuilder(dictionary)
        self.messy_words = messy_words

    def visit(self, node):
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
            return ''.join([self.visit(ch) for ch in node.children])

    def visit_repeat(self, node):
        # As far as I can tell, repeat only ever has exactly 1 child
        if isinstance(node.children[0], InNode):
            in_node = node.children[0]
            chars = get_valid_characters(in_node)
            return self.word_builder.build_word(
                chars, messy=self.messy_words, length=node.repetitions)
        else:
            node.repetitions = 1 if node.repetitions is None else node.repetitions
            return ''.join([self.visit(node.children[0]) for _ in range(node.repetitions)])

    def visit_branch(self, node):
        return self.visit(random.choice(node.children))

    def visit_in(self, node):
        chars = get_valid_characters(node)
        return self.word_builder.build_word(chars, length=1)

    def visit_literal(self, node):
        return unichr(node.value)

    def visit_any(self, node):
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
        return random.choice(printable_chars)


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


def get_valid_characters(in_node):
    if in_node.negated:
        op = lambda clist, c: clist.remove(c)
        chars = list(string.printable)
    else:
        op = lambda clist, c: clist.append(c)
        chars = []

    for child in in_node.children:
        if isinstance(child, LiteralNode):
            op(chars, unichr(child.value))
        elif isinstance(child, RangeNode):
            for val in range(child.lo, child.hi+1):
                op(chars, unichr(val))
        elif isinstance(child, CategoryNode):
            if child.classname == 'word':
                [op(chars, l) for l in string.ascii_letters]
            elif child.classname == 'space':
                [op(chars, s) for s in string.whitespace]
            elif child.classname == 'digit':
                [op(chars, s) for s in string.digits]
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
    print urtext(args.regex)
