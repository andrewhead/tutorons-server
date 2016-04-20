#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import ast

from tutorons.common.extractor import Region
from tutorons.packages.packages import explanations

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


class PackageFinder(ast.NodeVisitor):

    def __init__(self, package_names):
        self.calls = []
        self.package_names = package_names

    def generic_visit(self, node):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id.replace(" ", "-").lower() in self.package_names:
                self.calls.append(node)
        super(PackageFinder, self).generic_visit(node)


class PythonPackageExtractor(object):

    def extract(self, node):
        text = node.text.encode('ascii', 'ignore')
        valid_regions = []

        # Parse text into an ast tree and add all call nodes in the tree to calls
        try:
            ast_tree = ast.parse(text)
            finder = PackageFinder(explanations.keys())
            finder.visit(ast_tree)
            calls = finder.calls
        except:
            calls = []

        # Package ast nodes as region objects
        for call in calls:
            package = call.func.id
            start = find_offset(text, call)
            valid_regions.append(Region(node, start, start + len(package) - 1, package))
        return valid_regions
