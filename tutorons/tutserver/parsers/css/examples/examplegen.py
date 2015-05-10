#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import sys
from antlr4 import CommonTokenStream, ParseTreeWalker
from antlr4.InputStream import InputStream

from parser.CssLexer import CssLexer
from parser.CssParser import CssParser
from parser.CssListener import CssListener


logging.basicConfig(level=logging.INFO, format="%(message)s")


class CssExampleGenerator(CssListener):

    def enterSelector(self, ctx):
        print type(ctx)
        print ctx.getText()

    def enterNode(self, ctx):
        print type(ctx)
        print ctx.getText()

    def enterIdent(self, ctx):
        print type(ctx)
        print ctx.getText()


def parse(selector):

    input = InputStream(selector)
    lexer = CssLexer(input)
    stream = CommonTokenStream(lexer)
    parser = CssParser(stream)
    return parser.selector()


if __name__ == '__main__':
    
    walker = ParseTreeWalker()
    example_generator = CssExampleGenerator()

    for arg in sys.argv[1:]:
        tree = parse(arg)
        walker.walk(example_generator, tree)
