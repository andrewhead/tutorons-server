#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import re
import copy


logging.basicConfig(level=logging.INFO, format="%(message)s")
RARE_CHARACTER = '\u3222'  # A character we never expect to appear on an HTML page


class CommandNodeDetector(object):
    '''
    Finds HTML elements in a document that contain a bash command.
    '''
    def __init__(self, command):
        self.command = command

    def detect(self, document):

        matching_nodes = []

        # The pattern we look for in the node is how we expect most PS1 headers
        # will appear, containing 3 optional components:
        # 1. leading symbols and spaces
        # 2. some alphanumeric word with underscores
        # 3. training symbols and spaces
        pattern = '^\W*(\w+)?\W*' + self.command

        # We assume that some nodes will have bash by default
        definite_nodes = document.select('code,pre')
        matching_nodes.extend(definite_nodes)

        # Other more ambiguous elements (e.g., textual) need to be checked
        checkable_nodes = document.select('p,div')
        for n in checkable_nodes:
            if self._node_has_pattern(n, pattern):
                matching_nodes.append(n)

        return matching_nodes

    def _node_has_pattern(self, node, pattern):

        ''' Make a copy of the node and split on <br> tags. '''
        node_copy = copy.copy(node)
        for br in node_copy.select('br'):
            br.replace_with(RARE_CHARACTER)
        node_text = node_copy.text
        text_blocks = node_text.split(RARE_CHARACTER)

        for block in text_blocks:
            if re.search(pattern, block):
                return True
        return False
