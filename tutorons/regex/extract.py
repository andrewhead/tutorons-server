#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import re
from slimit.lexer import Lexer as JsLexer
from slimit.parser import Parser as JsParser
import os.path
import subprocess
import bashlex

from tutorons.common.extractor import Region, LineExtractor, CommandExtractor


logging.basicConfig(level=logging.INFO, format="%(message)s")
GREP_COMMAND_PATTERN = 'grep'
GREP = os.path.join('deps', 'grep', 'src', 'grep')
SED_COMMAND_PATTERN = 'sed'
SED = os.path.join('deps', 'sed', 'sed', 'sed')


def get_arguments(command, cmd_pattern):
    ''' Given a single command, return a list of its arguments. '''

    parse_tree = bashlex.parse(command)
    cmd_node = parse_tree[0]
    args = []
    after_command = False

    for p in cmd_node.parts:
        if after_command and p.kind == 'word':
            args.append(p.word)
        elif not after_command:
            after_command = (
                p.kind == 'word' and
                bool(re.match(cmd_pattern, p.word))
            )

    return args


class GrepRegexExtractor(object):
    ''' Extracts regular expressions from grep command lines. '''

    def __init__(self):
        self.command_extractor = CommandExtractor(GREP_COMMAND_PATTERN)

    def extract(self, node):
        '''
        Regex pattern locations are NOT always exact.
        Because no positioning is returned by grep's parser, which we reuse here,
        all we can get are the patterns that will be used by grep, and then match
        these up to the first position the pattern appears in in the input command.
        '''

        GREP_REGEX_PATTERN = '(?<=Tutorons string: ).*(?=$)'
        regions = []

        command_regions = self.command_extractor.extract(node)

        for cr in command_regions:

            command = cr.string
            args = [GREP] + get_arguments(command, GREP_COMMAND_PATTERN)
            try:
                output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as cpe:
                output = cpe.output

            regexes = re.findall(GREP_REGEX_PATTERN, output, flags=re.MULTILINE)
            for r in regexes:
                start_offset = cr.start_offset + command.find(r)
                end_offset = start_offset + len(r) - 1
                region = Region(node, start_offset, end_offset, r)
                regions.append(region)

        return regions


class JavascriptRegexExtractor(object):
    ''' Extracts regular expressions from Javascript. '''

    def extract(self, node):

        lexer = JsLexer()
        lexer.input(node.text)
        regions = []

        if not self._parse_succeeds(node.text):
            return regions

        while True:
            try:
                tok = lexer.token()
                if not tok:
                    break
                if tok.type == "REGEX":
                    start_char = tok.lexpos + 1
                    regex_parts = tok.value.split('/')
                    string = regex_parts[1]
                    flags = regex_parts[2]
                    if not self._are_flags_valid(flags):
                        continue
                    end_char = start_char + len(string) - 1
                    r = Region(node, start_char, end_char, string)
                    regions.append(r)
            except (TypeError, AttributeError):
                logging.warn("Failed to parse text: %s...", node.text[:100])
                break

        return regions

    def _are_flags_valid(self, flags):

        VALID_FLAGS = ['m', 'g', 'i', 'y']
        seen_flags = []

        # If any flags are repeated, then this was likely not written as a
        # Javascript regular expression.
        for f in flags:
            if f in seen_flags or f not in VALID_FLAGS:
                return False
            seen_flags.append(f)
        return True

    def _parse_succeeds(self, text):
        try:
            parser = JsParser()
            parser.parse(text)
        except SyntaxError:
            return False
        else:
            return True


class ApacheConfigRegexExtractor(LineExtractor):
    ''' Extracts regular expressions from mod_rewrite rules. '''

    def extract(self, node):
        '''
        We parse according to the syntax from the Apache Server Version 2.2 spec:
        http://httpd.apache.org/docs/2.2/configuring.html
        1. Each line is a different directive
        2. A directive may be continued on the next line if that line ends with a backslash
            * Note that we skip this one now as it's difficult to pattern match on a line
              continuation while preserving the offset of each of the characters
        3. There can be any amount of whitespace before a directive
        4. Directives are case-insensitive

        Then we look for regular expressions in two types of commands:
        RewriteCond <TestString> <CondPattern> [flags]
        RewriteRule <Pattern> <Substitution> [flags]
        CondPattern in RewriteCond and Pattern in RewriteRule are the regular expressions.

        We will split up arguments to the directives based on whitespace.
        Because we notice that some online examples for one or the other of these have
        spaces that are escaped (\ ), then we make sure that we explictly don't split when
        there is a backslash before a single space.
        '''

        line_regions = super(self.__class__, self).extract(node)

        regions = []
        for r in line_regions:

            pattern = None
            if re.match('^\s*RewriteRule\s', r.string, re.IGNORECASE):
                pattern, offset_in_line = self._get_token(r.string, 1)
            elif re.match('^\s*RewriteCond\s', r.string, re.IGNORECASE):
                pattern, offset_in_line = self._get_token(r.string, 2)

            if pattern is not None:
                start_offset = r.start_offset + offset_in_line
                end_offset = start_offset + len(pattern) - 1
                region = Region(node, start_offset, end_offset, pattern)
                regions.append(region)

        return regions

    def _get_token(self, string, index):
        '''
        Get token of a specified index from a line of text.
        Return token and index of where it starts in the string
        '''
        tokens = [_ for _ in re.finditer(r'(^)?(\s*)([^\s]*)(\s*|$)', string)]
        token_offset = 0
        for i, tok_match in enumerate(tokens):
            start_line, space_before, token, space_after = tok_match.groups()
            if i == 0:
                token_offset += len(space_before)
            if i == index:
                return (token, token_offset)
            token_offset += (len(token) + len(space_after))
        return None


class SedRegexExtractor(object):

    def __init__(self):
        self.sed_extractor = CommandExtractor(SED_COMMAND_PATTERN)

    def extract(self, node):

        SED_ADDR_PATTERN = '(?<=Tutorons address: ).*(?=$)'
        SED_SUB_PATTERN = '^Tutorons substitution.*$'
        regions = []

        def _region_from_substring(cr, substring):
            start_offset = cr.start_offset + cr.string.find(substring)
            end_offset = start_offset + len(substring) - 1
            region = Region(node, start_offset, end_offset, substring)
            return region

        command_regions = self.sed_extractor.extract(node)
        for cr in command_regions:

            command = cr.string
            command_escaped = command.replace('\\', '\\\\')
            args = [SED] + get_arguments(command_escaped, SED_COMMAND_PATTERN)
            try:
                output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as cpe:
                output = cpe.output

            addrs = re.findall(SED_ADDR_PATTERN, output, flags=re.MULTILINE)
            for addr in addrs:
                regions.append(_region_from_substring(cr, addr))

            subst_lines = re.findall(SED_SUB_PATTERN, output, flags=re.MULTILINE)
            for line in subst_lines:
                m = re.match('^Tutorons substitution \(slash: (.)\): (.*)$', line)
                slash_char, patt = m.groups()
                patt_escaped = patt.replace(slash_char, '\\' + slash_char)
                regions.append(_region_from_substring(cr, patt_escaped))

        return regions
