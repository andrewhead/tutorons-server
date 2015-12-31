#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import ast

from tutorons.common.extractor import Region
from tutorons.python.explain import explanations

logging.basicConfig(level=logging.INFO, format="%(message)s")
# TODO add real explanations for python docs
# TODO better variable, method naming

def filter_non_ascii(c):
    if ord(c) > 127:
        return ' '
    return c

def findOffset(text_list, call):
    # Takes in a text as a list and a call and finds the start of call within text
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

    # def generic_visit(self, node):
    #     if isinstance(node, ast.Call) and node.func.id in explanations:
    #         self.calls.append(node)
    #     ast.NodeVisitor.generic_visit(self, node)

    def generic_visit(self, node):
        print self.calls
        print node
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            print node.func.id
            if node.func.id in explanations:
                print "found builtin!!"
                self.calls.append(node)
        ast.NodeVisitor.generic_visit(self, node)

class PythonBuiltInExtractor(object):
    def extract(self, node):
        text = ''.join(map(filter_non_ascii, node.text))
        text_list = text.split('\n')
        offset = 0
        valid_regions = []
        print ".................START..................\n" + text + "\n.................END..................\n"

        # parse text into an ast tree, calls is all call nodes in the tree
        try:
            ast_tree = ast.parse(text)
            finder = BuiltInFinder()
            finder.visit(ast_tree)
            calls = finder.calls
            print calls
        except Exception,e:
            print str(e)
            print 'I have failed :('
            calls = []

        # package ast nodes into region objects
        for call in calls:
            built_in = call.func.id
            start = findOffset(text_list, call)
            valid_regions.append(Region(node, start, start + len(built_in) - 1, built_in))
        print "valid_regions: " + str(valid_regions)
        return valid_regions