#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import ast

from tutorons.common.extractor import Region
from tutorons.python.explain import explanations

logging.basicConfig(level=logging.INFO, format="%(message)s")


def filter_non_ascii(c):
    if ord(c) > 127:
        return ' '
    return c


def findOffset(text_list, call):
    """Takes in a text as a list and function call and finds the start of call within text"""
    offset = 0
    if call.lineno > 1:
        for l in xrange(call.lineno - 1):
            # add 1 to account for newline characters
            offset += len(text_list[l]) + 1
    offset += call.col_offset
    return offset


class BuiltInFinder(ast.NodeVisitor):
    def __init__(self):
        self.calls = []

    def generic_visit(self, node):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in explanations:
                self.calls.append(node)
        ast.NodeVisitor.generic_visit(self, node)


class PythonBuiltInExtractor(object):
    def extract(self, node):
        text = ''.join(map(filter_non_ascii, node.text))
        text_list = text.split('\n')
        valid_regions = []

        # Parse text into an ast tree and add all nodes in the tree to calls
        try:
            ast_tree = ast.parse(text)
            finder = BuiltInFinder()
            finder.visit(ast_tree)
            calls = finder.calls
        except:
            calls = []

        # Package ast nodes as region objects
        for call in calls:
            built_in = call.func.id
            start = findOffset(text_list, call)
            valid_regions.append(Region(node, start, start + len(built_in) - 1, built_in))
        return valid_regions
