#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import ast

from tutorons.common.extractor import Region
from tutorons.python.builtins import explanations

logging.basicConfig(level=logging.INFO, format="%(message)s")


def find_offset(text, call):
    """Takes in a text and function call and finds the start of call within text"""
    text_list = text.split('\n')
    offset = 0
    for l in range(call.lineno - 1):
        # add 1 to account for newline characters
        offset += len(text_list[l]) + 1
    offset += call.col_offset
    return offset


class BuiltInFinder(ast.NodeVisitor):

    def __init__(self, builtin_names):
        self.calls = []
        self.builtin_names = builtin_names

    def generic_visit(self, node):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in self.builtin_names:
                self.calls.append(node)
        super(BuiltInFinder, self).generic_visit(node)


class PythonBuiltInExtractor(object):

    def extract(self, node):
        text = node.text.encode('ascii', 'ignore')
        valid_regions = []

        # Parse text into an ast tree and add all call nodes in the tree to calls
        try:
            ast_tree = ast.parse(text)
            finder = BuiltInFinder(explanations.keys())
            finder.visit(ast_tree)
            calls = finder.calls
        except:
            calls = []

        # Package ast nodes as region objects
        for call in calls:
            built_in = call.func.id
            start = find_offset(text, call)
            valid_regions.append(Region(node, start, start + len(built_in) - 1, built_in))
        return valid_regions
