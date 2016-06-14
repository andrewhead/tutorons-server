#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from antlr4 import CommonTokenStream, ParseTreeWalker
from antlr4.InputStream import InputStream


logging.basicConfig(level=logging.INFO, format="%(message)s")


def parse_plaintext(text, LexerClass, ParserClass, rule_name):
    '''
    There's half a dozen lines of boilerplate code to initialize a
    lexer, parser, and parse the plaintext into a tree.  This method
    centralizes the logic all in one place.

    Returns: the parsed tree, accessible through the rule with `rule_name`
    from the parser's grammar.
    '''
    input_ = InputStream(text)
    lexer = LexerClass(input_)
    token_stream = CommonTokenStream(lexer)
    parser = ParserClass(token_stream)
    if hasattr(parser, rule_name):
        return getattr(parser, rule_name)()
    else:
        raise KeyError("Main rule %s doesn't exist in your parser's grammar", rule_name)


def walk_tree(tree, tree_listener):
    walker = ParseTreeWalker()
    walker.walk(tree_listener, tree)
    return walker
