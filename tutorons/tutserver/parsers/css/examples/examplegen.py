#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import sys
from antlr4 import CommonTokenStream, ParseTreeWalker
from antlr4.InputStream import InputStream
import cgi
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import re

from parser.CssLexer import CssLexer
from parser.CssParser import CssParser
from parser.CssListener import CssListener


logging.basicConfig(level=logging.INFO, format="%(message)s")


class CssExampleGenerator(CssListener):
    ''' Generates pretty examples of HTML documents that will satisfy a selector. '''

    def __init__(self, indent=4, *args, **kwargs):
        super(CssExampleGenerator, self).__init__(*args, **kwargs)
        self.indent = indent
        self.results = {}
        self.example = None

    def prettify(self, dom):
        return BeautifulSoup(str(dom)).body.next.prettify()

    def markSelection(self, selection):
        mark = pq("<mark></mark>")
        mark.append(selection)
        return mark

    def escape(self, html):
        esc = re.sub(r"&", "&amp;", html)
        esc = re.sub(r"<(?!/?mark)", "&lt;", esc)
        esc = re.sub(r"(?<!mark)>", "&gt;", esc)
        return esc

    def formatMark(self, html):
        marked = re.sub(r"<mark>", "<span class='tutoron_selection'>", html)
        marked = re.sub(r"</mark>", "</span>", marked)
        return marked

    def unindentMarks(self, html):
        spanLevel = 0
        lines = html.split('\n')
        for i in range(0, len(lines)):
            origL = lines[i]
            if re.match(" *</span", origL):
                spanLevel -= 1
            newL = re.sub('^' + ' '*spanLevel, '', origL)
            lines[i] = newL
            if re.match(" *<span", origL):
                spanLevel += 1
        return '\n'.join(lines)

    def addSpaces(self, html):
        lines = html.split('\n')
        for i in range(0, len(lines)):
            l = lines[i]
            spaces, text = re.match('^( *)([^ ].*)', l).groups()
            if not re.match(r" *</?span", l):
                l = (len(spaces) * self.indent) * '&nbsp;' + text + "<br>"
            else:
                l = text
            lines[i] = l

        return '\n'.join(lines)

    def exitSelector(self, ctx):
        pret = self.prettify(self.results.values()[0])
        esc = self.escape(pret)
        marked = self.formatMark(esc)
        indented = self.unindentMarks(marked)
        spaced = self.addSpaces(indented)
        self.example = spaced

    def exitNode(self, ctx):

        en = ctx.children[0].getText()
        el = pq('<{0}></{0}>'.format(en))

        childNodes = [c for c in ctx.children if isinstance(c, CssParser.NodeContext)]
        for c in childNodes:
            el.append(self.results[c.invokingState])
        if len(childNodes) == 0:
            el = self.markSelection(el)

        self.results[ctx.invokingState] = el


def get_example(selector, indent=4):

    walker = ParseTreeWalker()
    example_generator = CssExampleGenerator(indent=indent)
    input = InputStream(selector)
    lexer = CssLexer(input)
    stream = CommonTokenStream(lexer)
    parser = CssParser(stream)
    tree = parser.selector()
    walker.walk(example_generator, tree)
    return example_generator.example


if __name__ == '__main__':

    for arg in sys.argv[1:]:
        print get_example(arg)
