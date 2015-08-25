#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import re
import copy
from bs4 import Tag


logging.basicConfig(level=logging.INFO, format="%(message)s")
RARE_CHARACTER = '\u3222'  # A character we never expect to appear on an HTML page


class NodeScanner(object):
    ''' Scans document for explainable regions inside node types.'''

    def __init__(self, extractor, tags):
        self.extractor = extractor
        self.tags = tags

    def scan(self, document):
        return self.visit(document)

    def visit(self, node):

        regions = []
        children_with_regions = []

        if hasattr(node, 'children'):
            for c in node.children:
                child_regions = self.visit(c)
                regions.extend(child_regions)
                if len(child_regions) >= 1:
                    children_with_regions.append(c)

        # To avoid sensing the same explainable region twice, we literally
        # 'blank out' tags in which regions have been detected when examining
        # their parent for regions.
        if type(node) is Tag and node.name in self.tags and self.extract_allowed(node):
            node_clone = copy.copy(node)
            for c in node_clone.children:
                if c in children_with_regions:
                    c.replace_with(' ' * len(c.text))

            # As the clone is detached from the rest of the document, we need
            # to reset the region's parent node to the original node, even though
            # the text and position of the region found is the same
            node_regions = self.extractor.extract(node_clone)
            for r in node_regions:
                r.node = node

            regions.extend(node_regions)

        return regions

    def extract_allowed(self, node):
        '''
        Check preconditions before extracting from this node.
        Override this for your subclasses of scanner.
        '''
        return True


class CommandScanner(NodeScanner):
    ''' Scans HTML elements in a document that contain a bash command. '''

    def __init__(self, command, extractor, *args, **kwargs):
        self.command = command
        super(self.__class__, self).__init__(
            extractor, ['p', 'div', 'code', 'pre'], *args, **kwargs)

    def extract_allowed(self, node):

        # We assume that some nodes will have bash by default
        if node.name in ['code', 'pre']:
            return True

        # Other more ambiguous elements (e.g., textual) need to be checked
        # The pattern we look for in the node is how we expect most PS1 headers
        # will appear, containing 3 optional components:
        # 1. leading symbols and spaces
        # 2. some alphanumeric word with underscores
        # 3. training symbols and spaces
        pattern = '^\W*(\w+)?\W*' + self.command
        if node.name in ['p', 'div']:
            if self._node_has_pattern(node, pattern):
                return True

        return False

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
