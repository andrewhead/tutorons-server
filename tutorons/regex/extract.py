#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import re

from tutorons.common.extractor import Region, LineExtractor


logging.basicConfig(level=logging.INFO, format="%(message)s")


class ModRewriteRegexExtractor(LineExtractor):

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

        line_regions = super(ModRewriteRegexExtractor, self).extract(node)

        regions = []
        for r in line_regions:

            pattern = None
            if re.match('^\s*RewriteRule\s', r.string):
                pattern, offset_in_line = self._get_token(r.string, 1)
            elif re.match('^\s*RewriteCond\s', r.string):
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
        tokens = [_ for _ in re.finditer(r'(^|\s*)([^\s]*)(\s*|$)', string)]
        token_offset = 0
        for i, tok_match in enumerate(tokens):
            space_before, token, space_after = tok_match.groups()
            if i == 0:
                token_offset += len(space_before)
            if i == index:
                return (token, token_offset)
            token_offset += (len(token) + len(space_after))
        return None
