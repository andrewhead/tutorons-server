#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import re
from slimit.lexer import Lexer as JsLexer
import bashlex
import copy
from tutorons.common.util import get_descendants


logging.basicConfig(level=logging.INFO, format="%(message)s")
RARE_CHARACTER = '\u3222'  # A character we never expect to appear on an HTML page


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

        ''' Save the original command, with carated arguments escaped. '''
        orig_text = node.text
        orig_text_safe = self._replace_carats(orig_text)

        ''' Make a copy of the node and split on <br> tags. '''
        node_copy = copy.copy(node)
        for br in node_copy.select('br'):
            br.replace_with(RARE_CHARACTER)
        splittable_text = node_copy.text
        text_blocks = splittable_text.split(RARE_CHARACTER)

        regions = []
        offset = 0

        for text in text_blocks:

            text = self._replace_carats(text)
            text = self._clean_for_bashlex(text)

            if not text.isspace():

                try:
                    tree = bashlex.parse(text)
                    valid_script = True
                except bashlex.errors.ParsingError:
                    valid_script = False

                if valid_script:
                    nodes = get_descendants(tree)
                    commands = [n for n in nodes if n.kind == 'command']
                    for c in commands:
                        if self._is_target_command(c, self.cmdname) and self._has_arguments(c):
                            start_char = offset + self._get_start(c, self.cmdname)
                            end_char = offset + c.pos[1] - 1
                            string = orig_text_safe[start_char:end_char + 1]
                            r = Region(node, start_char, end_char, string)
                            regions.append(r)

            offset += len(text)

        return regions

    def _has_arguments(self, command):
        return len(command.parts) > 1

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

    def _replace_carats(self, text):
        '''
        Some UNIX or online documentation puts parameter names inside of carats, e.g.,
            wget -A <ext> <URL>
        This routine replaces these edge carats, which can be misinterpreted as redirects,
        with underscores.
        '''
        return re.sub('\<(\w+)\>', r'_\1_', text)

    def _clean_for_bashlex(self, text):
        '''
        This method cleans bash script text to address 3 limitations of the bashlex library.
        1. bashlex doesn't like it if there's a newline at the start of the file or
        more than one \n before a command, so we replace them with innocuous spaces.
        2. bashlex doesn't respond well when there's comments or trailing whitespace at
        the end of a line.  So, we replace comments with a bunch of newlines, and then
        resolve the newlines with the innocuous spaces (at the starts of lines)
        3. bashlex can't parse when a line follows another line that has trailing spaces.
        So, we replace these spaces with newlines before running our newline-expansion
        procedure, which will push spaces *after* the first newline.
        '''

        replace_space = lambda m: '\n' * len(m.group())
        text = re.sub(" *$", replace_space, text, flags=re.MULTILINE)

        replace_comment = lambda m: '\n' * len(m.group())
        text = re.sub("#.*$", replace_comment, text, flags=re.MULTILINE)

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

        return text
