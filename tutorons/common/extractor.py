#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import re
from slimit.lexer import Lexer as JsLexer
import bashlex
from tutorons.css.explain import get_descendants  # TODO -- migrate this into this file


logging.basicConfig(level=logging.INFO, format="%(message)s")


class Region(object):
    '''
    Region of text that might be explainable.
    Properties:
    * node: a BeautifulSoup HTML node
    * start_offset: character index where the region begins
    * end_offset: character index where the region ends
    * string: text of the region
    '''
    def __init__(self, node, start_offset, end_offset, string):
        self.node = node
        self.start_offset = start_offset
        self.end_offset = end_offset
        self.string = string

    def __str__(self):
        return '<%s>[%d,%d]: "%s"' % \
            (self.node.name, self.start_offset, self.end_offset, self.string)

    def __repr__(self):
        return str(self)


class LineExtractor(object):

    def extract(self, node):
        ''' Given BeautifulSoup node of HTML, extract all line Regions. '''

        text = node.text

        regions = []
        char_index = 0
        for line in text.split('\n'):
            first_char = char_index
            last_char = char_index + len(line) - 1
            r = Region(node, first_char, last_char, line)
            regions.append(r)
            char_index += (len(line) + 1)  # every line has at least 1 char: the newline

        return regions


class JavascriptStringExtractor(object):

    def extract(self, node):

        lexer = JsLexer()
        lexer.input(node.text)

        regions = []
        while True:
            try:
                tok = lexer.token()
                if not tok:
                    break
                if tok.type == "STRING":
                    start_char = tok.lexpos + 1
                    string = tok.value[1:-1]
                    end_char = start_char + len(string) - 1
                    r = Region(node, start_char, end_char, string)
                    regions.append(r)
            except TypeError:
                break

        return regions


class CommandExtractor(object):
    ''' Extractor of bash simple commands. '''

    def __init__(self, cmdname):
        self.cmdname = cmdname

    def extract(self, node):

        regions = []
        text = node.text

        # bashlex doesn't like it if there's a newline at the start of the file or
        # more than one \n before a command, so we replace them with innocuous spaces
        starting_newlines = 0
        for c in text:
            if c == '\n':
                starting_newlines += 1
            else:
                break
        text = ' ' * starting_newlines + text[starting_newlines:]

        on_newline = False
        for i, c in enumerate(text):
            if on_newline:
                if c == '\n':
                    text = text[:i] + ' ' + text[i+1:]
                elif not re.match('\s', c):
                    on_newline = False
            if not on_newline:
                on_newline = (c == '\n')

        tree = bashlex.parse(text)
        nodes = get_descendants(tree)
        commands = [n for n in nodes if n.kind == 'command']

        for c in commands:
            if self._is_target_command(c, self.cmdname):
                start_char = self._get_start(c, self.cmdname)
                end_char = c.pos[1] - 1
                string = text[start_char:end_char + 1]
                r = Region(node, start_char, end_char, string)
                regions.append(r)

        return regions

    def _is_target_command(self, command, cmdname):
        for p in command.parts:
            if p.kind == 'word' and re.match(cmdname, p.word):
                return True
        return False

    def _get_start(self, command, cmdname):
        # Search for the first variable assignment or the command invocation
        for p in command.parts:
            if p.kind == 'assignment' or (p.kind and re.match(cmdname, p.word)):
                return p.pos[0]
        return -1
