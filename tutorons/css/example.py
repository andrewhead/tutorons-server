#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import sys
from antlr4 import CommonTokenStream, ParseTreeWalker
from antlr4.InputStream import InputStream
from antlr4.error.ErrorListener import ErrorListener
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import re

from parsers.css.CssLexer import CssLexer
from parsers.css.CssParser import CssParser
from parsers.css.CssListener import CssListener


logging.basicConfig(level=logging.INFO, format="%(message)s")


class CssExampleGenerator(CssListener, ErrorListener):
    ''' Generates pretty examples of HTML documents that will satisfy a selector. '''

    def __init__(self, indent=4, *args, **kwargs):
        super(CssExampleGenerator, self).__init__(*args, **kwargs)
        self.indent = indent
        self.results = {}
        self.invokingStates = []
        self.example = ""

    def syntaxError(self, *args, **kwargs):
        print "Syntax Error!"

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
        if len(self.results) == 0:
            return
        pret = self.prettify(self.results[self.invokingStates[-1]])
        esc = self.escape(pret)
        marked = self.formatMark(esc)
        indented = self.unindentMarks(marked)
        spaced = self.addSpaces(indented)
        self.example = spaced

    def exitNode(self, ctx):

        def _getChild(ctx, klazz):
            els = [c for c in ctx.children if isinstance(c, klazz)]
            return els[0] if len(els) > 0 else None

        element = _getChild(ctx, CssParser.ElementContext)
        if element is not None:
            el = pq('<{0}></{0}>'.format(element.getText()))
        else:
            el = pq('<div></div>')

        qualifier = _getChild(ctx, CssParser.QualifierContext)
        if qualifier is not None:
            klazz = _getChild(qualifier, CssParser.KlazzContext)
            if klazz is not None:
                el.toggleClass(klazz.getText())
            ident = _getChild(qualifier, CssParser.IdentContext)
            if ident is not None:
                el.attr('id', ident.getText())

        attr = _getChild(ctx, CssParser.AttrContext)
        if attr is not None:
            name = _getChild(attr, CssParser.AttrnameContext).getText()
            value = _getChild(attr, CssParser.AttrvalueContext).getText()
            el.attr(name, value)

        pseudoclass = _getChild(ctx, CssParser.PseudoclassContext)
        if pseudoclass is not None:
            pcn = pseudoclass.getText().replace(':', '')
            el.append('<!-- pseudoclass "{0}" -->'.format(pcn))

        childNodes = [c for c in ctx.children if isinstance(c, CssParser.NodeContext)]
        for c in childNodes:
            el.append(self.results[c.invokingState])
        if len(childNodes) == 0:
            el = self.markSelection(el)

        self.results[ctx.invokingState] = el
        self.invokingStates.append(ctx.invokingState)


def get_example(selector, indent=4):

    walker = ParseTreeWalker()
    example_generator = CssExampleGenerator(indent=indent)
    input = InputStream(selector)
    lexer = CssLexer(input)
    stream = CommonTokenStream(lexer)
    parser = CssParser(stream)
    tree = parser.selector()
    try:
        walker.walk(example_generator, tree)
    except Exception:
        return None
    return example_generator.example


if __name__ == '__main__':

    for arg in sys.argv[1:]:
        print get_example(arg)
